from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Explicit router imports
from app.routers.upload import router as upload_router
from app.routers.validate import router as validate_router
from app.routers.analyze import router as analyze_router
from app.routers.audit import router as audit_router
from app.routers.dbops import router as dbops_router
from app.routers.chat import router as chat_router

from app.models.base import Base
from app.database import engine
import app.models  # Ensure all models are registered

# Initialize the FastAPI app
app = FastAPI(
    title="Termsheet Validation API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Mount upload router without extra prefix (endpoints at /upload/...)
app.include_router(upload_router, tags=["Upload"])

# Other routers
app.include_router(validate_router)
app.include_router(analyze_router)
app.include_router(audit_router)
# Database operations under /db
app.include_router(dbops_router, prefix="/db", tags=["Database Operations"])
# Chat endpoints under /api/chat
app.include_router(chat_router, prefix="/api", tags=["Chat"])

# Create tables from models
Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Termsheet Validation API"}

# Optional: Run FastAPI app directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
