from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router as v1_router
from app.api.auth.auth import router as auth_router

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

# ---------------------------
# Session Middleware for login
# ---------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key="your_secret_key_here",
)


# ---------------------------------------------------------
# Router v1
# ---------------------------------------------------------
app.include_router(v1_router)


# ---------------------------------------------------------
# Auth
# ---------------------------------------------------------
app.include_router(auth_router)

# ---------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": app.title,
        "version": app.version
    }


# ---------------------------------------------------------
# Global Exception Handler
# ---------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "Major error occurred. Please try again later.",
            "message": str(exc)
        },
    )

# Job Description to test the project
# Get me top 3 candidates that are good match for the following Job Description:\n\nJob Description: Junior Generative AI Developer (2026 Graduate Cohort)\n\nRole Overview:\nWe are hiring a Junior Generative AI Developer for our 2026 graduate batch.\nThe ideal candidate is a final-year B.Tech student (Class of 2026) with hands-on experience building production-ready AI applications using LLMs, RAG pipelines, and full-stack Python frameworks.\n\nKey Responsibilities:\n- Build and deploy LLM-powered applications using LangChain and OpenAI APIs\n- Develop multi-agent RAG systems with vector databases (FAISS, Pinecone, pgvector)\n- Integrate AI backends with web frameworks (Django / Flask)\n- Work with local LLMs using tools like Ollama or LM Studio\n- Build and maintain full-stack AI web applications with REST APIs


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)