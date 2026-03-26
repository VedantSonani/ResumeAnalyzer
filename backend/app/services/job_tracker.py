from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import asyncio

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileStatus(BaseModel):
    filename: str
    status: JobStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    candidate_name: Optional[str] = None
    chunks_created: int = 0

class JobInfo(BaseModel):
    job_id: str
    created_at: datetime
    files: List[FileStatus]
    total_files: int
    completed_files: int
    failed_files: int

# In-memory job store (use Redis/DB in production)
_jobs: Dict[str, JobInfo] = {}
_lock = asyncio.Lock()

async def create_job(job_id: str, filenames: List[str]) -> JobInfo:
    async with _lock:
        job = JobInfo(
            job_id=job_id,
            created_at=datetime.now(),
            files=[FileStatus(filename=f, status=JobStatus.QUEUED) for f in filenames],
            total_files=len(filenames),
            completed_files=0,
            failed_files=0
        )
        _jobs[job_id] = job
        return job

async def update_file_status(
    job_id: str, 
    filename: str, 
    status: JobStatus, 
    error: Optional[str] = None,
    candidate_name: Optional[str] = None,
    chunks_created: int = 0
):
    async with _lock:
        if job_id not in _jobs:
            return
        
        job = _jobs[job_id]
        for file_status in job.files:
            if file_status.filename == filename:
                file_status.status = status
                if status == JobStatus.PROCESSING:
                    file_status.started_at = datetime.now()
                elif status in [JobStatus.COMPLETED, JobStatus.FAILED]:
                    file_status.completed_at = datetime.now()
                    if status == JobStatus.COMPLETED:
                        job.completed_files += 1
                        file_status.candidate_name = candidate_name
                        file_status.chunks_created = chunks_created
                    else:
                        job.failed_files += 1
                        file_status.error = error
                break

async def get_job(job_id: str) -> Optional[JobInfo]:
    async with _lock:
        return _jobs.get(job_id)

async def get_all_jobs() -> List[JobInfo]:
    async with _lock:
        # Return jobs sorted by created_at desc, limit to last 20
        jobs = sorted(_jobs.values(), key=lambda j: j.created_at, reverse=True)
        return jobs[:20]

async def cleanup_old_jobs(max_age_hours: int = 24):
    """Remove jobs older than max_age_hours"""
    async with _lock:
        now = datetime.now()
        to_remove = []
        for job_id, job in _jobs.items():
            age = (now - job.created_at).total_seconds() / 3600
            if age > max_age_hours:
                to_remove.append(job_id)
        for job_id in to_remove:
            del _jobs[job_id]
