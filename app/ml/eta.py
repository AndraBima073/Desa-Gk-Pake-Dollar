
from __future__ import annotations

import math

# Approximate city-center coordinates (lat, lon) for every canonical city in
# CITY_ALIASES (app/ml/reference_data.py) — lets ETA be computed for any
# origin-destination pair instead of only routes someone entered by hand.
PORT_COORDINATES: dict[str, tuple[float, float]] = {
    "Jakarta": (-6.2088, 106.8456),
    "Surabaya": (-7.2575, 112.7521),
    "Makassar": (-5.1477, 119.4327),
    "Semarang": (-6.9667, 110.4167),
    "Balikpapan": (-1.2379, 116.8529),
    "Medan": (3.5952, 98.6722),
    "Bandung": (-6.9175, 107.6191),
    "Yogyakarta": (-7.7956, 110.3695),
    "Solo": (-7.5755, 110.8243),
    "Denpasar": (-8.6705, 115.2126),
    "Palembang": (-2.9761, 104.7754),
    "Batam": (1.0456, 104.0305),
    "Pekanbaru": (0.5333, 101.4500),
    "Padang": (-0.9471, 100.4172),
    "Banjarmasin": (-3.3186, 114.5944),
    "Pontianak": (-0.0263, 109.3425),
    "Manado": (1.4748, 124.8421),
    "Ambon": (-3.6954, 128.1814),
    "Jayapura": (-2.5337, 140.7181),
    "Malang": (-7.9666, 112.6326),
    "Cirebon": (-6.7063, 108.5570),
    "Bekasi": (-6.2383, 106.9756),
    "Tangerang": (-6.1783, 106.6319),
    "Bogor": (-6.5971, 106.8060),
    "Depok": (-6.4025, 106.7942),
    "Lampung": (-5.4292, 105.2610),
    "Cilegon": (-5.9827, 106.0264),
    "Gresik": (-7.1560, 112.6522),
}

# Effective schedule speed for inter-island feeder vessels, including port
# calls/weather/congestion — not open-ocean cruising speed. Min/max speed
# gives the max/min ETA respectively (slower speed -> longer ETA).
_MIN_SPEED_KM_PER_DAY = 320.0
_MAX_SPEED_KM_PER_DAY = 480.0
_HANDLING_DAYS_MIN = 1
_HANDLING_DAYS_MAX = 2


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius_km * math.asin(math.sqrt(a))


def estimate_eta_days(origin: str, destination: str) -> tuple[int, int] | None:
    """Distance-based ETA range in days, or None if either city has no known
    coordinates. Loading/unloading buffer is added on top of transit time."""
    if origin not in PORT_COORDINATES or destination not in PORT_COORDINATES:
        return None

    lat1, lon1 = PORT_COORDINATES[origin]
    lat2, lon2 = PORT_COORDINATES[destination]
    distance_km = _haversine_km(lat1, lon1, lat2, lon2)

    eta_min = _HANDLING_DAYS_MIN + math.ceil(distance_km / _MAX_SPEED_KM_PER_DAY)
    eta_max = _HANDLING_DAYS_MAX + math.ceil(distance_km / _MIN_SPEED_KM_PER_DAY)
    return eta_min, max(eta_max, eta_min + 1)
