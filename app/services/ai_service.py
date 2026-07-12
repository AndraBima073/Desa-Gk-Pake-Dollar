"""Service inferensi AI — terpisah dari router, siap ditukar implementasinya.

Mendukung dua mode via env AI_PROVIDER:
  - "local"    : boilerplate model lokal (mis. transformers / llama-cpp / ONNX)
  - "external" : boilerplate pemanggilan API eksternal via httpx (async)

Logika privasi: status is_anonymous user diperiksa SEBELUM pemrosesan,
menentukan apa yang boleh dicatat ke database.
"""
import time
from abc import ABC, abstractmethod

import httpx
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.user import AIInferenceLog, User
from app.schemas.ai import AIGenerateRequest, AIGenerateResponse
from app.services import user_service

settings = get_settings()


class BaseAIEngine(ABC):
    """Kontrak engine AI. Implementasikan class baru untuk provider lain."""

    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Menjalankan inferensi dan mengembalikan teks hasil."""


class LocalAIEngine(BaseAIEngine):
    """Boilerplate model lokal.

    Ganti isi `generate` dengan pemanggilan model Anda, contoh:
        from transformers import pipeline
        self.pipe = pipeline("text-generation", model="...")
    Untuk model blocking (non-async), bungkus dengan
    `asyncio.to_thread(...)` agar tidak memblokir event loop.
    """

    async def generate(self, prompt: str, max_tokens: int, temperature: float) -> str:
        # --- GANTI DENGAN INFERENSI MODEL LOKAL ANDA ---
        # contoh: return await asyncio.to_thread(self._run_model, prompt)
        return f"[{settings.AI_MODEL_NAME}] Echo demo: {prompt[:200]}"


class ExternalAIEngine(BaseAIEngine):
    """Boilerplate API eksternal (OpenAI-compatible / custom) via httpx async."""

    async def generate(self, prompt: str, max_tokens: int, temperature: float) -> str:
        if not settings.AI_EXTERNAL_API_URL:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI_EXTERNAL_API_URL belum dikonfigurasi.",
            )
        headers = {"Authorization": f"Bearer {settings.AI_EXTERNAL_API_KEY}"}
        payload = {
            "model": settings.AI_MODEL_NAME,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        try:
            async with httpx.AsyncClient(timeout=settings.AI_TIMEOUT_SECONDS) as client:
                resp = await client.post(
                    settings.AI_EXTERNAL_API_URL, json=payload, headers=headers
                )
                resp.raise_for_status()
        except httpx.TimeoutException as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Provider AI eksternal timeout.",
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Provider AI mengembalikan error: {exc.response.status_code}",
            ) from exc
        body = resp.json()
        # Sesuaikan parsing dengan skema respons provider Anda:
        return body.get("output") or body.get("choices", [{}])[0].get("text", "")


def get_engine() -> BaseAIEngine:
    """Factory engine berdasarkan konfigurasi."""
    if settings.AI_PROVIDER == "external":
        return ExternalAIEngine()
    return LocalAIEngine()


async def run_generation(
    db: AsyncSession, payload: AIGenerateRequest
) -> AIGenerateResponse:
    """Alur lengkap inferensi dengan penegakan privasi.

    1. Validasi user & baca status is_anonymous (SEBELUM inferensi).
    2. Jalankan inferensi.
    3. Catat metrik: user anonim -> tanpa user_id & tanpa snapshot prompt.
    4. Log aktivitas (otomatis dilewati untuk user anonim).
    """
    user: User = await user_service.get_user_or_404(db, payload.user_id)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akun tidak aktif; inferensi ditolak.",
        )

    anonymous = user.is_anonymous  # privacy check dilakukan lebih dulu
    engine = get_engine()

    start = time.perf_counter()
    success_flag = True
    try:
        output = await engine.generate(
            payload.prompt, payload.max_tokens, payload.temperature
        )
    except HTTPException:
        success_flag = False
        raise
    finally:
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        db.add(
            AIInferenceLog(
                user_id=None if anonymous else user.id,
                model_name=settings.AI_MODEL_NAME,
                latency_ms=latency_ms,
                success=success_flag,
                prompt_snapshot=None if anonymous else payload.prompt[:1000],
            )
        )
        await db.commit()

    await user_service.log_activity(db, user, "ai_generate", f"{latency_ms} ms")

    return AIGenerateResponse(
        output=output,
        model_name=settings.AI_MODEL_NAME,
        latency_ms=latency_ms,
        anonymous_mode=anonymous,
    )
