from app.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI

# Use REST transport instead of gRPC to avoid OAuth issues
LLM = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.0,
    max_tokens=None,
    timeout=None,
    transport="rest",  # Use REST API instead of gRPC
)
