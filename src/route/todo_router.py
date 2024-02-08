from typing import List
from starlette import status
from fastapi.routing import APIRouter
from fastapi.param_functions import Depends, Path, Security

from sqlalchemy.orm import Session

from ..apps.todo.service import todo as services
from ..apps.todo.exceptions import TodoNotFoundException
from ..apps.todo.models.domain.todos import TodoItem
from ..apps.todo.models.schema.todos import TodoCreateRequest, TodoUpdateRequest

from ..core.database import get_database_session

from ..apps.auth.service.user import get_current_active_user, get_current_user
from ..apps.auth.model.domain.user import User

todos_router = APIRouter()

# UUid
__valid_id = Path(
    ...,
    title="Todo ID",
    description="The ID of the TodoItem",
    regex="^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$",
)

__current_active_user = Depends(get_current_active_user)
__creatable_user = Security(get_current_active_user, scopes=["TODOS/POST"])
__readable_user = Security(get_current_active_user, scopes=["TODOS/GET"])
__updatable_user = Security(get_current_active_user, scopes=["TODOS/PATCH"])
__deletable_user = Security(get_current_active_user, scopes=["TODOS/DELETE"])


@todos_router.get(
    "/",
    response_model=List[TodoItem],
    status_code=status.HTTP_200_OK
)
async def get_todos(
        db: Session = Depends(get_database_session),
        current_user: User = __readable_user,
) -> List[TodoItem]:
    """
    Get all TodoItems
    """
    todos = services.get_all(
        db=db,
        user_id=current_user.id,
    )
    return todos


@todos_router.get("/{todo_id}", response_model=TodoItem, status_code=status.HTTP_200_OK)
async def get_todo(
        todo_id: str = __valid_id,
        db: Session = Depends(get_database_session),
) -> TodoItem:
    """
    Get a TodoItem
    """
    todo = services.get_todo(db=db, todo_id=todo_id)
    if todo is None:
        raise TodoNotFoundException
    return todo


@todos_router.post(
    "/",
    response_model=TodoItem,
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
        todo: TodoCreateRequest,
        current_user: User = __creatable_user,
        db: Session = Depends(get_database_session),
) -> TodoItem:
    """
    Create a TodoItem
    """
    new_todo = services.create_todo(
        db=db,
        user_id=current_user.id,
        todo=todo,
    )

    return new_todo


@todos_router.put("/{todo_id}", response_model=TodoItem, status_code=status.HTTP_200_OK)
async def update_todo(
        todo_update: TodoUpdateRequest,
        todo_id: str = __valid_id,
        db: Session = Depends(get_database_session),
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
        db: Session = Depends(get_database_session),
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
