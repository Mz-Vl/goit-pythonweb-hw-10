from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import config

engine = create_async_engine(
    config.DB_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)

AsyncDBSession = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function for FastAPI endpoint-ах to Depends.
    """
    session = AsyncDBSession()
    try:
        yield session
    finally:
        await session.close()