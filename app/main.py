
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as consolidation_router

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(consolidation_router)


@app.get("/", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "smart-logistics-consolidation"}