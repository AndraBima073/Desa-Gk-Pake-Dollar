
import pytest

from app.core.config import get_settings


@pytest.fixture(autouse=True)
def disable_ai_shipment_parsing(monkeypatch):
    # Otherwise /consolidate hits the real Gemini API and tests get flaky.
    monkeypatch.setenv("AI_SHIPMENT_PARSING_ENABLED", "false")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
