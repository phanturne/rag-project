from fastapi import APIRouter, HTTPException
from app.services.rag_model import mock_rag_model
import os

router = APIRouter()

UPLOAD_DIR = "./uploaded_files"

@router.get("/ask/")
async def ask_question(filename: str, question: str):
    file_path = f"{UPLOAD_DIR}/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    answer = mock_rag_model(file_path, question)
    return {"filename": filename, "question": question, "answer": answer}