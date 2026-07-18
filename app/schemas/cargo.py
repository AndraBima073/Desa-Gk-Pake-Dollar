
from __future__ import annotations

from datetime import date as date_type
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

class ConsolidationRequest(BaseModel):
    raw_text: str = Field(
        ...,
        min_length=5,
        max_length=4000,
        description="Unstructured shipment request text (Bahasa Indonesia or English).",
        examples=[
            "Halo, saya mau kirim tekstil 8 m3 berat 5 ton dari Jakarta ke Surabaya "
            "tanggal 20 Juli 2026."
        ],
    )


class AIParsedResult(BaseModel):
    origin: str = Field(description="City or port of origin")
    destination: str = Field(description="City or port of destination")
    date: str = Field(description="ISO 8601 shipment date (YYYY-MM-DD)")
    item_name: str = Field(description="Specific name of the goods")
    volume_m3: float = Field(description="Total volume in cubic meters")
    weight_tons: float = Field(description="Total weight in metric tons")

    is_safe_to_consolidate: bool = Field(
        description="False if the item is Dangerous Goods (DG), explosive, physically "
        "impossible (e.g. negative/zero volume or weight), or otherwise cannot be mixed "
        "with general cargo"
    )
    safety_reason: str = Field(description="Explanation of safety compliance or violation")

    recommended_split_price_idr: int = Field(
        description="Fair estimated price for the user to pay for this shared space"
    )
    negotiation_basis: str = Field(
        description="Why this price is fair based on volume/weight ratio"
    )

    @field_validator("date")
    @classmethod
    def _validate_iso_date(cls, value: str) -> str:
        try:
            date_type.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("date must be a valid ISO 8601 date (YYYY-MM-DD)") from exc
        return value

class ExtractedShipmentData(BaseModel):
    origin: str
    destination: str
    date: date_type
    item_name: str
    volume_m3: float = Field(gt=0, description="Must be a strictly positive volume")
    weight_tons: float = Field(gt=0, description="Must be a strictly positive weight")


class PricingRecommendation(BaseModel):
    recommended_split_price_idr: int = Field(gt=0)
    dedicated_container_price_idr: int = Field(
        gt=0, description="What a full dedicated 20ft container would cost instead"
    )
    savings_idr: int = Field(ge=0, description="dedicated_container_price_idr minus the split price")
    savings_percent: float = Field(ge=0, le=100)
    negotiation_basis: str


class AnonymousMatch(BaseModel):
    """Everything a requester is allowed to see about the container they were
    matched with. Deliberately excludes any field that could identify the
    owning company (no slot_id, no company_id, no company_name).
    """

    anonymous_slot_reference: str = Field(
        description="Randomly generated per-request token, not traceable to the owning company"
    )
    route: str
    consolidation_date: date_type
    combined_volume_m3: float = Field(gt=0)
    combined_weight_tons: float = Field(gt=0)
    space_utilization_percent: float = Field(gt=0, le=100)
    efficiency_gained_percent: float = Field(ge=0)
    remaining_volume_m3: float = Field(ge=0)
    remaining_weight_tons: float = Field(ge=0)
    capacity_urgency: Literal["low", "medium", "high"] = Field(
        description="How close this slot is to being full — derived from remaining space"
    )


class ConsolidateResponse(BaseModel):
    status: Literal["MATCH_FOUND", "NO_MATCH_DEDICATED_CONTAINER"]
    extracted_data: ExtractedShipmentData
    pricing: PricingRecommendation
    match: Optional[AnonymousMatch] = None
    notification_message: str

class AvailableRoute(BaseModel):
    origin: str
    destination: str
    date: date_type
    available_volume_m3: float = Field(ge=0, description="Remaining space before the slot is full")
    available_weight_tons: float = Field(ge=0)
    space_utilization_percent: float = Field(ge=0, le=100, description="How full the slot already is")
