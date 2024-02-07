"""
users endpoint
"""
from fastapi import status
from fastapi.param_functions import Depends, Security
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from ..apps.auth.model.domain.user import User
from ..apps.auth.model.schema.user import UserCreateRequest

from ..core.database import get_database_session
from ..apps.auth.service.auth import get_admin_user

# from ..di.database import get_user_repository
# from ..repository import UserRepository
# from ..repository.mysql import UserMysqlRepository

auth_router = APIRouter()

__admin = Security(get_admin_user)


@auth_router.post(
    path="",
    name="Sign Up",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def add_user(
        user_create_request: UserCreateRequest,
        db: Session = Depends(get_database_session),
        current_user: str = __admin,
) -> User:
    """ 회원가입 """
