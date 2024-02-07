# pylint: disable=no-self-argument
"""
User Schema
"""
from typing import Dict

from pydantic import field_validator

from ..domain.user import User

__all__ = ["UserCreateRequest"]


class UserCreateRequest(User):
    """ Register a new account """

    plain_password: str
    repeat_plain_password: str

    # @validator("repeat_plain_password")
    @field_validator("repeat_plain_password")
    def password_match(  # type: ignore
            cls, v: str, values: Dict[str, str], **kwargs  # noqa
    ) -> str:
        """ password match """
        if "plain_password" in values and v != values["plain_password"]:
            raise ValueError("password do not match")
        return v
