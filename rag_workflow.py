import os
from dotenv import load_dotenv
from typing import TypedDict, List
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langgraph.graph import StateGraph, END
from ingest import load_vectorstore

load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# Define state schema
class RAGState(TypedDict):
    question: str
    rewritten_question: str
    retrieved_docs: List[Document]
    relevant_docs: List[Document]
    answer: str
    retry_count: int

# Load vectorstore
vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Node 1: Query Analysis
def query_analysis(state: RAGState) -> RAGState:
    question = state["question"]
    prompt = f"""Rewrite this question to be more specific and clear for document retrieval.
    Original question: {question}
    Rewritten question (just the question, nothing else):"""
    
    response = llm.invoke(prompt)
    rewritten = response.content.strip()
    print(f"Original: {question}")
    print(f"Rewritten: {rewritten}")
    
    return {**state, "rewritten_question": rewritten, "retry_count": 0}

# Node 2: Retrieval
def retrieve(state: RAGState) -> RAGState:
    question = state["rewritten_question"]
    docs = retriever.invoke(question)
    print(f"Retrieved {len(docs)} documents")
    return {**state, "retrieved_docs": docs}

# Node 3: Document Grading
def grade_documents(state: RAGState) -> RAGState:
    question = state["rewritten_question"]
    docs = state["retrieved_docs"]
    relevant_docs = []

    for doc in docs:
        prompt = f"""Is this document relevant to the question?
        Question: {question}
        Document: {doc.page_content}
        Answer with only 'relevant' or 'irrelevant':"""
        
        response = llm.invoke(prompt)
        grade = response.content.strip().lower()
        
        if "relevant" in grade:
            relevant_docs.append(doc)

    print(f"Relevant docs: {len(relevant_docs)} out of {len(docs)}")
    return {**state, "relevant_docs": relevant_docs}

# Node 4: Generation
def generate(state: RAGState) -> RAGState:
    question = state["question"]
    docs = state["relevant_docs"]
    
    context = "\n\n".join([
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in docs
    ])
    
    prompt = f"""Answer the question based on the context below.
    Include citations to the source documents in your answer.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    response = llm.invoke(prompt)
    return {**state, "answer": response.content.strip()}

# Node 5: Fallback
def fallback(state: RAGState) -> RAGState:
    retry_count = state.get("retry_count", 0) + 1
    print(f"No relevant docs found. Retry attempt {retry_count}")
    
    # Rewrite question differently for retry
    prompt = f"""Rewrite this question using different words for a second retrieval attempt:
    Question: {state['question']}
    Rewritten (just the question):"""
    
    response = llm.invoke(prompt)
    rewritten = response.content.strip()
    
    return {**state, "rewritten_question": rewritten, "retry_count": retry_count}

# Routing function
def route_after_grading(state: RAGState) -> str:
    if len(state["relevant_docs"]) > 0:
        return "generate"
    elif state.get("retry_count", 0) < 2:
        return "fallback"
    else:
        return "no_answer"

# No answer node
def no_answer(state: RAGState) -> RAGState:
    return {**state, "answer": "I don't have enough information in my documents to answer this question."}

# Build the graph
def build_rag_graph():
    graph = StateGraph(RAGState)
    
    # Add nodes
    graph.add_node("query_analysis", query_analysis)
    graph.add_node("retrieve", retrieve)
    graph.add_node("grade_documents", grade_documents)
    graph.add_node("generate", generate)
    graph.add_node("fallback", fallback)
    graph.add_node("no_answer", no_answer)
    
    # Add edges
    graph.set_entry_point("query_analysis")
    graph.add_edge("query_analysis", "retrieve")
    graph.add_edge("retrieve", "grade_documents")
    graph.add_edge("fallback", "retrieve")
    graph.add_edge("generate", END)
    graph.add_edge("no_answer", END)
    
    # Conditional edge after grading
    graph.add_conditional_edges(
        "grade_documents",
        route_after_grading,
        {
            "generate": "generate",
            "fallback": "fallback",
            "no_answer": "no_answer"
        }
    )
    
    return graph.compile()

# Create the app
rag_app = build_rag_graph()

def run_rag(question: str) -> dict:
    initial_state = RAGState(
        question=question,
        rewritten_question="",
        retrieved_docs=[],
        relevant_docs=[],
        answer="",
        retry_count=0
    )
    result = rag_app.invoke(initial_state)
    return {
        "question": result["question"],
        "answer": result["answer"],
        "sources": [doc.metadata.get("source", "unknown") for doc in result["relevant_docs"]]
    }