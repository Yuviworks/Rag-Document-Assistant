
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()

# Initialize embeddings
embeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

SUPPORTED_EXTENSIONS = (".txt", ".md", ".pdf")


def ingest_documents():
    documents = []
    docs_folder = "documents"

    os.makedirs(docs_folder, exist_ok=True)

    # Load TXT, Markdown, and PDF files
    for filename in os.listdir(docs_folder):
        filepath = os.path.join(docs_folder, filename)

        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        if filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(filepath)
        else:
            loader = TextLoader(filepath, encoding="utf-8")

        loaded_docs = loader.load()
        documents.extend(loaded_docs)

    if not documents:
        print("No supported documents found in documents folder!")
        return None

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    print(
        f"Created {len(chunks)} chunks "
        f"from {len(documents)} pages/documents"
    )
# Rebuild the vector database to prevent duplicate chunks
    vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="rag_documents"
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
