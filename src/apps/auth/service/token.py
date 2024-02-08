import jwt
import time
from typing import Optional

from ....core.config import settings
from ..model.domain.token import TokenData
from ..exceptions import token_credential_exception
from ..constants import TokenType


async def create_access_token(
        user_id: str,
        scopes: list[str],
        expires_in: int = settings.ACCESS_TOKEN_EXPIRE_SECONDS,
) -> str:
    # Create Access Token
    init_time = int(time.time())
    to_encode = {
        "user_id": user_id,
        "token_type": TokenType.BEARER,
        "scopes": scopes,
        "created_at": init_time,
    }
    expire = init_time + expires_in
    to_encode.update({"expire_at": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


async def decode_token(token: str) -> Optional[TokenData]:
    # Decode Token
    token_data = Optional[TokenData] = None

    try:
        payload = await jwt.decode(
            jwt=token,
            key=settings.PUBLIC_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        token_data = TokenData(
            user_id=payload.get("user_id"),
            token_type=payload.get("token_type"),
            scopes=payload.get("scopes"),
            created_at=payload.get("created_at"),
            expire_at=payload.get("expire_at"),
        )

    except jwt.PyJWTError as err:
        raise err
    except Exception:
        raise Exception("Could not validate credentials")
    finally:
        return token_data
