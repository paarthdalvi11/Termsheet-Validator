import faiss
import numpy as np
from sqlalchemy.orm import Session
from app.crud.chunk_ops import get_chunks
from app.database import SessionLocal
import os

def build_faiss_index(doc_id: int, output_dir: str = "app/indices"):
    """
    Build a FAISS index from document chunks' vector embeddings
    
    Args:
        doc_id: Document ID to build index for
        output_dir: Directory to save index and ID mapping
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Index and mapping file paths
    index_path = os.path.join(output_dir, f"doc_{doc_id}_index.faiss")
    ids_path = os.path.join(output_dir, f"doc_{doc_id}_ids.npy")
    
    # Get database session
    db = SessionLocal()
    try:
        # Get all chunks for document
        chunks = get_chunks(db, doc_id)
        
        if not chunks:
            raise ValueError(f"No chunks found for document ID {doc_id}")
        
        # Extract vectors and IDs
        vectors = []
        chunk_ids = []
        
        for chunk in chunks:
            if chunk.vector is not None:
                vectors.append(np.array(chunk.vector, dtype=np.float32))
                chunk_ids.append(chunk.id)
        
        if not vectors:
            raise ValueError(f"No vectors found for document ID {doc_id}")
        
        # Stack vectors into single array
        vectors_array = np.vstack(vectors)
        ids_array = np.array(chunk_ids, dtype=np.int64)
        
        # Get dimensionality
        dim = vectors_array.shape[1]
        
        # Create and train index
        index = faiss.IndexFlatL2(dim)  # L2 distance
        index.add(vectors_array)
        
        # Save index and ID mapping
        faiss.write_index(index, index_path)
        np.save(ids_path, ids_array)
        
        return {
            "status": "success",
            "document_id": doc_id,
            "vectors_indexed": len(vectors),
            "index_path": index_path,
            "ids_path": ids_path
        }
    
    except Exception as e:
        raise Exception(f"Failed to build index: {str(e)}")
    
    finally:
        db.close()