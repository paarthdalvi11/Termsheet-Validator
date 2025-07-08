import json
from datetime import datetime
from typing import Dict, Any

def log_validation(termsheet_id: str, result: Dict[str, Any]) -> None:
    """
    Log validation results to a structured format for auditing.
    
    Args:
        termsheet_id: Identifier for the termsheet (filename or ID)
        result: Validation result dictionary
    """
    timestamp = datetime.now().isoformat()
    
    log_entry = {
        "termsheet_id": termsheet_id,
        "timestamp": timestamp,
        "criticality_score": result.get("criticality_score", 0),
        "error_count": len(result.get("errors", [])),
        "summary": result.get("validation_summary", "")
    }
    
    # In a production system, you would write to a database or log file
    # For now, just print in a structured format
    print(f"[VALIDATION LOG] {json.dumps(log_entry)}")
