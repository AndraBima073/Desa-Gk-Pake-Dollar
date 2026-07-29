
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import ValidationError

from app.database import MOCK_CONTAINER_DB
from app.ml import extraction
from app.ml.pricing import calculate_savings
from app.schemas.cargo import (
    AIParsedResult,
    ConfirmedShipmentData,
    ConsolidateResponse,
    ConsolidationRequest,
    ExtractedShipmentData,
    ExtractionPreview,
    PricingRecommendation,
)
from app.services.base import NoLogisticsDataFoundError, ShipmentIntelligenceError
from app.services.ml_service import MLShipmentIntelligenceService
from app.services.optimization_service import OptimizationService

router = APIRouter()


async def _build_consolidate_response(parsed: AIParsedResult) -> ConsolidateResponse:
    if not parsed.is_safe_to_consolidate:
        raise HTTPException(status_code=400, detail=parsed.safety_reason)

    outcome = await run_in_threadpool(
        OptimizationService.find_best_match, parsed, MOCK_CONTAINER_DB
    )

    try:
        extracted_data = ExtractedShipmentData(
            origin=parsed.origin,
            destination=parsed.destination,
            date=parsed.date,
            item_name=parsed.item_name,
            volume_m3=parsed.volume_m3,
            weight_tons=parsed.weight_tons,
        )
        dedicated_price, savings_idr, savings_percent = calculate_savings(
            parsed.recommended_split_price_idr
        )
        pricing = PricingRecommendation(
            recommended_split_price_idr=parsed.recommended_split_price_idr,
            dedicated_container_price_idr=dedicated_price,
            savings_idr=savings_idr,
            savings_percent=savings_percent,
            negotiation_basis=parsed.negotiation_basis,
        )

        return ConsolidateResponse(
            status="MATCH_FOUND" if outcome.found else "NO_MATCH_DEDICATED_CONTAINER",
            extracted_data=extracted_data,
            pricing=pricing,
            match=outcome.match,
            alternatives=outcome.alternatives,
            notification_message=outcome.message,
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Data hasil ekstraksi tidak valid setelah verifikasi keamanan: {exc}",
        )


@router.post("/extract", response_model=ExtractionPreview)
async def extract_shipment_data(payload: ConsolidationRequest) -> ExtractionPreview:
    result = extraction.extract(payload.raw_text, datetime.now().date())
    if not result.has_any_signal:
        raise HTTPException(
            status_code=422, detail="Data logistik tidak ditemukan dalam teks"
        )

    return ExtractionPreview(
        origin=result.origin,
        destination=result.destination,
        date=result.date_iso,
        item_name=result.item_name,
        volume_m3=result.volume_m3,
        weight_tons=result.weight_tons,
    )


@router.post("/consolidate-confirmed", response_model=ConsolidateResponse)
async def consolidate_confirmed_shipment(payload: ConfirmedShipmentData) -> ConsolidateResponse:
    parsed = await MLShipmentIntelligenceService.evaluate_confirmed(payload)
    return await _build_consolidate_response(parsed)


@router.post("/consolidate", response_model=ConsolidateResponse)
async def consolidate_shipment(payload: ConsolidationRequest) -> ConsolidateResponse:
    try:
        parsed = await MLShipmentIntelligenceService.parse_and_evaluate(payload.raw_text)
    except NoLogisticsDataFoundError:
        raise HTTPException(
            status_code=422, detail="Data logistik tidak ditemukan dalam teks"
        )
    except ShipmentIntelligenceError as exc:
        raise HTTPException(
            status_code=502, detail=f"Gagal memproses permintaan: {exc}"
        )

    return await _build_consolidate_response(parsed)
