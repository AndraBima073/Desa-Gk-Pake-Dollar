"""Router: /api/v1/ai — endpoint inferensi model."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.ai import AIGenerateRequest, AIGenerateResponse
from app.schemas.common import APIResponse, success
from app.services import ai_service

router = APIRouter(prefix="/ai", tags=["AI Inference"])


@router.post("/generate", response_model=APIResponse[AIGenerateResponse])
async def generate(payload: AIGenerateRequest, db: AsyncSession = Depends(get_db)):
    """POST /api/v1/ai/generate — inferensi teks dengan penegakan privasi.

    Status is_anonymous user diperiksa sebelum pemrosesan; user anonim
    diproses tanpa penyimpanan prompt maupun keterkaitan identitas.
    """
    result = await ai_service.run_generation(db, payload)
    return success(result, "Inferensi berhasil.")
