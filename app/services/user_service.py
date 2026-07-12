"""Logika bisnis: manajemen user, toggle anonim, dan masking data sensitif."""
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import ActivityLog, User
from app.schemas.user import UserCreate

MASKED_NAME = "Guest"


def mask_user(user: User) -> dict:
    """Mengembalikan dict user; field sensitif dimasking jika mode anonim aktif.

    Model ORM TIDAK dimutasi — masking hanya pada lapisan presentasi.
    """
    if not user.is_anonymous:
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_anonymous": user.is_anonymous,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }
    return {
        "id": user.id,
        "username": MASKED_NAME,
        "email": "hidden@anonymous.local",
        "full_name": MASKED_NAME,
        "is_anonymous": True,
        "is_active": user.is_active,
        "created_at": user.created_at,
    }


async def get_user_or_404(db: AsyncSession, user_id: int) -> User:
    """Mengambil user berdasarkan ID; raise 404 jika tidak ditemukan."""
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User dengan id={user_id} tidak ditemukan.",
        )
    return user


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    """Membuat user baru; raise 409 jika username/email sudah terdaftar."""
    user = User(**payload.model_dump())
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username atau email sudah terdaftar.",
        ) from exc
    await db.refresh(user)
    return user


async def set_privacy_mode(db: AsyncSession, user_id: int, is_anonymous: bool) -> User:
    """Mengubah status mode anonim user (PATCH /user/privacy)."""
    user = await get_user_or_404(db, user_id)
    user.is_anonymous = is_anonymous
    await db.commit()
    await db.refresh(user)
    return user


async def log_activity(
    db: AsyncSession, user: User, action: str, detail: str | None = None
) -> None:
    """Menyimpan log aktivitas — DILEWATI sepenuhnya jika user anonim.

    Ini adalah titik penegakan privasi (privacy enforcement point):
    seluruh service lain wajib memanggil fungsi ini, bukan menulis
    ActivityLog secara langsung.
    """
    if user.is_anonymous:
        return  # Kepatuhan privasi: tidak ada jejak aktivitas yang disimpan.
    db.add(ActivityLog(user_id=user.id, action=action, detail=detail))
    await db.commit()


async def list_users(db: AsyncSession, limit: int = 50, offset: int = 0) -> list[User]:
    """Mengambil daftar user dengan paginasi sederhana."""
    result = await db.execute(select(User).order_by(User.id).limit(limit).offset(offset))
    return list(result.scalars().all())
