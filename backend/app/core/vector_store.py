from app.config import settings
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from pinecone import Pinecone


class VectorStore:
    def __init__(self, 
                 index_name: str = settings.PINECONE_INDEX_NAME, 
                 namespace: str = settings.PINECONE_NAMESPACE):
        
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        index = pc.Index(index_name)
        embeddings = PineconeEmbeddings(model="llama-text-embed-v2", api_key=settings.PINECONE_API_KEY)
        self.store = PineconeVectorStore(index=index, embedding=embeddings, namespace=namespace)

    def vector_store(self):
        return self.store