import uuid
from typing import Any, List, Optional
from datetime import datetime

from .models.domain.todos import TodoItem
from .models.schema.todos import TodoCreateRequest, TodoUpdateRequest


def get_todo(db: Any, todo_id: str) -> Optional[TodoItem]:
    todo: Optional[TodoItem] = db.get(todo_id, None)
    return todo


def get_all(db: Any) -> List[TodoItem]:
    todos = [TodoItem(**todo.dict()) for todo in db.values()]
    return todos


def create_todo(db: Any, todo: TodoCreateRequest) -> TodoItem:
    next_todo_id = get_new_todo_id()
    new_todo = TodoItem(
        id=next_todo_id,
        title=todo.title,
        content=todo.content,
        is_done=todo.is_done,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    db[next_todo_id] = new_todo
    return new_todo


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
