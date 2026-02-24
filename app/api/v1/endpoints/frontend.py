from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter(
    tags=["Frontend"]
)


BASE_DIR = Path(__file__).resolve().parents[3]

templates = Jinja2Templates(directory=str(BASE_DIR /'frontend'/'templates'))

@router.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/features", response_class=HTMLResponse)
async def serve_features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})

@router.get("/how-it-works", response_class=HTMLResponse)
async def serve_how_it_works(request: Request):
    return templates.TemplateResponse("how_it_works.html", {"request": request})

@router.get("/pricing", response_class=HTMLResponse)
async def serve_pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
