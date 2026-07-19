
from __future__ import annotations

from dataclasses import dataclass
from datetime import date as date_type
from typing import Optional
from uuid import uuid4

from ortools.sat.python import cp_model

from app.database import ContainerSlotDB
from app.schemas.cargo import AIParsedResult, AnonymousMatch

_SCALE = 10_000  # CP-SAT requires integer coefficients; scale float ratios up.


@dataclass
class OptimizationOutcome:
    found: bool
    candidates_count: int
    match: Optional[AnonymousMatch]
    alternatives: list[AnonymousMatch]
    message: str


class OptimizationService:
    @staticmethod
    def find_best_match(
        parsed: AIParsedResult, mock_db: list[ContainerSlotDB]
    ) -> OptimizationOutcome:
        shipment_date = date_type.fromisoformat(parsed.date)

        candidates = [
            slot
            for slot in mock_db
            if slot.origin.strip().lower() == parsed.origin.strip().lower()
            and slot.destination.strip().lower() == parsed.destination.strip().lower()
            and slot.date == shipment_date
            and (slot.existing_volume_m3 + parsed.volume_m3) <= slot.max_volume_m3
            and (slot.existing_weight_tons + parsed.weight_tons) <= slot.max_weight_tons
        ]

        if not candidates:
            return OptimizationOutcome(
                found=False,
                candidates_count=0,
                match=None,
                alternatives=[],
                message=(
                    "Tidak ditemukan slot kontainer kompatibel untuk rute dan tanggal ini. "
                    "Pengiriman akan diarahkan ke kontainer khusus (dedicated)."
                ),
            )

        best_slot = OptimizationService._solve_best_fit(candidates, parsed)

        # Build a fully-populated AnonymousMatch for every capacity-feasible
        # candidate (not just the winner) so the client can render a "best
        # match + alternative slots" list, each with its own utility data.
        matches_by_slot_id = {
            slot.slot_id: OptimizationService._build_match(slot, parsed, shipment_date)
            for slot in candidates
        }
        match = matches_by_slot_id[best_slot.slot_id]
        # Transparency: surface what the other candidates would have yielded,
        # so the client can see the optimizer actually compared options
        # rather than picking the first compatible slot it found.
        alternatives = sorted(
            (m for slot_id, m in matches_by_slot_id.items() if slot_id != best_slot.slot_id),
            key=lambda m: m.space_utilization_percent,
            reverse=True,
        )

        if alternatives:
            alternatives_text = ", ".join(
                f"{a.space_utilization_percent}%" for a in alternatives
            )
            message = (
                f"Ditemukan {len(candidates)} slot kontainer kompatibel (alternatif: "
                f"{alternatives_text}). Slot terbaik dipilih dengan efisiensi ruang "
                f"gabungan: {match.space_utilization_percent}%."
            )
        else:
            message = (
                f"Ditemukan {len(candidates)} slot kontainer kompatibel. "
                f"Slot terbaik dipilih dengan efisiensi ruang gabungan: "
                f"{match.space_utilization_percent}%."
            )

        return OptimizationOutcome(
            found=True,
            candidates_count=len(candidates),
            match=match,
            alternatives=alternatives,
            message=message,
        )

    @staticmethod
    def _build_match(
        slot: ContainerSlotDB, parsed: AIParsedResult, shipment_date: date_type
    ) -> AnonymousMatch:
        combined_volume = round(slot.existing_volume_m3 + parsed.volume_m3, 2)
        combined_weight = round(slot.existing_weight_tons + parsed.weight_tons, 2)
        utilization = round((combined_volume / slot.max_volume_m3) * 100, 2)
        solo_utilization = round((parsed.volume_m3 / slot.max_volume_m3) * 100, 2)
        # Floored at 0: AnonymousMatch.efficiency_gained_percent is ge=0 —
        # rounding noise should never surface as a spurious ValidationError.
        efficiency_gained = max(round(utilization - solo_utilization, 2), 0.0)

        remaining_volume_m3 = round(slot.max_volume_m3 - combined_volume, 2)
        remaining_weight_tons = round(slot.max_weight_tons - combined_weight, 2)
        # Whichever dimension is tighter determines how soon the slot fills —
        # same "binding constraint" idea used for pricing.
        remaining_ratio = min(
            remaining_volume_m3 / slot.max_volume_m3,
            remaining_weight_tons / slot.max_weight_tons,
        )
        if remaining_ratio < 0.10:
            capacity_urgency = "high"
        elif remaining_ratio < 0.30:
            capacity_urgency = "medium"
        else:
            capacity_urgency = "low"

        return AnonymousMatch(
            anonymous_slot_reference=f"SLOT-{uuid4().hex[:8].upper()}",
            route=f"{parsed.origin} -> {parsed.destination}",
            consolidation_date=shipment_date,
            combined_volume_m3=combined_volume,
            combined_weight_tons=combined_weight,
            space_utilization_percent=utilization,
            efficiency_gained_percent=efficiency_gained,
            remaining_volume_m3=remaining_volume_m3,
            remaining_weight_tons=remaining_weight_tons,
            capacity_urgency=capacity_urgency,
        )

    @staticmethod
    def _solve_best_fit(
        candidates: list[ContainerSlotDB], parsed: AIParsedResult
    ) -> ContainerSlotDB:
        """Among all capacity-feasible candidates, pick the one that
        maximizes combined volume utilization (i.e. leaves the least empty
        space) via a CP-SAT single-choice knapsack formulation.
        """
        model = cp_model.CpModel()
        n = len(candidates)
        choice_vars = [model.NewBoolVar(f"choose_slot_{i}") for i in range(n)]
        model.Add(sum(choice_vars) == 1)

        utilization_scores = [
            int(((slot.existing_volume_m3 + parsed.volume_m3) / slot.max_volume_m3) * _SCALE)
            for slot in candidates
        ]
        model.Maximize(sum(choice_vars[i] * utilization_scores[i] for i in range(n)))

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            for i in range(n):
                if solver.Value(choice_vars[i]) == 1:
                    return candidates[i]

        # Defensive fallback (should be unreachable given a trivial feasible model).
        return max(candidates, key=lambda s: s.existing_volume_m3 + parsed.volume_m3)
