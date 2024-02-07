import time
from typing import Iterable, List, Optional

# import jwt
from fastapi.param_functions import Depends, Security
from fastapi.security.oauth2 import OAuth2PasswordBearer, SecurityScopes

from sqlalchemy.orm import Session

from ....core.database import get_database_session
from ..model.domain.user import User
from ..constants import UserPermission, SupportScopes
from ..exceptions import *
from .auth import oauth2_scheme, credential_exception


async def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_database_session),
) -> User:
    # Check Current User
    credentials_exception = credential_exception(security_scopes.scope_str)
