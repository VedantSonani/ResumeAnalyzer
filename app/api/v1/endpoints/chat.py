from fastapi import APIRouter, Header
from app.models.PromptModel import Prompt
from app.agents.agent import agent
from app.core.memory import Memory
from app.core.auth import verify_access_token
from langchain.messages import AIMessage, HumanMessage


router = APIRouter(
    prefix="/chat",
    tags=["LLM"]
)

# will add a middleware later to verify the jwt token and extract user info, 
# for now we will do it in the endpoint itself
@router.post("/")
async def chat(input : Prompt, jwt_token:str = Header()):
    user_id = verify_access_token(jwt_token)
    msg_history = Memory(user_id)

    msg_history.add_to_memory(HumanMessage(input.msg))

    answer = await agent.ainvoke({"messages": msg_history.get_memory()})
    msg_history.add_to_memory(AIMessage(answer["messages"][-1].text))

    return {
        "msg" : answer["messages"][-1].text
    }