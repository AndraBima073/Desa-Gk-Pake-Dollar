"""Inisialisasi database async (SQLAlchemy 2.0 + asyncio)."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class untuk seluruh model ORM."""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency FastAPI: satu session per request, auto-close."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Membuat seluruh tabel saat startup (untuk dev; gunakan Alembic di prod)."""
    from app import models  # noqa: F401 — register semua model ke metadata

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
