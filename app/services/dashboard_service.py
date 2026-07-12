"""Agregasi statistik dashboard — satu round-trip DB seminimal mungkin."""
from datetime import datetime, timedelta, timezone

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import ActivityLog, AIInferenceLog, User
from app.schemas.dashboard import AIMetrics, DashboardStats


async def get_stats(db: AsyncSession) -> DashboardStats:
    """Menghitung metrik dashboard memakai agregasi SQL (bukan loop Python).

    - total_users     : COUNT seluruh user aktif
    - anonymous_users : COUNT user dengan is_anonymous = true
    - active_sessions : user unik dengan aktivitas dalam 15 menit terakhir
    - ai_metrics      : agregat inferensi 24 jam terakhir
    """
    now = datetime.now(timezone.utc)
    session_window = now - timedelta(minutes=15)
    ai_window = now - timedelta(hours=24)

    # --- Statistik user (satu query, dua agregat) ---
    user_row = (
        await db.execute(
            select(
                func.count(User.id),
                func.coalesce(
                    func.sum(case((User.is_anonymous.is_(True), 1), else_=0)), 0
                ),
            ).where(User.is_active.is_(True))
        )
    ).one()
    total_users, anonymous_users = int(user_row[0]), int(user_row[1])

    # --- Sesi aktif (user unik ber-aktivitas 15 menit terakhir) ---
    active_sessions = (
        await db.execute(
            select(func.count(func.distinct(ActivityLog.user_id))).where(
                ActivityLog.created_at >= session_window
            )
        )
    ).scalar_one()

    # --- Metrik AI (satu query, tiga agregat) ---
    ai_row = (
        await db.execute(
            select(
                func.count(AIInferenceLog.id),
                func.coalesce(func.avg(AIInferenceLog.latency_ms), 0.0),
                func.coalesce(
                    func.avg(case((AIInferenceLog.success.is_(True), 1.0), else_=0.0)),
                    0.0,
                ),
            ).where(AIInferenceLog.created_at >= ai_window)
        )
    ).one()

    return DashboardStats(
        total_users=total_users,
        active_sessions=int(active_sessions),
        anonymous_users=anonymous_users,
        ai_metrics=AIMetrics(
            total_inferences=int(ai_row[0]),
            avg_latency_ms=round(float(ai_row[1]), 2),
            success_rate=round(float(ai_row[2]) * 100, 2),
        ),
    )
