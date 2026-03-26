from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from typing import List, Literal
from app.services.document_parser import parse_resume
from app.services.job_tracker import create_job, get_job, get_all_jobs, JobInfo
import aiofiles
from app.config import settings
from pathlib import Path
import uuid

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_docs(
    background_tasks: BackgroundTasks, 
    Files: List[UploadFile] = File(...), 
    document_type: Literal["resume", "job description"] = Form(...)
):
    """Upload documents and start background processing"""
    
    # Generate job ID
    job_id = str(uuid.uuid4())[:8]
    file_names: List[str] = []

    CHUNK_SIZE = 1024 * 1024  # 1MB
    for file in Files:
        file_path = UPLOAD_DIR / file.filename
        file_names.append(file.filename)

        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(CHUNK_SIZE):
                await out_file.write(content)
    
    # Create job tracker entry
    await create_job(job_id, file_names)
    
    # Schedule background processing
    background_tasks.add_task(parse_resume, job_id, file_names)
    
    return {
        "message": f"Successfully uploaded {len(Files)} files. Processing started.",
        "job_id": job_id,
        "files": file_names
    }


@router.get("/jobs")
async def list_jobs() -> List[JobInfo]:
    """Get all recent processing jobs"""
    return await get_all_jobs()


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get status of a specific job"""
    job = await get_job(job_id)
    if not job:
        return {"error": "Job not found"}
    return job
