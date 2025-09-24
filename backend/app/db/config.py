# DB config for pgvector

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/mgdi"
)

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,  # TODO: Use proper pool in production
    echo=True,  # TODO: Disable in production
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


async def get_db():
    """Gets a database session.

    This is a dependency that can be used in FastAPI endpoints.
    """
    async with async_session() as session:
        yield session
