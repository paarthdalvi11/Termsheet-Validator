import faiss
import numpy as np
from typing import Tuple, List, Dict, Any
import os

class ChatbotRetriever:
    def __init__(self, index_dir: str = "app/indices/chatbot"):
        """
        Initialize chatbot retriever with unified index across all documents
        
        Args:
            index_dir: Directory containing chatbot index files
        """
        index_path = os.path.join(index_dir, "chatbot_index.faiss")
        ids_path = os.path.join(index_dir, "chatbot_ids.npy")
        
        if not os.path.exists(index_path) or not os.path.exists(ids_path):
            raise FileNotFoundError(
                "Chatbot index not found. Please run build_chatbot_index first."
            )
            
        self.index = faiss.read_index(index_path)
        self.id_map = np.load(ids_path)
        
    def query(self, query_vector: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Search for most similar chunks across all documents
        
        Args:
            query_vector: The query vector to search for
            top_k: Number of results to return
            
        Returns:
            Tuple of (chunk_ids, distances)
        """
        # Ensure vector is 2D with proper dtype
        if len(query_vector.shape) == 1:
            query_vector = query_vector.reshape(1, -1)
            
        query_vector = query_vector.astype(np.float32)
        
        # Perform search
        distances, indices = self.index.search(query_vector, top_k)
        
        # Map FAISS indices to actual chunk IDs
        chunk_ids = self.id_map[indices]
        
        return chunk_ids.flatten(), distances.flatten()
