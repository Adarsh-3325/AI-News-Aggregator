from typing import Generator
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, init_db
from app.database.repository import Repository, repository

def init_app_database() -> None:
    """Initializes relational database tables and seeds starter state."""
    init_db()

def get_db_session() -> Generator[Session, None, None]:
    """Dependency helper providing SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repository() -> Repository:
    """Dependency helper providing unified Repository instance."""
    return repository
