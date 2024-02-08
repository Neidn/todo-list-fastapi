from typing import Optional
from pydantic import BaseModel

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime

from .....core.database import Base

TABLE_NAME = "todos"


class TodoItem(BaseModel):
    """ TodoItem schema """
    id: str
    title: str
    content: str
    is_done: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class TodoItemDB(Base):
    """ TodoItem database schema """
    __tablename__ = TABLE_NAME

    id = Column(
        String,
        primary_key=True,
        index=True,
        default="",
        server_default="",
        comment="TodoItem uuid",
    )
    title = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="TodoItem title",
    )
    content = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="TodoItem content",
    )
    is_done = Column(
        Boolean,
        index=True,
        default=False,
        server_default="",
        comment="TodoItem is done or not(True: done, False: not done)",
    )
    created_at = Column(String, index=True)  # format: %Y-%m-%d %H:%M:%S
    updated_at = Column(String, index=True)  # format: %Y-%m-%d %H:%M:%S
