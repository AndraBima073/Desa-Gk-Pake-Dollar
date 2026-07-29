
from __future__ import annotations

from fastapi import APIRouter

from app.database import MOCK_CONTAINER_DB, ROUTE_ETA_DAYS
from app.schemas.cargo import AvailableRoute

router = APIRouter()


@router.get("/routes", response_model=list[AvailableRoute])
async def list_available_routes() -> list[AvailableRoute]:
    routes = []
    for slot in MOCK_CONTAINER_DB:
        eta_min, eta_max = ROUTE_ETA_DAYS.get((slot.origin, slot.destination), (None, None))
        routes.append(
            AvailableRoute(
                origin=slot.origin,
                destination=slot.destination,
                date=slot.date,
                available_volume_m3=round(slot.max_volume_m3 - slot.existing_volume_m3, 2),
                available_weight_tons=round(slot.max_weight_tons - slot.existing_weight_tons, 2),
                space_utilization_percent=round(
                    (slot.existing_volume_m3 / slot.max_volume_m3) * 100, 2
                ),
                eta_min_days=eta_min,
                eta_max_days=eta_max,
            )
        )
    return routes
