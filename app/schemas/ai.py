"""Skema Pydantic untuk modul AI."""
from pydantic import BaseModel, Field


class AIGenerateRequest(BaseModel):
    """Payload POST /ai/generate."""

    user_id: int = Field(gt=0, description="ID user pemanggil (ganti dgn auth token di prod)")
    prompt: str = Field(min_length=1, max_length=8000)
    max_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class AIGenerateResponse(BaseModel):
    """Payload data hasil inferensi."""

    output: str
    model_name: str
    latency_ms: float
    anonymous_mode: bool
