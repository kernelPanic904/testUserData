from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base
from app.utils import create_user_id


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    phone_number = Column(String(12), unique=True, nullable=False)
    email = Column(String, nullable=True)
    country = Column(String(50), nullable=False)

    # TODO: rework create_user_id func to create unique
    user_id = Column(String(12), default=create_user_id, unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
