from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
def upload_docs(file: UploadFile = File(...), document_type: str = Form(...)):
    
    # will add pdf parsing
    # once extracted raw txt, will embed them into vector db using gemini embedding model
    
    return {
        "filename" : file.filename,
        "document_type" : document_type
    }