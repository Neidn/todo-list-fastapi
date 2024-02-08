# pylint: disable=no-self-argument
"""
configuration
"""
import os
from typing import List, Union

from pydantic import HttpUrl, field_validator
from pydantic_settings import BaseSettings


class SQLAlchemySettings(BaseSettings):
    # USER: str
    # PASSWORD: str
    # ROOT_PASSWORD: str
    # HOST: str
    DATABASE: str = "todo"

    SQLALCHEMY_POOL_SIZE: int = 5
    SQLALCHEMY_POOL_TIMEOUT: int = 10
    SQLALCHEMY_POOL_RECYCLE: int = 3600
    SQLALCHEMY_ECHO: bool = False
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///{DATABASE}.db"

    class Config:
        """ additional setting for SQLAlchemySettings """
        env_file = "../../.env"


class Settings(BaseSettings):
    """
    application settings
    """

    API_VERSION_PREFIX: str = "/api/v1"
    PRIVATE_KEY_PATH: str = "private_key.pem"
    PUBLIC_KEY_PATH: str = "public_key.pem"
    PRIVATE_KEY: str = ''
    PUBLIC_KEY: str = ''
    JWT_ALGORITHM: str = "RS256"

    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600
    USER_REPOSITORY_PATH: str = ""

    CORS_ALLOWS: List[HttpUrl] = []

    # @validator("CORS_ALLOWS", pre=True)
    @field_validator("CORS_ALLOWS")
    def __set_cors_allows(cls, v: Union[str, List[str]]) -> List[str]:  # noqa
        if isinstance(v, str) and not v.startswith("["):
            result = [i.strip() for i in v.split(",")]
        elif isinstance(v, List):
            result = v
        else:
            raise ValueError(v)
        return result

    '''
    # @validator("PRIVATE_KEY", pre=True)
    @field_validator("PRIVATE_KEY")
    def __set_private_key(cls, path: str) -> str:  # noqa
        private_key = open(path).read()
        return private_key

    # @validator("PUBLIC_KEY", pre=True)
    @field_validator("PUBLIC_KEY")
    def __set_public_key(cls, path: str) -> str:  # noqa
        public_key = open(path).read()
        return public_key
    '''

    class Config:
        """ additional setting for Settings """
        env_file = "../../.env"


class LoadSettings:
    """
    load settings
    """

    def __init__(self):
        self.settings = None
        self.sqlalchemy_settings = None

    def __call__(self):
        try:
            self.settings = Settings()
            self.sqlalchemy_settings = SQLAlchemySettings()
        except Exception as e:
            print(e)
        return self.settings, self.sqlalchemy_settings


settings, sqlalchemy_settings = LoadSettings()()
