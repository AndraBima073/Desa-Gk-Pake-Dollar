"""Aggregates all v1 resource routers. Carries no prefix of its own — the
`/api/v1` prefix is applied once, centrally, in `app.main`."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints.cargo import router as cargo_router
from app.api.v1.endpoints.routes import router as routes_router

api_router = APIRouter()
api_router.include_router(cargo_router, tags=["Consolidation"])
api_router.include_router(routes_router, tags=["Routes"])
