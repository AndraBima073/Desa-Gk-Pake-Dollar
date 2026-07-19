
from __future__ import annotations

from typing import Protocol

from app.schemas.cargo import AIParsedResult


class ShipmentIntelligenceError(Exception):
    """Raised for any failure while parsing/evaluating a shipment request."""


class NoLogisticsDataFoundError(ShipmentIntelligenceError):
    """Raised when the input text contains no coherent logistics data."""


class ShipmentIntelligenceService(Protocol):
    async def parse_and_evaluate(self, raw_text: str) -> AIParsedResult: ...
