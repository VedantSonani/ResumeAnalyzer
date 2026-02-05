import os
from dotenv import load_dotenv
from fastapi import APIRouter
from langchain_google_genai import ChatGoogleGenerativeAI
from services import rag_pipeline
from models import schemas

load_dotenv()

router = APIRouter(
    prefix="/chat",
    tags=["LLM"]
)

SYSTEM_PROMPT = ""

@router.post("/")
async def ask_llm(prompt : schemas.Prompt):
    message = [
        ("system", SYSTEM_PROMPT),
        ("human", prompt.msg)
    ]

    answer = await rag_pipeline.get_response(message)

    return {
        "msg" : answer
    }