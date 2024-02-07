from typing import List
from starlette import status
from fastapi.routing import APIRouter
from fastapi.param_functions import Depends, Path, Query

from src.apps.todo.exceptions import TodoNotFoundException

from src.apps.todo import services

from src.apps.todo.models.domain.todos import TodoItem
from src.apps.todo.models.schema.todos import TodoCreateRequest, TodoUpdateRequest

from src.apps.todo.repo.fake import todos_repo

todos_router = APIRouter()

__valid_id = Path(..., title="The ID of the todo", description="The ID of the todo", ge=1)


@todos_router.get("/", response_model=List[TodoItem], status_code=status.HTTP_200_OK)
async def get_todos() -> List[TodoItem]:
    """
    Get all TodoItems
    """
    todos = services.get_all(db=todos_repo)
    return todos


@todos_router.get("/{todo_id}", response_model=TodoItem, status_code=status.HTTP_200_OK)
async def get_todo(
        todo_id: str = __valid_id,
) -> TodoItem:
    """
    Get a TodoItem
    """
    todo = services.get_todo(db=todos_repo, todo_id=todo_id)
    if todo is None:
        raise TodoNotFoundException
    return todo


@todos_router.post("/", response_model=TodoItem, status_code=status.HTTP_201_CREATED)
async def create_todo(
        todo: TodoCreateRequest,
) -> TodoItem:
    """
    Create a TodoItem
    """
    return services.create_todo(db=todos_repo, todo=todo)


@todos_router.put("/{todo_id}", response_model=TodoItem, status_code=status.HTTP_200_OK)
async def update_todo(
        todo_update: TodoUpdateRequest,
        todo_id: str = __valid_id,
) -> TodoItem:
    """
    Update a TodoItem
    """
    todo = services.get_todo(
        db=todos_repo,
        todo_id=todo_id,
    )

    if todo is None:
        raise TodoNotFoundException

    todo = services.update_todo(
        db=todos_repo,
        todo_id=todo_id,
        previous_todo=todo,
        todo_update_request=todo_update,
    )
    return todo


@todos_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        todo_id: str = __valid_id,
) -> None:
    """
    Delete a TodoItem
    """
    todo = services.get_todo(
        db=todos_repo,
        todo_id=todo_id,
    )

    if todo is None:
        raise TodoNotFoundException

    services.delete_todo(
        db=todos_repo,
        todo_id=todo_id,
    )
    return None
