import time
from typing import Iterable, List, Optional

# import jwt
from fastapi.param_functions import Depends, Security
from fastapi.security.oauth2 import OAuth2PasswordBearer, SecurityScopes

from sqlalchemy.orm import Session

from .user import get_current_user

from ....core.database import get_database_session
from ..model.domain.user import User
from ..constants import UserPermission, SupportScopes
from ..exceptions import *

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes=SupportScopes,
)


def __build_credential_exception(scope: str) -> Exception:
    msg = f"Bearer token required for {scope}" if scope else "Bearer token required"
    return UserCredentialException({
        "www-authenticate": msg
    })


def get_admin_user(current_user: User = Security(get_current_user)) -> bool:
    return current_user.permission == UserPermission.ADMIN
