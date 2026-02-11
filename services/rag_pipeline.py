import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SYSTEM_PROMPT = ""

LLM = ChatGoogleGenerativeAI(
        # model = "gemma-3-12b-it",
        # model = "gemini-2.5-flash",
        model="gemini-2.5-flash-lite",
        # model = "gemini-3-flash-preview",
        api_key = GEMINI_API_KEY,
        temperature=0.5,  
        max_tokens=None,
        timeout=None,
        max_retries=1
)

def get_prompt(user_prompt):
    # gemma models dont take system instructions
    prompt = [
        ("system", SYSTEM_PROMPT),
        ("human", user_prompt)
    ]

    return prompt

async def get_response(message):
    model = LLM
    response = await model.ainvoke(message)
    response = response.content

    return response