from typing import Optional
from pydantic import BaseModel

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime

from src.core.database import Base


class TodoItem(BaseModel):
    """ TodoItem schema """
    id: str
    title: str
    content: Optional[str]
    is_done: bool
    created_at: str  # format: %Y-%m-%d %H:%M:%S
    updated_at: str  # format: %Y-%m-%d %H:%M:%S


class TodoItemDB(Base):
    """ TodoItem database schema """
    __tablename__ = "todos"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    is_done = Column(Boolean, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)
    # owner_user_id = Column(String, ForeignKey("users.id"))
