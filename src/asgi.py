"""
"""
from .core.config import settings
from .core.database import Base, engine

from .main import create_app

from .route import api_router, auth_router

Base.metadata.create_all(bind=engine)
app = create_app()
app.include_router(api_router, prefix=f"{settings.API_VERSION_PREFIX}")
app.include_router(auth_router, prefix="/api/token", tags=["auth"])
