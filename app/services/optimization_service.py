"""1D Bin Packing / Knapsack-style container matching using OR-Tools CP-SAT.

The AI-parsed shipment is treated as a single item that must be placed into
exactly one compatible 20ft container slot, chosen to maximize the
resulting combined space utilization (equivalently, minimize leftover
empty space). This is intentionally solved via CP-SAT rather than a plain
`max()` so the selection logic generalizes cleanly if candidate containers
grow to require multi-constraint (volume AND weight) trade-off handling.
"""
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
    message: str


class OptimizationService:
    @staticmethod
    def find_best_match(
        parsed: AIParsedResult, mock_db: list[ContainerSlotDB]
    ) -> OptimizationOutcome:
        # AIParsedResult.date is a validated ISO string (kept as `str` so it
        # round-trips through Gemini's structured-output schema); convert
        # once here to compare against ContainerSlotDB.date, a real `date`.
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
                message=(
                    "Tidak ditemukan slot kontainer kompatibel untuk rute dan tanggal ini. "
                    "Pengiriman akan diarahkan ke kontainer khusus (dedicated)."
                ),
            )

        best_slot = OptimizationService._solve_best_fit(candidates, parsed)

        combined_volume = round(best_slot.existing_volume_m3 + parsed.volume_m3, 2)
        combined_weight = round(best_slot.existing_weight_tons + parsed.weight_tons, 2)
        utilization = round((combined_volume / best_slot.max_volume_m3) * 100, 2)
        solo_utilization = round((parsed.volume_m3 / best_slot.max_volume_m3) * 100, 2)
        # Floored at 0: AnonymousMatch.efficiency_gained_percent is ge=0 —
        # rounding noise should never surface as a spurious ValidationError.
        efficiency_gained = max(round(utilization - solo_utilization, 2), 0.0)

        remaining_volume_m3 = round(best_slot.max_volume_m3 - combined_volume, 2)
        remaining_weight_tons = round(best_slot.max_weight_tons - combined_weight, 2)
        # Whichever dimension is tighter determines how soon the slot fills —
        # same "binding constraint" idea used for pricing.
        remaining_ratio = min(
            remaining_volume_m3 / best_slot.max_volume_m3,
            remaining_weight_tons / best_slot.max_weight_tons,
        )
        if remaining_ratio < 0.10:
            capacity_urgency = "high"
        elif remaining_ratio < 0.30:
            capacity_urgency = "medium"
        else:
            capacity_urgency = "low"

        match = AnonymousMatch(
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

        # Transparency: show what utilization the other candidates would have
        # yielded, so the client can see the optimizer actually compared
        # options rather than picking the first compatible slot it found.
        alternative_utilizations = sorted(
            (
                round(((slot.existing_volume_m3 + parsed.volume_m3) / slot.max_volume_m3) * 100, 2)
                for slot in candidates
                if slot.slot_id != best_slot.slot_id
            ),
            reverse=True,
        )
        if alternative_utilizations:
            alternatives_text = ", ".join(f"{u}%" for u in alternative_utilizations)
            message = (
                f"Ditemukan {len(candidates)} slot kontainer kompatibel (alternatif: "
                f"{alternatives_text}). Slot terbaik dipilih dengan efisiensi ruang "
                f"gabungan: {utilization}%."
            )
        else:
            message = (
                f"Ditemukan {len(candidates)} slot kontainer kompatibel. "
                f"Slot terbaik dipilih dengan efisiensi ruang gabungan: {utilization}%."
            )

        return OptimizationOutcome(
            found=True, candidates_count=len(candidates), match=match, message=message
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
