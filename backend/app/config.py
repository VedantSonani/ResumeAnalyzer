from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    PINECONE_API_KEY: str
    SECRET_KEY: str
    USER_ID_SALT: str
    PINECONE_INDEX_NAME: str = "resume-analyzer"
    PINECONE_NAMESPACE: str = "resumes_v3"
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"

settings = Settings()