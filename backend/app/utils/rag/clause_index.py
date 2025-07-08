import faiss
import numpy as np
from typing import List

class ClauseIndex:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.clause_map = {}

    def add_clauses(self, clauses: List[dict]):
        """Add clauses with their embeddings"""
        embeddings = np.array([c["embedding"] for c in clauses], dtype="float32")
        self.index.add(embeddings)
        for i, clause in enumerate(clauses):
            self.clause_map[i] = clause

    def search(self, query_embedding: np.ndarray, k: int = 5):
        """Search for similar clauses"""
        query_embedding = query_embedding.astype("float32").reshape(1, -1)
        distances, indices = self.index.search(query_embedding, k)
        return [
            {
                **self.clause_map[i],
                "score": float(d),
                "match_type": self._get_match_type(d)
            }
            for i, d in zip(indices[0], distances[0])
        ]

    def _get_match_type(self, distance: float):
        if distance < 0.2:  # Adjust thresholds as needed
            return "exact"
        elif distance < 0.5:
            return "partial"
        return "related"