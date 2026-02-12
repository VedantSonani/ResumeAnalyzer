from langchain_community.document_loaders import PDFPlumberLoader
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from pinecone import Pinecone
from typing import List
import os
from dotenv import load_dotenv
from models import schemas
from services.rag_pipeline import LLM
from services.embedding_service import json_splitter
import aiofiles
import hashlib
from pathlib import Path as FilePath

load_dotenv()
# ----PINECODE SETUP----
PINECODE_API_KEY = os.getenv("PINECODE_API_KEY")

pc = Pinecone(api_key=PINECODE_API_KEY)
index_name = "resume-analyzer"
index = pc.Index(index_name)
embeddings = PineconeEmbeddings(model="llama-text-embed-v2", api_key=PINECODE_API_KEY)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)
# ------------------------

UPLOAD_DIR = FilePath("uploads/processed")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def parse_resume(file_names:List[str]):
    model = LLM

    structured_output = model.with_structured_output(schemas.Resume, method="function_calling")
    
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