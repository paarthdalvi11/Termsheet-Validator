from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.audit_trail import AuditTrail
from app.schemas import AuditLog
from datetime import datetime

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.post("/log")
async def log_audit_entry(
    log_data: AuditLog, 
    db: Session = Depends(get_db)
):
    """
    Create an audit log entry to track system actions
    """
    try:
        # Create audit trail entry
        audit_entry = AuditTrail(
            user_id=log_data.user_id,
            action=log_data.action,
            details=f"Validation ID: {log_data.validation_id}",
            timestamp=datetime.utcnow()
        )
        
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)
        
        return {"status": "success", "audit_id": audit_entry.id}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create audit log: {str(e)}")

@router.get("/history")
async def get_audit_history(
    user_id: int = None,
    action: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Retrieve audit history with optional filters
    """
    try:
        query = db.query(AuditTrail)
        
        # Apply filters if provided
        if user_id:
            query = query.filter(AuditTrail.user_id == user_id)
        
        if action:
            query = query.filter(AuditTrail.action == action)
        
        # Get results ordered by timestamp
        results = query.order_by(AuditTrail.timestamp.desc()).limit(limit).all()
        
        # Convert to dict format
        audit_logs = [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "details": log.details,
                "timestamp": log.timestamp.isoformat()
            }
            for log in results
        ]
        
        return {"audit_logs": audit_logs, "count": len(audit_logs)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve audit logs: {str(e)}")