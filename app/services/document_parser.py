from langchain_community.document_loaders import PDFPlumberLoader
from typing import List
from app.models import Resume
from app.core.gemini import LLM
import aiofiles
import hashlib
from langchain_core.documents import Document
from pathlib import Path
from app.config import settings
from app.core.vector_store import VectorStore

# will make separate pinecone namespace for diffrent users, 
# for now we will use a common one for testing and development

# ----PINECODE SETUP----
Pinecone = VectorStore()
vector_store = Pinecone.vector_store()  # Get the initialized PineconeVectorStore instance
# ------------------------
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR = UPLOAD_DIR / "processed"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)



def json_splitter(doc):
    clean_name = doc['name'].lower().replace(" ", "_")
    unique_suffix = hashlib.md5(doc['email'].encode()).hexdigest()[:6]
    doc_id = f"{clean_name}_{unique_suffix}" 
    
    final_docs = []
    # --- Identity & Summary Chunk ---
    # summary is like a free throw, everyone says stuff but it may not be super reliable. So we can use it as a quick intro but not rely heavily on it for skills extraction or scoring.
    summary_content = f"Candidate: {doc['name']}\nSummary: {doc['summary']}\nCareer Level: {doc['career_level']}"
    final_docs.append(Document(
        page_content=summary_content, 
        metadata={"doc_id": doc_id, "chunk_id": f"{doc_id}_summary", "section": "summary"}
    ))

    # --- Education Chunk ---
    final_docs.append(Document(
        page_content=str(doc['education']), 
        metadata={"doc_id": doc_id, "chunk_id": f"{doc_id}_education", "section": "education"}
    ))

    # --- Skills Chunk ---
    final_docs.append(Document(
        page_content=f"Technical Skills: {', '.join(doc['skills'])}", 
        metadata={"doc_id": doc_id, "chunk_id": f"{doc_id}_skills", "section": "skills"}
    ))

    # --- Project Chunks (One per project) ---
    for i, project in enumerate(doc['projects']):
        project_text = f"Project: {project['name']}\nTech: {', '.join(project['tech_stack'])}\nDescription: {project['description']}"
        final_docs.append(Document(
            page_content=project_text, 
            metadata={"doc_id": doc_id, "chunk_id": f"{doc_id}_project_{i}", "section": "projects"}
        ))

    # add no of months, years timeline 
    # --- Experience Chunks (One per company) ---
    for i, experience in enumerate(doc['experience']):
        project_text = f"Company Name: {experience['name']}\nDesignation: {(experience['designation'])}\nResponsibilities: {experience['responsibilities']}"
        final_docs.append(Document(
            page_content=project_text, 
            metadata={"doc_id": doc_id, "chunk_id": f"{doc_id}_experience_{i}", "section": "experience"}
        ))

    # --- Certificate Chunks ---
    for i, cert in enumerate(doc['certificates']):
        cert_text = f"Certificate: {cert['title']}\nIssuer: {cert['issuer']}"
        final_docs.append(Document(
            page_content=cert_text, 
            metadata={"doc_id": doc_id, "chunk_id": f"{doc_id}_cert_{i}", "section": "certificates"}
        ))

    
    return final_docs


async def parse_resume(file_names:List[str]):
    model = LLM

    structured_output = model.with_structured_output(Resume, method="function_calling")
    
    for file in file_names:
        text = ""
        loader = PDFPlumberLoader(f"uploads/{file}")
        docs = loader.load()
        print(f"Loaded {len(docs)} pages from {file}")
        
        for page in docs:
            text += page.page_content + "\n"

        result = await structured_output.ainvoke(text)

        clean_name = result.name.lower().replace(" ", "_")
        unique_suffix = hashlib.md5(result.email.encode()).hexdigest()[:6]
        doc_id = f"{clean_name}_{unique_suffix}"
        
        file_path = UPLOAD_DIR / f"{doc_id}.json"

        async with aiofiles.open(file_path, 'w') as f:
            await f.write(result.model_dump_json(indent=4)) 

        print(f"Finished processing {file}...Starting embedding generation")
        
        # --- Generate embeddings for the processed document ---
        chunks = json_splitter(result.model_dump())

        ids = [chunk.metadata['chunk_id'] for chunk in chunks]
        print(f"Generated {len(chunks)} chunks for {file}")

        vector_store.add_documents(documents=chunks, ids=ids)
        print(f"Added {len(chunks)} chunks to Pinecone index for {doc_id}")