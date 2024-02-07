from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from .config import settings, sqlalchemy_settings

# print(sqlalchemy_settings.SQLALCHEMY_DATABASE_URL)
print(settings)
print(sqlalchemy_settings)

engine = create_engine(
    sqlalchemy_settings.SQLALCHEMY_DATABASE_URL.format(
        DATABASE=sqlalchemy_settings.DATABASE,
    ),
    pool_size=sqlalchemy_settings.SQLALCHEMY_POOL_SIZE,
    pool_recycle=sqlalchemy_settings.SQLALCHEMY_POOL_RECYCLE,
    pool_timeout=sqlalchemy_settings.SQLALCHEMY_POOL_TIMEOUT,
    echo=sqlalchemy_settings.SQLALCHEMY_ECHO,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database_session() -> Generator[Session, None, None]:
    """ sqlalchemy Session generator """
    session = None

    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
