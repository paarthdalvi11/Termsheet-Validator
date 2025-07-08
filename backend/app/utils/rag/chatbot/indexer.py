import faiss
import numpy as np
import os
from app.database import SessionLocal
from app.crud.chunk_ops import get_all_chunks

def build_chatbot_index(output_dir: str = "app/indices/chatbot"):
    """
    Build a unified FAISS index for the chatbot from ALL document chunks
    
    Args:
        output_dir: Directory to save chatbot index and ID mapping
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Index and mapping file paths
    index_path = os.path.join(output_dir, "chatbot_index.faiss")
    ids_path = os.path.join(output_dir, "chatbot_ids.npy")
    
    # Get database session
    db = SessionLocal()
    try:
        # Get all chunks across all documents
        chunks = get_all_chunks(db)  # Create this function in crud/chunk_ops.py
        
        if not chunks:
            raise ValueError("No chunks found in the database")
        
        # Extract vectors and IDs
        vectors = []
        chunk_ids = []
        
        for chunk in chunks:
            if chunk.vector is not None:
                vectors.append(np.array(chunk.vector, dtype=np.float32))
                chunk_ids.append(chunk.id)
        
        if not vectors:
            raise ValueError("No vectors found in the database")
        
        # Stack vectors into single array
        vectors_array = np.vstack(vectors)
        ids_array = np.array(chunk_ids, dtype=np.int64)
        
        # Get dimensionality
        dim = vectors_array.shape[1]
        
        # Create and train index
        index = faiss.IndexFlatL2(dim)
        index.add(vectors_array)
        
        # Save index and ID mapping
        faiss.write_index(index, index_path)
        np.save(ids_path, ids_array)
        
        return {
            "status": "success",
            "vectors_indexed": len(vectors),
            "index_path": index_path,
            "ids_path": ids_path
        }
    
    except Exception as e:
        raise Exception(f"Failed to build chatbot index: {str(e)}")
    
    finally:
        db.close()

