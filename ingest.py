import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()

# Initialize embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_documents():
    documents = []
    docs_folder = "documents"
    
    # Load all text files from documents folder
    for filename in os.listdir(docs_folder):
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(docs_folder, filename)
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())
    
    if not documents:
        print("No documents found in documents folder!")
        return None
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} documents")
    
    # Store in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print("Documents ingested and stored in ChromaDB successfully!")
    return vectorstore

def load_vectorstore():
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

if __name__ == "__main__":
    ingest_documents()