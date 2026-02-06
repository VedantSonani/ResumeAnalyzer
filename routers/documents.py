from fastapi import APIRouter, UploadFile, File, Form
import pdfplumber
from dotenv import load_dotenv
from models import schemas
import os
from services.rag_pipeline import get_llm
load_dotenv()

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
def upload_docs(file: UploadFile = File(...), document_type: str = Form(...)):
    
    # will add pdf parsing
    # once extracted raw txt, will embed them into vector db using gemini embedding model
    print("Extracting text from PDF...")
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    llm = get_llm()
    structured_output = llm.with_structured_output(schemas.Resume, method="function_calling")
    result = structured_output.invoke(text)

    return {
        "filename" : file.filename,
        "document_type" : document_type,
        "parsed_data" : result
    }