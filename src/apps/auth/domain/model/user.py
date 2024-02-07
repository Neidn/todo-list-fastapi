from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime

from ...constants import UserPermission
from .....core.database import Base


class User(BaseModel):
    """ User Info """

    username: str
    email: Optional[str] = ""
    full_name: Optional[str] = ""
    disabled: Optional[bool] = False

    class Config:
        from_attribute = True


class UserCore(User):
    hashed_password: str
    permission: UserPermission = UserPermission.NORMAL

    class Config:
        from_attribute = True


class UserDB(Base):
    """ User DB """

    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        index=True,
        default="",
        server_default="",
        comment="User uuid",
    )
    username = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="User name",
    )
    email = Column(
        String,
        index=True,
        unique=True,
        default="",
        server_default="",
        comment="User email",
    )
    full_name = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="User full name",
    )
    hashed_password = Column(
        String,
        default="",
        server_default="",
        comment="User hashed password",
    )
    disabled = Column(
        Boolean,
        index=True,
        default=False,
        server_default="",
        comment="User disabled Status(True: disabled, False: enabled)",
    )
    permission = Column(
        Integer,
        index=True,
        default=UserPermission.NORMAL,
        server_default="",
        comment="User permission(GUEST: 0, NORMAL: 1, ADMIN: 2)",
    )