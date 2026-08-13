
from __future__ import annotations

import logging

from app.core.config import get_settings
from app.schemas.cargo import AIParsedResult, ConfirmedShipmentData
from app.services.ai_service import AIService, AIServiceError
from app.services.base import NoLogisticsDataFoundError
from app.services.ml_service import MLShipmentIntelligenceService

logger = logging.getLogger(__name__)


class HybridShipmentIntelligenceService:
    @staticmethod
    async def parse_and_evaluate(raw_text: str) -> AIParsedResult:
        settings = get_settings()
        if settings.AI_SHIPMENT_PARSING_ENABLED:
            try:
                return await AIService.parse_and_evaluate(raw_text)
            except NoLogisticsDataFoundError:
                raise
            except AIServiceError:
                logger.warning("Gemini gagal, fallback ke pipeline ML.", exc_info=True)

        return await MLShipmentIntelligenceService.parse_and_evaluate(raw_text)

    @staticmethod
    async def evaluate_confirmed(data: ConfirmedShipmentData) -> AIParsedResult:
        settings = get_settings()
        if settings.AI_SHIPMENT_PARSING_ENABLED:
            try:
                return await AIService.evaluate_confirmed(data)
            except AIServiceError:
                logger.warning("Gemini gagal, fallback ke pipeline ML.", exc_info=True)

        return await MLShipmentIntelligenceService.evaluate_confirmed(data)
