from fastapi import APIRouter
from pathlib import Path
from app.config import settings
from datetime import datetime
import json

router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)

PROCESSED_DIR = Path(settings.UPLOAD_DIR) / "processed"


@router.get("/")
async def get_stats():
    """Get dashboard statistics"""
    
    # Count processed resumes (JSON files)
    resume_count = 0
    candidates = set()
    today_count = 0
    today = datetime.now().date()
    
    if PROCESSED_DIR.exists():
        for json_file in PROCESSED_DIR.glob("*.json"):
            resume_count += 1
            
            # Check if processed today
            file_mtime = datetime.fromtimestamp(json_file.stat().st_mtime).date()
            if file_mtime == today:
                today_count += 1
            
            # Extract candidate name
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    if 'name' in data:
                        candidates.add(data['name'])
            except:
                pass
    
    return {
        "resumes": resume_count,
        "candidates": len(candidates),
        "queries": 0,  # Could track this with a counter
        "today": today_count
    }
