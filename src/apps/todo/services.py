import uuid
from typing import Any, List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import LambdaElement

from .models.domain.todos import TodoItem, TodoItemDB
from .models.schema.todos import TodoCreateRequest, TodoUpdateRequest

from src.core.database import get_database_session


def get_todo(
        db: Session,
        todo_id: str
) -> TodoItem:
    query_filter = LambdaElement(TodoItemDB.id == todo_id)
    todo = db.query(TodoItemDB).filter(query_filter).first()
    return TodoItem.from_orm(todo)


async def get_all(db: Session) -> List[TodoItem]:
    todos = db.query(TodoItemDB).all()

    new_todos = [TodoItem.from_orm(todo) for todo in todos]
    return new_todos


async def create_todo(
        db: Session,
        todo: TodoCreateRequest,
) -> TodoItem:
    new_todo_id = get_new_todo_id()
    # Should map to the database schema
    new_todo = TodoItem(
        id=new_todo_id,
        owner_user_id='',
        title=todo.title,
        content=todo.content,
        is_done=todo.is_done,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    # convert TodoItem to TodoItemDB
    new_todo = TodoItemDB(**new_todo.dict())

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return TodoItem.from_orm(new_todo)


def get_new_todo_id() -> str:
    return str(uuid.uuid4())


def update_todo(
        db: Any,
        todo_id: str,
        previous_todo: TodoItem,
        todo_update_request: TodoUpdateRequest,
) -> TodoItem:
    """ TodoItem Update  """
    update_flag = False

    if previous_todo.title != todo_update_request.title:
        previous_todo.title = todo_update_request.title
        db[todo_id].title = todo_update_request.title
        update_flag = True

    if previous_todo.content != todo_update_request.content:
        previous_todo.content = todo_update_request.content
        db[todo_id].content = todo_update_request.content
        update_flag = True

    if previous_todo.is_done != todo_update_request.is_done:
        previous_todo.is_done = todo_update_request.is_done
        db[todo_id].is_done = todo_update_request.is_done
        update_flag = True

    if update_flag:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        previous_todo.updated_at = now
        db[todo_id].updated_at = now

    return previous_todo


def delete_todo(db: Any, todo_id: str) -> None:
    db.pop(todo_id, None)
    print(db)
