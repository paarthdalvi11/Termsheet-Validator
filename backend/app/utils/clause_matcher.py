import hashlib
import numpy as np
import faiss
from typing import List, Dict, Any
from app.schemas import ClauseMatch

class FaissClauseMatcher:
    """
    Semantic clause matching using FAISS vector search for termsheet validation.
    """
    
    def __init__(self, reference_clauses: List[str]):
        """
        Initialize the clause matcher with reference clauses.
        
        Args:
            reference_clauses: List of standard clauses to match against
        """
        self.ref_clauses = reference_clauses
        # Dimension for nomic-embed-text embeddings
        self.index = faiss.IndexFlatL2(768)
        self.clause_text_map = {}
        self._build_index()

    def _build_index(self):
        """Build FAISS index from reference clauses"""
        from app.utils.validation_helpers import get_embedding
        
        embeddings = []
        for i, clause in enumerate(self.ref_clauses):
            # Generate embedding for reference clause
            emb = get_embedding(clause)
            # Create a unique identifier for the clause
            hash_id = hashlib.md5(clause.encode()).hexdigest()
            self.clause_text_map[hash_id] = {
                "text": clause,
                "index": i
            }
            embeddings.append(emb)
        
        # Add embeddings to FAISS index if we have any
        if embeddings:
            embeddings_array = np.vstack(embeddings).astype('float32')
            self.index.add(embeddings_array)

    def match(self, uploaded_clauses: List[str]) -> List[ClauseMatch]:
        """
        Find semantic matches for each clause in the document.
        
        Args:
            uploaded_clauses: List of clauses extracted from uploaded termsheet
            
        Returns:
            List of ClauseMatch objects with similarity scores and match types
        """
        from app.utils.validation_helpers import get_embedding
        
        matches = []
        
        for clause in uploaded_clauses:
            # Skip very short clauses (likely not meaningful)
            if len(clause.strip()) < 20:
                continue
                
            # Get embedding for the clause
            emb = get_embedding(clause).reshape(1, -1)
            
            # Search for nearest neighbor in FAISS index
            D, I = self.index.search(emb, 1)
            
            # Calculate similarity score (inverse of distance)
            similarity = 1 / (1 + D[0][0])
            
            # Determine match type based on similarity threshold
            match_type = (
                "match" if similarity > 0.1 else
                "partial" if similarity > 0.01 else
                "missing"
            )
            
            matches.append(ClauseMatch(
                clause=clause,
                match_type=match_type,
                similarity=float(similarity)
            ))
        
        return matches
