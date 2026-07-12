"""Skema Pydantic untuk modul Dashboard."""
from pydantic import BaseModel


class AIMetrics(BaseModel):
    """Ringkasan performa AI (agregat 24 jam terakhir)."""

    total_inferences: int
    success_rate: float
    avg_latency_ms: float


class DashboardStats(BaseModel):
    """Payload GET /dashboard/stats."""

    total_users: int
    active_sessions: int
    anonymous_users: int
    ai_metrics: AIMetrics
