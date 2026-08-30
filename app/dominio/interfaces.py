from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IVectorDatabase(ABC):
    """
    Abstract Base Class defining the strict contract for Vector Database operations.
    Any underlying infrastructure (ChromaDB, Qdrant, etc.) must inherit from this 
    interface and implement its methods.
    """

    @abstractmethod
    def connect(self) -> None:
        """
        Establishes the connection or initializes the vector database client.
        """
        pass

    @abstractmethod
    def add_documents(self, chunks: List[str], metadatas: List[Dict[str, Any]]) -> bool:
        """
        Ingests text chunks, converts them to vector embeddings, and stores them.
        
        Args:
            chunks: A list of text strings to be vectorized.
            metadatas: A list of dictionaries containing metadata for each chunk.
            
        Returns:
            bool: True if the operation was successful.
        """
        pass

    @abstractmethod
    def similarity_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs a vector similarity search against the stored embeddings.
        
        Args:
            query: The user's input string to search for.
            top_k: The number of most similar results to return.
            
        Returns:
            A list of dictionaries representing the retrieved documents and metadata.
        """
        pass