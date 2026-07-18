
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Anonymous Smart Logistics Consolidation Platform",
    description=(
        "AI-powered blind matchmaking backend for B2B freight consolidation "
        "(COMPFEST 18 MVP)."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "smart-logistics-consolidation"}