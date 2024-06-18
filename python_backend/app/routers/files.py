from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from app.utils.file_utils import save_upload_file, ALLOWED_EXTENSIONS
from app.services.parser import parse_file
import os

router = APIRouter()

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/uploadfile/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    if not file.filename.split(".")[-1] in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    await save_upload_file(file, file_location)

    # Correctly add file parsing to background tasks
    parse_file(file_location, background_tasks)

    return {"filename": file.filename, "status": "File uploaded successfully. Parsing in progress."}