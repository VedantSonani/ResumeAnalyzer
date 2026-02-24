from fastapi import APIRouter
from app.api.auth import auth
from app.api.v1.endpoints import chat, documents, match, frontend

router = APIRouter(prefix="/api/v1")

router.include_router(chat.router)
router.include_router(documents.router)
router.include_router(frontend.router)
# router.include_router(match.router)