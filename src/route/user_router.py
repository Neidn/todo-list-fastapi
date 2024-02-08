"""
users endpoint
"""
from fastapi import status
from fastapi.param_functions import Depends, Security
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..apps.auth.model.domain.user import User
from ..apps.auth.model.schema.user import UserCreateRequest, UserCreatedResponse
from ..apps.auth.service.user import create_user

from ..core.database import get_database_session

# from ..apps.auth.service.user import get_admin_user
from ..apps.auth.service.user import get_current_active_user

user_router = APIRouter()


# __admin = Security(get_admin_user)


@user_router.post(
    path="",
    name="Sign Up",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreatedResponse,
)
async def add_user(
        user_create_request: UserCreateRequest,
        db: Session = Depends(get_database_session),
) -> UserCreatedResponse:
    """ Add User """
    try:
        new_user: User = await create_user(
            username=user_create_request.username,
            email=user_create_request.email,
            full_name=user_create_request.full_name,
            plain_password=user_create_request.plain_password,
            db=db,
        )
        user_created_response: UserCreatedResponse = UserCreatedResponse(
            username=new_user.username,
            email=new_user.email,
            full_name=new_user.full_name,
            created_at=new_user.created_at,
        )
        return user_created_response
    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail=str(err),
        )
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=str(err),
        )
