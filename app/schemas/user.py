"""Skema Pydantic untuk modul User & Privacy."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Payload pembuatan user baru."""

    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=120)


class PrivacyUpdate(BaseModel):
    """Payload PATCH /user/privacy — toggle mode anonim."""

    is_anonymous: bool


class UserPublic(BaseModel):
    """Representasi user yang dikirim ke frontend.

    Jika is_anonymous=True, field sensitif SUDAH dimasking oleh service
    sebelum serialisasi (nama menjadi "Guest", email disamarkan).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    full_name: str | None
    is_anonymous: bool
    is_active: bool
    created_at: datetime
