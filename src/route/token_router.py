from typing import Any, Dict

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from starlette import status

from sqlalchemy.orm import Session

from ..apps.auth.model.schema.token import TokenResponse
from ..apps.auth.service.auth import authenticate_user
from ..apps.auth.service.token import create_access_token
from ..apps.auth.constants import TokenType
from ..core.database import get_database_session
from ..apps.auth.constants import SupportScopes

token_router = APIRouter()


@token_router.post(
    path="",
    name="Sign In",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
)
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_database_session),
) -> TokenResponse:
    try:
        user = await authenticate_user(
            db=db,
            email=form_data.username,
            password=form_data.password,
        )

        token = await create_access_token(
            user_id=user.id,
            scopes=form_data.scopes,
        )

        if not token:
            raise ValueError("Invalid token")

        token_response = TokenResponse(
            access_token=token,
            token_type=TokenType.BEARER,
        )

        return token_response
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
