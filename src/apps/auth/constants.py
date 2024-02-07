from enum import Enum


class UserPermission(str, Enum):
    GUEST = 0
    NORMAL = 1
    ADMIN = 2
