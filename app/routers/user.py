"""Router: /api/v1/user — manajemen pengguna & privacy toggle."""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse, success
from app.schemas.user import PrivacyUpdate, UserCreate, UserPublic
from app.services import user_service

router = APIRouter(prefix="/user", tags=["User & Privacy"])


@router.post(
    "",
    response_model=APIResponse[UserPublic],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    """Registrasi user baru (default is_anonymous = false)."""
    user = await user_service.create_user(db, payload)
    return success(user_service.mask_user(user), "User berhasil dibuat.")


@router.get("", response_model=APIResponse[list[UserPublic]])
async def list_users(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """Daftar user; data user anonim otomatis dimasking."""
    users = await user_service.list_users(db, limit, offset)
    return success([user_service.mask_user(u) for u in users])


@router.get("/{user_id}", response_model=APIResponse[UserPublic])
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Detail satu user (dimasking bila mode anonim aktif)."""
    user = await user_service.get_user_or_404(db, user_id)
    return success(user_service.mask_user(user))


@router.patch("/privacy", response_model=APIResponse[UserPublic])
async def update_privacy(
    payload: PrivacyUpdate,
    user_id: int = Query(gt=0, description="Ganti dengan user dari auth token di prod"),
    db: AsyncSession = Depends(get_db),
):
    """PATCH /api/v1/user/privacy — toggle mode anonim.

    Contoh fetch dari frontend:
        fetch("/api/v1/user/privacy?user_id=1", {
            method: "PATCH",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ is_anonymous: true }),
        })
    """
    user = await user_service.set_privacy_mode(db, user_id, payload.is_anonymous)
    mode = "diaktifkan" if user.is_anonymous else "dinonaktifkan"
    return success(user_service.mask_user(user), f"Mode anonim {mode}.")
