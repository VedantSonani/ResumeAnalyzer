from langchain_core.tools import tool
from typing import List, Tuple
from app.core.vector_store import VectorStore
Pinecone = VectorStore()  # Initialize the vector store (e.g., Pinecone)\
vector_store = Pinecone.vector_store()  # Get the initialized vector store instance

@tool
def perform_sementic_search(query: str, top_k: int, sections: List[str]) -> List[Tuple]:
    """
        Performs a semantic (context-based) search across the vector database to retrieve 
        the most relevant information based on conceptual similarity rather than exact 
        keyword matches. 

        Use this tool when the user asks complex questions, seeks background information, 
        or when a direct keyword search fails to provide depth. 

        Args:
            query (str): The natural language search string or question.
            top_k (int): The number of highly relevant documents to return.
            sections (List[str]): A list of section names to narrow the search scope.

        Returns:
            List[Tuple]: A ranked list of search results with their corresponding similarity scores. 
                Returns an empty list if no results meet the minimum relevance threshold (0.15).
        """
    # search_results = vector_store.similarity_search_with_score(query, k=top_k, filter=filter)
    search_results = vector_store.similarity_search_with_score(query, k=top_k, filter={"section": {"$in": sections}})

    if search_results[0][-1] < 0.15:
        return []  # No relevant results found
    return search_results
