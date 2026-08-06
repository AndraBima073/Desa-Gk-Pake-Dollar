import asyncio

import pytest

from app.core.config import get_settings
from app.services import ai_service
from app.services.hybrid_service import HybridShipmentIntelligenceService


@pytest.fixture(autouse=True)
def enable_ai_for_this_module(monkeypatch):
    """This module tests the AI branch itself, so it needs the opposite of
    the suite-wide conftest fixture that disables it."""
    monkeypatch.setenv("AI_SHIPMENT_PARSING_ENABLED", "true")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_falls_back_to_ml_pipeline_when_gemini_unavailable(monkeypatch):
    async def _boom(raw_text: str):
        raise ai_service.AIServiceError("simulated Gemini outage")

    monkeypatch.setattr(ai_service.AIService, "parse_and_evaluate", staticmethod(_boom))

    result = asyncio.run(
        HybridShipmentIntelligenceService.parse_and_evaluate(
            "Halo, saya mau kirim tekstil 8 m3 berat 5 ton dari Jakarta ke Surabaya tanggal 20 Juli 2026."
        )
    )

    assert result.origin == "Jakarta"
    assert result.destination == "Surabaya"
    assert result.is_safe_to_consolidate is True


def test_skips_ai_entirely_when_disabled(monkeypatch):
    monkeypatch.setenv("AI_SHIPMENT_PARSING_ENABLED", "false")
    get_settings.cache_clear()

    called = False

    async def _should_not_be_called(raw_text: str):
        nonlocal called
        called = True
        raise AssertionError("AIService must not be called when the flag is disabled")

    monkeypatch.setattr(ai_service.AIService, "parse_and_evaluate", staticmethod(_should_not_be_called))

    result = asyncio.run(
        HybridShipmentIntelligenceService.parse_and_evaluate(
            "Halo, saya mau kirim tekstil 8 m3 berat 5 ton dari Jakarta ke Surabaya tanggal 20 Juli 2026."
        )
    )

    assert called is False
    assert result.origin == "Jakarta"
