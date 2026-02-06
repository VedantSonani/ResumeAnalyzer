from fastapi import APIRouter, UploadFile, File, Form
import pdfplumber
from dotenv import load_dotenv
from services.document_parser import parse_document

load_dotenv()

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
def upload_docs(file: UploadFile = File(...), document_type: str = Form(...)):
    
    # once extracted raw txt, will embed them into vector db using gemini embedding model
    # will do embedding later
    result = parse_document(file)

    return {
        "filename" : file.filename,
        "document_type" : document_type,
        "parsed_data" : result
    }