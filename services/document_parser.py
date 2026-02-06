import pdfplumber
from models import schemas
from services.rag_pipeline import get_llm

def parse_document(file):
    # will add code to save file later on, for now just read and extract text from pdf
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    llm = get_llm()
    structured_output = llm.with_structured_output(schemas.Resume, method="function_calling")
    result = structured_output.invoke(text)

    return result