import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    LLM = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash",
        api_key = GEMINI_API_KEY,
        temperature=1.0,  
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    return LLM

async def get_response(message):
    llm = get_llm()
    response = await llm.ainvoke(message)
    response = response.content

    return response