from typing import List
from starlette import status
from fastapi.routing import APIRouter
from fastapi.param_functions import Depends, Path, Security

from sqlalchemy.orm import Session

from ..apps.todo.service import todo as services
from ..apps.todo.exceptions import TodoNotFoundException
from ..apps.todo.models.domain.todos import TodoItem
from ..apps.todo.models.schema.todos import *

from ..core.database import get_database_session

from ..apps.auth.service.user import get_current_active_user, get_current_user
from ..apps.auth.model.domain.user import User

from .. import check_uuid

todos_router = APIRouter()

# UUid
__valid_id = Path(
    ...,
    title="Todo ID",
    description="The ID of the TodoItem",
)

__current_active_user = Depends(get_current_active_user)
__creatable_user = Security(get_current_active_user, scopes=["TODOS/POST"])
__readable_user = Security(get_current_active_user, scopes=["TODOS/GET"])
__updatable_user = Security(get_current_active_user, scopes=["TODOS/PUT/{todo_id}"])
__deletable_user = Security(get_current_active_user, scopes=["TODOS/DELETE/{todo_id}"])


@todos_router.get(
    "/",
    response_model=List[TodoGetResponse],
    status_code=status.HTTP_200_OK
)
async def get_todos(
        db: Session = Depends(get_database_session),
        current_user: User = __readable_user,
) -> List[TodoGetResponse]:
    """
    Get all TodoItems
    """
    todos = services.get_all(
        db=db,
        user_id=current_user.id,
    )
    response = [TodoGetResponse(
        id=todo.id,
        title=todo.title,
        content=todo.content,
        is_done=todo.is_done,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    ) for todo in todos]

    return response


@todos_router.get(
    "/done",
    response_model=List[TodoGetResponse],
    status_code=status.HTTP_200_OK
)
async def get_done_todos(
        db: Session = Depends(get_database_session),
        current_user: User = __readable_user,
) -> List[TodoGetResponse]:
    """
    Get all done TodoItems
    """
    todos = services.get_done_all(
        db=db,
        user_id=current_user.id,
    )
    response = [TodoGetResponse(
        id=todo.id,
        title=todo.title,
        content=todo.content,
        is_done=todo.is_done,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    ) for todo in todos]

    return response


@todos_router.get(
    "/undone",
    response_model=List[TodoGetResponse],
    status_code=status.HTTP_200_OK
)
async def get_undone_todos(
        db: Session = Depends(get_database_session),
        current_user: User = __readable_user,
) -> List[TodoGetResponse]:
    """
    Get all not done TodoItems
    """
    todos = services.get_undone_all(
        db=db,
        user_id=current_user.id,
    )
    response = [TodoGetResponse(
        id=todo.id,
        title=todo.title,
        content=todo.content,
        is_done=todo.is_done,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    ) for todo in todos]

    return response


@todos_router.get(
    "/{todo_id}",
    response_model=TodoGetResponse,
    status_code=status.HTTP_200_OK
)
async def get_todo(
        todo_id: str = __valid_id,
        current_user: User = __readable_user,
        db: Session = Depends(get_database_session),
) -> TodoGetResponse:
    """
    Get a TodoItem
    """
    if not check_uuid(todo_id):
        raise TodoNotFoundException

    todo = services.get_todo(
        db=db,
        user_id=current_user.id,
        todo_id=todo_id
    )
    if todo is None:
        raise TodoNotFoundException

    response = TodoGetResponse(
        id=todo.id,
        title=todo.title,
        content=todo.content,
        is_done=todo.is_done,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )
    return response


@todos_router.post(
    "/",
    response_model=TodoGetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
        todo: TodoCreateRequest,
        current_user: User = __creatable_user,
        db: Session = Depends(get_database_session),
) -> TodoGetResponse:
    """
    Create a TodoItem
    """
    new_todo = services.create_todo(
        db=db,
        user_id=current_user.id,
        todo=todo,
    )

    response = TodoGetResponse(
        id=new_todo.id,
        title=new_todo.title,
        content=new_todo.content,
        is_done=new_todo.is_done,
        created_at=new_todo.created_at,
        updated_at=new_todo.updated_at,
    )

    return response


@todos_router.put(
    "/{todo_id}",
    response_model=TodoGetResponse,
    status_code=status.HTTP_200_OK
)
async def update_todo(
        todo_update: TodoUpdateRequest,
        todo_id: str = __valid_id,
        current_user: User = __updatable_user,
        db: Session = Depends(get_database_session),
) -> TodoGetResponse:
    """
    Update a TodoItem
    """
    if not check_uuid(todo_id):
        raise TodoNotFoundException

    todo = services.get_todo(
        db=db,
        user_id=current_user.id,
        todo_id=todo_id,
    )

    if todo is None:
        raise TodoNotFoundException

    result = services.update_todo(
        db=db,
        user_id=current_user.id,
        todo_id=todo_id,
        todo_update_request=todo_update,
    )

    if result < 1:
        raise TodoNotFoundException

    todo = services.get_todo(
        db=db,
        user_id=current_user.id,
        todo_id=todo_id,
    )

    return TodoGetResponse(
        id=todo.id,
        title=todo.title,
        content=todo.content,
        is_done=todo.is_done,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )


@todos_router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_todo(
        todo_id: str,
        current_user: User = __deletable_user,
        db: Session = Depends(get_database_session),
) -> None:
    """
    Delete a TodoItem
    """
    if not check_uuid(todo_id):
        raise TodoNotFoundException

    todo = services.get_todo(
        db=db,
        todo_id=todo_id,
        user_id=current_user.id,
    )

    if todo is None:
        raise TodoNotFoundException

    services.delete_todo(
        db=db,
        todo_id=todo_id,
        user_id=current_user.id,
    )
    return None
