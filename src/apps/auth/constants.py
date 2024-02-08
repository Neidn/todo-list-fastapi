from enum import Enum
from fastapi.security.oauth2 import OAuth2PasswordBearer


class UserPermission(str, Enum):
    GUEST = 0
    NORMAL = 1
    ADMIN = 2


class TokenType(str, Enum):
    BEARER: str = "Bearer"


SupportScopes = {
    "TODOS/POST": "Create a TodoItem",
    "TODOS/GET/": "Get all TodoItem",
    "TODOS/GET/{todo_id}": "Get a TodoItem",
    "TODOS/PUT/{todo_id}": "Update a TodoItem",
    "TODOS/DELETE/{todo_id}": "Delete a TodoItem",
}

Oauth2Scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes=SupportScopes,
)
