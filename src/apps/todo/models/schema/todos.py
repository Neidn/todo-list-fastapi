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


class TodoCreateSuccessResponse(BaseModel):
    """ TodoItem Create response schema """
    title: str
    content: Optional[str]
    created_at: str


class TodoGetResponse(BaseModel):
    """ TodoItem Get response schema """
    id: str
    title: str
    content: Optional[str]
    is_done: bool
    created_at: str
    updated_at: str
