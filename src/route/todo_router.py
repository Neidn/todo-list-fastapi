from typing import List, Any, Coroutine
from starlette import status
from fastapi.routing import APIRouter
from fastapi.param_functions import Depends, Path, Query

from sqlalchemy.orm import Session

from src.apps.todo.exceptions import TodoNotFoundException

from src.apps.todo import services

from src.apps.todo.models.domain.todos import TodoItem
from src.apps.todo.models.schema.todos import TodoCreateRequest, TodoUpdateRequest

todos_router = APIRouter()

# UUid
__valid_id = Path(
    ...,
    title="Todo ID",
    description="The ID of the TodoItem",
    regex="^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$",
)


@todos_router.get("/", response_model=List[TodoItem], status_code=status.HTTP_200_OK)
async def get_todos(
        db: Session = Depends(services.get_database_session),
) -> List[TodoItem]:
    """
    Get all TodoItems
    """
    todos = services.get_all(db=db)
    return todos


@todos_router.get("/{todo_id}", response_model=TodoItem, status_code=status.HTTP_200_OK)
async def get_todo(
        todo_id: str = __valid_id,
        db: Session = Depends(services.get_database_session),
) -> TodoItem:
    """
    Get a TodoItem
    """
    todo = services.get_todo(db=db, todo_id=todo_id)
    if todo is None:
        raise TodoNotFoundException
    return todo


@todos_router.post("/", response_model=TodoItem, status_code=status.HTTP_201_CREATED)
async def create_todo(
        todo: TodoCreateRequest,
        db: Session = Depends(services.get_database_session),
) -> TodoItem:
    """
    Create a TodoItem
    """
    new_todo = services.create_todo(
        db=db,
        todo=todo,
    )

    return new_todo


@todos_router.put("/{todo_id}", response_model=TodoItem, status_code=status.HTTP_200_OK)
async def update_todo(
        todo_update: TodoUpdateRequest,
        todo_id: str = __valid_id,
        db: Session = Depends(services.get_database_session),
) -> TodoItem:
    """
    Update a TodoItem
    """
    todo = services.get_todo(
        db=db,
        todo_id=todo_id,
    )

    if todo is None:
        raise TodoNotFoundException

    result = services.update_todo(
        db=db,
        todo_id=todo_id,
        todo_update_request=todo_update,
    )
    if not result:
        raise TodoNotFoundException

    return todo


@todos_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        todo_id: str = __valid_id,
        db: Session = Depends(services.get_database_session),
) -> None:
    """
    Delete a TodoItem
    """
    todo = services.get_todo(
        db=db,
        todo_id=todo_id,
    )

    if todo is None:
        raise TodoNotFoundException

    services.delete_todo(
        db=db,
        todo_id=todo_id,
    )
    return None
