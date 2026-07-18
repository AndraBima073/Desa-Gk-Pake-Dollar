"""Shared contract for shipment-intelligence backends — the component that
turns a free-text shipment request into a validated `AIParsedResult`. The
active backend is `app.services.ml_service.MLShipmentIntelligenceService`;
the legacy Gemini backend (`app.services.ai_service`) satisfies the same
shape but is no longer wired into the API. The endpoint layer only depends
on this module, never on a specific backend's implementation.
"""
from __future__ import annotations

from typing import Protocol

from app.schemas.cargo import AIParsedResult


class ShipmentIntelligenceError(Exception):
    """Raised for any failure while parsing/evaluating a shipment request."""


class NoLogisticsDataFoundError(ShipmentIntelligenceError):
    """Raised when the input text contains no coherent logistics data."""


class ShipmentIntelligenceService(Protocol):
    async def parse_and_evaluate(self, raw_text: str) -> AIParsedResult: ...
