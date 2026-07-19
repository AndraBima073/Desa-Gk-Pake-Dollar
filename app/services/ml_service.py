
from __future__ import annotations

from datetime import datetime

from app.ml import extraction, pricing, safety_classifier
from app.schemas.cargo import AIParsedResult
from app.services.base import NoLogisticsDataFoundError


class MLShipmentIntelligenceService:
    @staticmethod
    async def parse_and_evaluate(raw_text: str) -> AIParsedResult:
        reference_date = datetime.now().date()
        result = extraction.extract(raw_text, reference_date)

        if not result.has_any_signal:
            raise NoLogisticsDataFoundError(
                "Tidak ada data logistik yang valid ditemukan dalam teks."
            )

        origin = result.origin or "Tidak diketahui"
        destination = result.destination or "Tidak diketahui"
        date_iso = result.date_iso or reference_date.isoformat()
        item_name = result.item_name or "Barang tidak teridentifikasi"
        volume_m3 = result.volume_m3 if result.volume_m3 is not None else 0.0
        weight_tons = result.weight_tons if result.weight_tons is not None else 0.0

        # Classify on the full raw text when item_name extraction came up
        # empty — the safety-critical decision should not depend on the
        # (best-effort, sometimes-empty) display-name extraction succeeding.
        classification_text = result.item_name or raw_text
        safety = safety_classifier.predict(classification_text)

        numeric_invalid = volume_m3 <= 0 or weight_tons <= 0
        is_safe = not safety.is_dangerous and not numeric_invalid

        if safety.is_dangerous:
            safety_reason = (
                f"Terindikasi sebagai barang berbahaya (dangerous goods) oleh model "
                f"klasifikasi ML (keyakinan {safety.confidence * 100:.0f}%) dan tidak "
                f"dapat dikonsolidasikan dengan kargo umum."
            )
        elif numeric_invalid:
            safety_reason = (
                "Volume atau berat yang diekstrak tidak valid (<= 0) — kemungkinan data "
                "tidak lengkap atau tidak logis dalam teks permintaan."
            )
        else:
            safety_reason = (
                f"Tidak terindikasi sebagai barang berbahaya oleh model klasifikasi ML "
                f"(keyakinan {safety.confidence * 100:.0f}%). Aman untuk dikonsolidasikan."
            )

        price = pricing.recommend_price(volume_m3=volume_m3, weight_tons=weight_tons)

        return AIParsedResult(
            origin=origin,
            destination=destination,
            date=date_iso,
            item_name=item_name,
            volume_m3=volume_m3,
            weight_tons=weight_tons,
            is_safe_to_consolidate=is_safe,
            safety_reason=safety_reason,
            recommended_split_price_idr=price.recommended_split_price_idr,
            negotiation_basis=price.negotiation_basis,
        )
