"""Registrasi seluruh model ORM agar terdaftar di metadata Base."""
from app.models.user import ActivityLog, AIInferenceLog, User

__all__ = ["User", "ActivityLog", "AIInferenceLog"]
