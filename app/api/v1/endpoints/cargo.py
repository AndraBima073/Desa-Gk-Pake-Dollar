"""Single SPA-style endpoint: raw text in, fully processed anonymous JSON out."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import ValidationError

from app.database import MOCK_CONTAINER_DB
from app.ml.pricing import calculate_savings
from app.schemas.cargo import (
    ConsolidateResponse,
    ConsolidationRequest,
    ExtractedShipmentData,
    PricingRecommendation,
)
from app.services.base import NoLogisticsDataFoundError, ShipmentIntelligenceError
from app.services.ml_service import MLShipmentIntelligenceService
from app.services.optimization_service import OptimizationService

router = APIRouter()


@router.post("/consolidate", response_model=ConsolidateResponse)
async def consolidate_shipment(payload: ConsolidationRequest) -> ConsolidateResponse:
    # 1-2. Parse + evaluate via the self-hosted ML pipeline (extraction +
    # safety classifier + pricing — see app/services/ml_service.py).
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

    # 3. Safety gate.
    if not parsed.is_safe_to_consolidate:
        raise HTTPException(status_code=400, detail=parsed.safety_reason)

    # 4. CPU-bound OR-Tools CP-SAT solve — offload to the threadpool so a
    #    slow solve never blocks the event loop under concurrent load.
    outcome = await run_in_threadpool(
        OptimizationService.find_best_match, parsed, MOCK_CONTAINER_DB
    )

    # 5. Anonymous response assembly. Wrapped: is_safe_to_consolidate only
    #    guarantees volume/weight are positive (see the numeric_invalid
    #    check in MLShipmentIntelligenceService); a residual bad value here
    #    (e.g. a zero-rounded price) must fail as a controlled 400, never
    #    an unhandled 500.
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
