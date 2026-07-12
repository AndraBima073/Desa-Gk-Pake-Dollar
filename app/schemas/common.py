"""Envelope JSON standar: seluruh endpoint mengembalikan format konsisten.

Format:
    { "status": "success" | "error", "message": str, "data": <payload|null> }
"""
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Wrapper respons generik untuk konsistensi konsumsi frontend."""

    status: str = "success"
    message: str = "OK"
    data: T | None = None


def success(data: T | None = None, message: str = "OK") -> dict:
    """Helper cepat untuk membangun respons sukses."""
    return {"status": "success", "message": message, "data": data}
