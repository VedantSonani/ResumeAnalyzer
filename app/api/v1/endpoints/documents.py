from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from typing import List, Literal
from app.services.document_parser import parse_resume
import aiofiles
from app.config import settings
from pathlib import Path

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path(settings.UPLOAD_DIR)

# will add a middleware later to verify the jwt token and extract user info, 
# for now we will do it in the endpoint itself
@router.post("/upload")
async def upload_docs( background_tasks: BackgroundTasks, 
                      Files: List[UploadFile] = File(...), 
                      document_type: Literal["resume", "job description"] = Form(...)):
    
    file_names: List[str] = []

    CHUNK_SIZE = 1024 * 1024  # 1MB
    for file in Files:
        file_path = UPLOAD_DIR / file.filename
        file_names.append(file.filename)

        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(CHUNK_SIZE):  # async read
                await out_file.write(content)  # async write
    
    background_tasks.add_task(parse_resume, file_names)  # schedule the document parsing in the background
    return {
        "message": f"Successfully uploaded {len(Files)} files of type {document_type}. Parsing started in the background."
    }