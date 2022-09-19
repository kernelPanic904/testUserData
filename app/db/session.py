from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core.config import settings

engine = create_engine(url=settings.DB_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
