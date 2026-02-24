from app.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI


LLM = ChatGoogleGenerativeAI(
        # model = "gemini-2.5-flash",
        # model = "gemini-2.5-flash-lite",
        # model = "gemini-2.5-pro",
        model = "gemini-3-flash-preview",
        api_key = settings.GEMINI_API_KEY,
        temperature=0.0,  
        max_tokens=None,
        timeout=None
)
