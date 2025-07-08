import os
import json
from typing import Dict, Any
import ollama
from sentence_transformers import SentenceTransformer

# Initialize model once for efficiency
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def embed_text(text: str) -> list[float]:
    """Generate embedding for text using sentence transformer"""
    model = get_embedding_model()
    embedding = model.encode(text)
    return embedding.tolist()  # Convert to list for JSON storage

class LLMValidator:
    def __init__(self):
        self.model = "mistral"  # Default model
        with open("app/utils/prompt_templates/termsheet_validation.json", "r") as f:
            self.templates = json.load(f)
    
    async def validate(self, text: str) -> Dict[str, Any]:
        """
        Validate document text using LLM
        """
        # Get the prompt template
        prompt = self.templates["validation_prompt"].format(text=text)
        
        try:
            # Call the Ollama API
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json",
                options={"temperature": 0.0, "num_ctx": 16000}
            )
            
            # Parse the response
            result = json.loads(response["response"])
            
            # Validate the result has all required fields
            required_fields = ["errors", "criticality_score", "validation_summary"]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"LLM response missing required field: {field}")
            
            return result
            
        except Exception as e:
            raise Exception(f"LLM validation failed: {str(e)}")