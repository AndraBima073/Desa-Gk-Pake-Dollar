
from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

STANDARD_MAX_VOLUME_M3: float = 33.0
STANDARD_MAX_WEIGHT_TONS: float = 22.0


class ContainerSlotDB(BaseModel):
    slot_id: str  
    company_id: str  
    company_name: str 

    origin: str
    destination: str
    date: date

    existing_volume_m3: float = Field(ge=0)
    existing_weight_tons: float = Field(ge=0)

    max_volume_m3: float = Field(default=STANDARD_MAX_VOLUME_M3, gt=0)
    max_weight_tons: float = Field(default=STANDARD_MAX_WEIGHT_TONS, gt=0)


MOCK_CONTAINER_DB: list[ContainerSlotDB] = [
    ContainerSlotDB(
        slot_id="CTN-JKT-001",
        company_id="CMP-0091",
        company_name="PT Sumber Makmur Logistik",
        origin="Jakarta",
        destination="Surabaya",
        date=date(2026, 7, 20),
        existing_volume_m3=18.5,
        existing_weight_tons=12.0,
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-002",
        company_id="CMP-0114",
        company_name="CV Bintang Cargo",
        origin="Jakarta",
        destination="Surabaya",
        date=date(2026, 7, 20),
        existing_volume_m3=10.0,
        existing_weight_tons=8.0,
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-003",
        company_id="CMP-0157",
        company_name="PT Cipta Logistindo",
        origin="Jakarta",
        destination="Surabaya",
        date=date(2026, 7, 20),
        existing_volume_m3=5.0,
        existing_weight_tons=4.0,
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-001",
        company_id="CMP-0203",
        company_name="PT Trans Nusantara",
        origin="Surabaya",
        destination="Makassar",
        date=date(2026, 7, 22),
        existing_volume_m3=22.0,
        existing_weight_tons=15.0,
    ),
    ContainerSlotDB(
        slot_id="CTN-SMG-001",
        company_id="CMP-0248",
        company_name="UD Sejahtera Abadi",
        origin="Semarang",
        destination="Balikpapan",
        date=date(2026, 7, 25),
        existing_volume_m3=14.0,
        existing_weight_tons=9.5,
    ),
    ContainerSlotDB(
        slot_id="CTN-MDN-001",
        company_id="CMP-0311",
        company_name="PT Andalan Ekspedisi",
        origin="Medan",
        destination="Jakarta",
        date=date(2026, 7, 18),
        existing_volume_m3=25.0,
        existing_weight_tons=17.0,
    ),
]
