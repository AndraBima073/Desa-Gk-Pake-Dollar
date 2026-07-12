"""Router: /api/v1/dashboard — agregasi statistik."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse, success
from app.schemas.dashboard import DashboardStats
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=APIResponse[DashboardStats])
async def get_stats(db: AsyncSession = Depends(get_db)):
    """GET /api/v1/dashboard/stats — ringkasan metrik via agregasi SQL."""
    stats = await dashboard_service.get_stats(db)
    return success(stats)
