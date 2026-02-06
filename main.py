from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import documents, chat, frontend


app = FastAPI(
    title="Resume Analyzer API",
    description="Resume & Job Description parsing with RAG-based matching",
    version="1.0.0"
)

# ---------------------------
# CORS Middleware
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change it later on, right now it allows every req from all sources
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(frontend.router)
