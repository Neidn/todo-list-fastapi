"""
routes
"""
from fastapi.routing import APIRouter

from .health import health as health_router
from ..apps.todo.router import todos_router

# from ..apps.auth.routes.tokens import token as token_router
# from ..apps.auth.routes.users import user as user_router

# __all__ = ["api_router", "health_router", "todos_router", "token_router"]
__all__ = ["api_router", "health_router", "todos_router"]

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["manage"])
api_router.include_router(todos_router, prefix="/todos", tags=["todos"])
# api_router.include_router(user_router, prefix="/users", tags=["auth"])
