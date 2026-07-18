"""Deterministic split-price recommendation: pro-rates a shipment's share of
a standard 20ft container against typical Indonesian domestic freight
rates. Extracted from the old LLM-prompt pricing instructions so the same
business rule is now testable and doesn't depend on model output.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.database import STANDARD_MAX_VOLUME_M3, STANDARD_MAX_WEIGHT_TONS

# A full dedicated 20ft container costs roughly IDR 6.5M-9M depending on
# route distance; use the midpoint as a single flat rate for MVP simplicity.
_BASE_CONTAINER_COST_IDR = 7_500_000
_SERVICE_MARGIN = 0.08


@dataclass
class PriceRecommendation:
    recommended_split_price_idr: int
    negotiation_basis: str


def recommend_price(volume_m3: float, weight_tons: float) -> PriceRecommendation:
    volume_ratio = volume_m3 / STANDARD_MAX_VOLUME_M3
    weight_ratio = weight_tons / STANDARD_MAX_WEIGHT_TONS

    if volume_ratio >= weight_ratio:
        binding_ratio, binding_label = volume_ratio, "volume"
    else:
        binding_ratio, binding_label = weight_ratio, "berat"

    price = round(_BASE_CONTAINER_COST_IDR * binding_ratio * (1 + _SERVICE_MARGIN))
    base_cost_formatted = f"{_BASE_CONTAINER_COST_IDR:,}".replace(",", ".")

    negotiation_basis = (
        f"Estimasi berdasarkan rasio {binding_label} ({binding_ratio * 100:.1f}% dari "
        f"kapasitas kontainer 20ft standar), dipro-rata dari perkiraan biaya kontainer "
        f"penuh IDR {base_cost_formatted} ditambah margin layanan konsolidasi "
        f"{_SERVICE_MARGIN * 100:.0f}%."
    )

    return PriceRecommendation(
        recommended_split_price_idr=max(price, 1),
        negotiation_basis=negotiation_basis,
    )


def calculate_savings(recommended_split_price_idr: int) -> tuple[int, int, float]:
    """Returns (dedicated_container_price_idr, savings_idr, savings_percent) —
    the direct cost comparison against booking a full dedicated container,
    which is the number a freight buyer actually decides on."""
    dedicated_price = _BASE_CONTAINER_COST_IDR
    savings_idr = max(dedicated_price - recommended_split_price_idr, 0)
    savings_percent = round((savings_idr / dedicated_price) * 100, 1)
    return dedicated_price, savings_idr, savings_percent
