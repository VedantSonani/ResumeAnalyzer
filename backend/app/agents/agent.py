from app.agents.tools import parse_job_description, perform_sementic_search
from app.agents.prompts import SYSTEM_PROMPT
from app.core.gemini import LLM
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=LLM,
    tools=[parse_job_description, perform_sementic_search],
    prompt=SYSTEM_PROMPT
)
