from pydantic import BaseModel

from ...constants import TokenType


class TokenResponse(BaseModel):
    """ Token Response """

    access_token: str
    token_type: TokenType
