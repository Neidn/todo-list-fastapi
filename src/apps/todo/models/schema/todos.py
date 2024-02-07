from typing import Optional
from pydantic import BaseModel


class TodoCreateRequest(BaseModel):
    """ TodoItem Create request schema """
    title: str
    content: Optional[str]
    is_done: bool = False


class TodoUpdateRequest(BaseModel):
    """ TodoItem Update request schema """
    title: Optional[str]
    content: Optional[str]
    is_done: Optional[bool]
