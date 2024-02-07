from enum import Enum


class UserPermission(str, Enum):
    GUEST = 0
    NORMAL = 1
    ADMIN = 2


SupportScopes = {
    "TODOS/POST": "Create a TodoItem",
    "TODOS/GET/{todo_id}": "Get a TodoItem",
    "TODOS/PUT/{todo_id}": "Update a TodoItem",
    "TODOS/DELETE/{todo_id}": "Delete a TodoItem",
}
