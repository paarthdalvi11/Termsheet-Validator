from app.database import SessionLocal

def get_db():
    """
    Dependency to get a database session.
    This will be used with FastAPI's Depends().
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()