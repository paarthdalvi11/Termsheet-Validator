import faiss
import numpy as np
from typing import Tuple, List

class FaissRetriever:
    def __init__(self, index_path: str, ids_path: str):
        """
        Initialize FAISS retriever with pre-built index
        
        Args:
            index_path: Path to the saved FAISS index
            ids_path: Path to numpy array of chunk IDs
        """
        self.index = faiss.read_index(index_path)
        self.id_map = np.load(ids_path)  # maps row-idx → chunk_id
        
    def query(self, query_vector: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Search for most similar vectors in the index
        
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
    
    def batch_query(self, query_vectors: np.ndarray, top_k: int = 5) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Search for multiple query vectors at once
        
        Args:
            query_vectors: Batch of query vectors, shape (n, dim)
            top_k: Number of results per query
            
        Returns:
            List of (chunk_ids, distances) tuples for each query
        """
        query_vectors = query_vectors.astype(np.float32)
        distances, indices = self.index.search(query_vectors, top_k)
        
        results = []
        for i in range(distances.shape[0]):
            chunk_ids = self.id_map[indices[i]]
            results.append((chunk_ids, distances[i]))
            
        return results