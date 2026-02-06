import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

SYSTEM_PROMPT = ""

def get_llm():
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    LLM = ChatGoogleGenerativeAI(
        # model = "gemma-3-12b-it",
        model = "gemini-3-flash-preview",
        api_key = GEMINI_API_KEY,
        temperature=1.0,  
        max_tokens=None,
        timeout=None,
        max_retries=1
    )

    return LLM

def get_prompt(user_prompt):
    # gemma models dont take system instructions

    prompt = [
        ("system", SYSTEM_PROMPT),
        ("human", user_prompt)
    ]

    return prompt


async def get_response(message):
    llm = get_llm()
    response = await llm.ainvoke(message)
    response = response.content

    return response