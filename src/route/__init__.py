"""
routes
"""
from fastapi.routing import APIRouter

from .health_router import health_router
from .todo_router import todos_router
from .user_router import user_router
from .token_router import token_router

__all__ = ["api_router", "health_router", "todos_router", "user_router", "token_router"]

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["manage"])
api_router.include_router(todos_router, prefix="/todos", tags=["todos"])
api_router.include_router(user_router, prefix="/user", tags=["auth"])
api_router.include_router(token_router, prefix="/token", tags=["auth"])
