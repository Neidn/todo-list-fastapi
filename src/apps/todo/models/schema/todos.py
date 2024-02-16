from typing import Optional
from pydantic import BaseModel


class TodoCreateRequest(BaseModel):
    """ TodoItem Create request schema """
    title: str
    content: Optional[str] = None
    is_done: Optional[bool] = False


class TodoUpdateRequest(BaseModel):
    """ TodoItem Update request schema """
    title: Optional[str] = None
    content: Optional[str] = None
    is_done: Optional[bool] = False


class TodoCreateSuccessResponse(BaseModel):
    """ TodoItem Create response schema """
    title: str
    content: Optional[str] = None
    created_at: str


class TodoGetResponse(BaseModel):
    """ TodoItem Get response schema """
    id: str
    title: str
    content: Optional[str] = None
    is_done: bool
    created_at: str
    updated_at: str
