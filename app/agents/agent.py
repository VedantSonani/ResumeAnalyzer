from app.agents.tools import parse_job_description, perform_sementic_search
from app.agents.prompts import SYSTEM_PROMPT
from app.core.gemini import LLM
from langchain.agents import create_agent

agent = create_agent(
    model=LLM,
    tools=[parse_job_description, perform_sementic_search],
    system_prompt=SYSTEM_PROMPT
)
