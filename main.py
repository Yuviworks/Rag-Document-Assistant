
import os
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional

from ingest import ingest_documents, load_vectorstore
from rag_workflow import run_rag

app = FastAPI(
    title="RAG Technical Documentation Assistant",
    description="A RAG-powered assistant for technical documentation",
    version="1.0.0"
)

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}
DOCS_FOLDER = "documents"

os.makedirs(DOCS_FOLDER, exist_ok=True)


# Request/Response models
class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: str
    comment: Optional[str] = None


# Store feedback in memory
feedback_store = []


# POST /query
@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        result = run_rag(request.question)

        return QueryResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# POST /ingest
@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only TXT, Markdown, and PDF files are supported."
        )

    try:
        file_path = os.path.join(DOCS_FOLDER, filename)

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        with open(file_path, "wb") as f:
            f.write(content)

        ingest_documents()

        return {
            "message": f"File '{filename}' ingested successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET /documents
@app.get("/documents")
async def list_documents():
    try:
        files = [
            filename
            for filename in os.listdir(DOCS_FOLDER)
            if Path(filename).suffix.lower() in SUPPORTED_EXTENSIONS
        ]

        return {
            "documents": files,
            "count": len(files)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# POST /feedback
@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    if request.rating not in ["thumbs_up", "thumbs_down"]:
        raise HTTPException(
            status_code=400,
            detail="Rating must be 'thumbs_up' or 'thumbs_down'"
        )

    feedback_store.append({
        "question": request.question,
        "answer": request.answer,
        "rating": request.rating,
        "comment": request.comment
    })

    return {"message": "Feedback received, thank you!"}


# GET / (health check)
@app.get("/")
async def root():
    return {
        "message": "RAG Assistant is running!",
        "status": "healthy"
    }
