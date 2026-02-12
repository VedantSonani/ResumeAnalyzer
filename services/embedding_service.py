from langchain_core.documents import Document
import hashlib

def json_splitter(doc):
    clean_name = doc['name'].lower().replace(" ", "_")
    unique_suffix = hashlib.md5(doc['email'].encode()).hexdigest()[:6]
    doc_id = f"{clean_name}_{unique_suffix}" 
    
    final_docs = []
    # --- Identity & Summary Chunk ---
    # summary is like a free throw, everyone says stuff but it may not be super reliable. So we can use it as a quick intro but not rely heavily on it for skills extraction or scoring.
    # summary_content = f"Candidate: {doc['name']}\nSummary: {doc['summary']}\nCareer Level: {doc['career_level']}"
    # final_docs.append(Document(
    #     page_content=summary_content, 
    #     metadata={"doc_id": doc_id, "chunk_id": f"{doc_id}_summary", "section": "summary"}
    # ))

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
