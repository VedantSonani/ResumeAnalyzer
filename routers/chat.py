from dotenv import load_dotenv
from fastapi import APIRouter
from services import rag_pipeline
from models import schemas

load_dotenv()

router = APIRouter(
    prefix="/chat",
    tags=["LLM"]
)

@router.post("/")
async def ask_llm(input : schemas.Prompt):
    '''gemma models dont take system instructions'''
    # message = [
    #     ("system", SYSTEM_PROMPT),
    #     ("human", prompt.msg)
    # ]
    prompt = rag_pipeline.get_prompt(input.msg)

    answer = await rag_pipeline.get_response(prompt)

    return {
        "msg" : answer[0]["text"]
    }