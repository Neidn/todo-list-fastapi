"""
routes
"""
from fastapi.routing import APIRouter

from .health_router import health_router
from .todo_router import todos_router
from .auth_router import auth_router

__all__ = ["api_router", "health_router", "todos_router", "auth_router"]

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["manage"])
api_router.include_router(todos_router, prefix="/todos", tags=["todos"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
