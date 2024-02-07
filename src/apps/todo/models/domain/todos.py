from typing import Optional
from pydantic import BaseModel


class TodoItem(BaseModel):
    """ Todoitem schema """
    id: str
    title: str
    content: Optional[str]
    is_done: bool
    created_at: str  # format: %Y-%m-%d %H:%M:%S
    updated_at: str  # format: %Y-%m-%d %H:%M:%S
