from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from typing import List
from services.document_parser import parse_document
from dotenv import load_dotenv
import aiofiles
from pathlib import Path as FilePath

load_dotenv()

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = FilePath("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_docs( background_tasks: BackgroundTasks, Files: List[UploadFile] = File(...), document_type: str = Form(...)):
    file_names: List[str] = []

    CHUNK_SIZE = 1024 * 1024  # 1MB
    for file in Files:
        file_path = UPLOAD_DIR / file.filename
        file_names.append(file.filename)

        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(CHUNK_SIZE):  # async read
                await out_file.write(content)  # async write
    
    background_tasks.add_task(parse_document, file_names)  # schedule the document parsing in the background
    return {
        "message": f"Successfully uploaded {len(Files)} files of type {document_type}. Parsing started in the background."
    }