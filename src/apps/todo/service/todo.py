import uuid
from typing import Any, List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import LambdaElement, select

from src.apps.todo.models.domain.todos import TodoItem, TodoItemDB
from src.apps.todo.models.schema.todos import TodoCreateRequest, TodoUpdateRequest


def get_todo(
        db: Session,
        todo_id: str
) -> TodoItem:
    todo = db.query(TodoItemDB).filter_by(id=todo_id).first()

    return TodoItem.from_orm(todo)


def get_all(
        db: Session,
        user_id: str
) -> List[TodoItem]:
    todos = db.query(TodoItemDB).filter_by(user_id=user_id).all()

    new_todos = [TodoItem.from_orm(todo) for todo in todos]
    return new_todos


def create_todo(
        db: Session,
        user_id: str,
        todo: TodoCreateRequest,
) -> TodoItem:
    new_todo_id = get_new_todo_id()
    # Should map to the database schema
    new_todo = TodoItem(
        id=new_todo_id,
        user_id=user_id,
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

    return new_todo


def get_new_todo_id() -> str:
    return str(uuid.uuid4())


def update_todo(
        db: Session,
        todo_id: str,
        todo_update_request: TodoUpdateRequest,
) -> int:
    """ TodoItem Update  """
    result = db.query(TodoItemDB).filter_by(id=todo_id).update(todo_update_request.dict())

    db.commit()

    return True if result > 0 else False


def delete_todo(db: Session, todo_id: str) -> None:
    """ TodoItem Delete  """
    db.query(TodoItemDB).filter_by(id=todo_id).delete()
    db.commit()
