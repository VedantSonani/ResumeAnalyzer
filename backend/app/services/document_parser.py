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
from app.services.job_tracker import update_file_status, JobStatus

# ----PINECODE SETUP----
Pinecone = VectorStore()
vector_store = Pinecone.vector_store()
# ------------------------

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
PROCESSED_DIR = UPLOAD_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def json_splitter(doc):
    clean_name = doc['name'].lower().replace(" ", "_")
    unique_suffix = hashlib.md5(doc['email'].encode()).hexdigest()[:6]
    doc_id = f"{clean_name}_{unique_suffix}" 
    
    final_docs = []
    
    # --- Identity & Summary Chunk ---
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

    # --- Project Chunks ---
    for i, project in enumerate(doc['projects']):
        project_text = f"Project: {project['name']}\nTech: {', '.join(project['tech_stack'])}\nDescription: {project['description']}"
        final_docs.append(Document(
            page_content=project_text, 
            metadata={"doc_id": doc_id, "chunk_id": f"{doc_id}_project_{i}", "section": "projects"}
        ))

    # --- Experience Chunks ---
    for i, experience in enumerate(doc['experience']):
        exp_text = f"Company Name: {experience['name']}\nDesignation: {experience['designation']}\nResponsibilities: {experience['responsibilities']}"
        final_docs.append(Document(
            page_content=exp_text, 
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


async def parse_resume(job_id: str, file_names: List[str]):
    """Parse resumes with job tracking"""
    model = LLM
    structured_output = model.with_structured_output(Resume, method="function_calling")
    
    for file in file_names:
        try:
            # Update status to processing
            await update_file_status(job_id, file, JobStatus.PROCESSING)
            
            # Load PDF
            text = ""
            loader = PDFPlumberLoader(f"uploads/{file}")
            docs = loader.load()
            print(f"[Job {job_id}] Loaded {len(docs)} pages from {file}")
            
            for page in docs:
                text += page.page_content + "\n"

            # Extract structured data
            result = await structured_output.ainvoke(text)

            # Generate doc ID
            clean_name = result.name.lower().replace(" ", "_")
            unique_suffix = hashlib.md5(result.email.encode()).hexdigest()[:6]
            doc_id = f"{clean_name}_{unique_suffix}"
            
            # Save JSON
            file_path = PROCESSED_DIR / f"{doc_id}.json"
            async with aiofiles.open(file_path, 'w') as f:
                await f.write(result.model_dump_json(indent=4)) 

            print(f"[Job {job_id}] Finished processing {file}, starting embeddings...")
            
            # Generate and store embeddings
            chunks = json_splitter(result.model_dump())
            ids = [chunk.metadata['chunk_id'] for chunk in chunks]
            vector_store.add_documents(documents=chunks, ids=ids)
            
            print(f"[Job {job_id}] Added {len(chunks)} chunks for {doc_id}")
            
            # Update status to completed
            await update_file_status(
                job_id, file, JobStatus.COMPLETED,
                candidate_name=result.name,
                chunks_created=len(chunks)
            )
            
        except Exception as e:
            print(f"[Job {job_id}] Error processing {file}: {str(e)}")
            await update_file_status(job_id, file, JobStatus.FAILED, error=str(e))
