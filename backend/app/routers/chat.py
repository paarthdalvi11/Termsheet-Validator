from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.rag.chatbot.retriever import ChatbotRetriever
from app.utils.llm_integration import embed_text
from app.crud.chunk_ops import get_chunks_by_ids
from typing import List, Dict, Any
import numpy as np

router = APIRouter()

@router.post("/chat")
def chat_with_docs(query: str, db: Session = Depends(get_db)):
    try:
        # 1. Embed the query
        query_vector = np.array(embed_text(query))
        
        # 2. Retrieve relevant chunks
        retriever = ChatbotRetriever()
        chunk_ids, distances = retriever.query(query_vector, top_k=5)
        
        # 3. Get chunk details from database
        chunks = get_chunks_by_ids(db, chunk_ids.tolist())
        
        # 4. Format results
        results = []
        for i, chunk in enumerate(chunks):
            results.append({
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,  # CORRECTED: using content instead of chunk_text
                "relevance_score": float(1.0 - distances[i]),  # Convert distance to similarity score
            })
        
        # 5. Generate response using an LLM (placeholder - implement in llm_integration.py)
        # response = generate_response(query, [c["content"] for c in results])
        
        return {
            "query": query,
            "relevant_chunks": results,
            # "response": response  # Uncomment when LLM integration is ready
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
