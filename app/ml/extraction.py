"""Deterministic, rule-based entity extraction from free-form Indonesian/
English shipment request text: origin, destination, date, item name,
volume, and weight. Regex + a curated gazetteer/keyword dictionary
(`reference_data.py`) instead of an LLM — no network call, no hallucination
risk, fully unit-testable. This is intentionally the "boring but reliable"
half of the pipeline; the safety *judgment* call is delegated to the ML
classifier in `safety_classifier.py`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date as date_type
from datetime import datetime

from dateparser.search import search_dates

from app.ml.reference_data import CITY_ALIASES, DANGEROUS_GOODS_TRAINING_DATA

# Longest-alias-first so "jakarta pusat" matches before the shorter "jakarta".
_ALIAS_TO_CANONICAL: dict[str, str] = {
    alias: canonical for canonical, aliases in CITY_ALIASES.items() for alias in aliases
}
_CITY_PATTERN = re.compile(
    r"\b(" + "|".join(sorted((re.escape(a) for a in _ALIAS_TO_CANONICAL), key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

# (regex, unit-to-base-unit multiplier) — volume normalized to m3, weight to
# metric tons. The leading `-?` is load-bearing: a negative-value injection
# attempt (e.g. "-5 ton") MUST surface as volume_m3/weight_tons < 0, not get
# silently absorbed as a positive number — that's what lets the numeric
# safety-guardian check downstream actually catch it.
_VOLUME_PATTERNS: list[tuple[re.Pattern, float]] = [
    (re.compile(r"(-?\d+(?:[.,]\d+)?)\s*(?:m3|m\^3|m³|meter\s*kubik|kubik)\b", re.IGNORECASE), 1.0),
    (re.compile(r"(-?\d+(?:[.,]\d+)?)\s*(?:liter|ltr|l)\b", re.IGNORECASE), 0.001),
]
_WEIGHT_PATTERNS: list[tuple[re.Pattern, float]] = [
    (re.compile(r"(-?\d+(?:[.,]\d+)?)\s*ton\b", re.IGNORECASE), 1.0),
    (re.compile(r"(-?\d+(?:[.,]\d+)?)\s*kuintal\b", re.IGNORECASE), 0.1),
    (re.compile(r"(-?\d+(?:[.,]\d+)?)\s*kg\b", re.IGNORECASE), 0.001),
]

# Longest-item-phrase-first, drawn from the same labeled set the classifier
# trains on, so the extracted item_name and the safety label stay consistent.
_KNOWN_ITEM_PHRASES: list[str] = sorted(
    (text for text, _ in DANGEROUS_GOODS_TRAINING_DATA), key=len, reverse=True
)
# "barang" ("goods"/"item") is deliberately excluded as a trigger word on
# its own — it's too generic (e.g. "kirim 5 ton barang dari jakarta..." has
# no actual item name after it, just the directional phrase) and produced
# false captures like item_name="dari jakarta".
_ITEM_TRIGGER_PATTERN = re.compile(
    r"(?:kirim|mengirim|muat(?:an)?)\s+"
    r"(?:-?\d+(?:[.,]\d+)?\s*(?:m3|kubik|liter|ltr|l|ton|kuintal|kg)\s+)*"
    r"([a-zA-ZÀ-ɏ ]{3,40}?)"
    r"(?=\s+\d|\s+(?:dari|ke|menuju|tujuan)\b|[.,]|$)",
    re.IGNORECASE,
)

# Explicit month names + relative-date phrases: dateparser's search_dates can
# misfire on a bare quantity (e.g. "8 m3") as a day-of-month, so a match
# carrying one of these tokens is trusted over one that doesn't.
_STRONG_DATE_SIGNALS = [
    "januari", "februari", "maret", "april", "mei", "juni", "juli",
    "agustus", "september", "oktober", "november", "desember",
    "besok", "lusa", "kemarin", "hari ini", "minggu depan", "minggu ini",
    "bulan depan", "bulan ini", "tahun depan", "tomorrow", "today",
]


@dataclass
class ExtractionResult:
    origin: str | None
    destination: str | None
    date_iso: str | None
    item_name: str | None
    volume_m3: float | None
    weight_tons: float | None
    has_any_signal: bool


def _parse_number(raw: str) -> float:
    return float(raw.replace(",", "."))


def _extract_first_match(text: str, patterns: list[tuple[re.Pattern, float]]) -> float | None:
    for pattern, multiplier in patterns:
        match = pattern.search(text)
        if match:
            return round(_parse_number(match.group(1)) * multiplier, 4)
    return None


def _extract_cities(text: str) -> list[tuple[int, str]]:
    """Returns (position, canonical_city) for every city mention, in order."""
    matches = []
    for m in _CITY_PATTERN.finditer(text):
        canonical = _ALIAS_TO_CANONICAL[m.group(1).lower()]
        matches.append((m.start(), canonical))
    return matches


def _extract_origin_destination(text: str) -> tuple[str | None, str | None]:
    lower = text.lower()

    origin = None
    origin_match = re.search(r"\bdari\s+([a-z ]{2,30}?)(?=\s+(?:ke|menuju|tujuan)\b|[.,]|$)", lower)
    if origin_match:
        candidate = _CITY_PATTERN.search(origin_match.group(1))
        if candidate:
            origin = _ALIAS_TO_CANONICAL[candidate.group(1).lower()]

    destination = None
    dest_match = re.search(r"\b(?:ke|menuju|tujuan)\s+([a-z ]{2,30}?)(?=\s+(?:dari|tanggal)\b|[.,]|$)", lower)
    if dest_match:
        candidate = _CITY_PATTERN.search(dest_match.group(1))
        if candidate:
            destination = _ALIAS_TO_CANONICAL[candidate.group(1).lower()]

    if origin and destination:
        return origin, destination

    # Fallback: no directional keyword found (or only one side matched) —
    # take the first two distinct city mentions in reading order.
    cities_in_order = _extract_cities(text)
    distinct: list[str] = []
    for _, city in cities_in_order:
        if city not in distinct:
            distinct.append(city)
    if len(distinct) >= 2:
        return distinct[0], distinct[1]
    if len(distinct) == 1:
        return origin or distinct[0], destination
    return origin, destination


def _extract_date(text: str, reference_date: date_type) -> str | None:
    reference_datetime = datetime.combine(reference_date, datetime.min.time())
    try:
        results = search_dates(
            text,
            languages=["id", "en"],
            settings={
                "PREFER_DATES_FROM": "future",
                "RELATIVE_BASE": reference_datetime,
                "STRICT_PARSING": False,
            },
        )
    except Exception:
        results = None

    if not results:
        return None

    def in_range(parsed: datetime) -> bool:
        delta_days = (parsed.date() - reference_date).days
        return -30 <= delta_days <= 730

    # Prefer matches carrying an explicit month name or a recognized
    # relative-date keyword over a bare number dateparser guessed at.
    strong_matches = [
        parsed
        for matched_text, parsed in results
        if in_range(parsed) and any(sig in matched_text.lower() for sig in _STRONG_DATE_SIGNALS)
    ]
    if strong_matches:
        return strong_matches[0].date().isoformat()

    weak_matches = [parsed for _matched_text, parsed in results if in_range(parsed)]
    if weak_matches:
        return weak_matches[0].date().isoformat()
    return None


def _extract_item_name(text: str) -> str | None:
    lower = text.lower()
    for phrase in _KNOWN_ITEM_PHRASES:
        if phrase in lower:
            return phrase

    trigger_match = _ITEM_TRIGGER_PATTERN.search(text)
    if trigger_match:
        candidate = trigger_match.group(1).strip()
        if candidate:
            return candidate

    return None


def extract(raw_text: str, reference_date: date_type) -> ExtractionResult:
    origin, destination = _extract_origin_destination(raw_text)
    volume_m3 = _extract_first_match(raw_text, _VOLUME_PATTERNS)
    weight_tons = _extract_first_match(raw_text, _WEIGHT_PATTERNS)
    item_name = _extract_item_name(raw_text)
    date_iso = _extract_date(raw_text, reference_date)

    has_any_signal = any(
        [origin, destination, volume_m3 is not None, weight_tons is not None, item_name]
    )

    return ExtractionResult(
        origin=origin,
        destination=destination,
        date_iso=date_iso,
        item_name=item_name,
        volume_m3=volume_m3,
        weight_tons=weight_tons,
        has_any_signal=has_any_signal,
    )
