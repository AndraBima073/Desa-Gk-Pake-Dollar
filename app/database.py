
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
    ContainerSlotDB(
        slot_id="CTN-JKT-004",
        company_id="CMP-0091",
        company_name="PT Sumber Makmur Logistik",
        origin="Jakarta",
        destination="Medan",
        date=date(2026, 7, 21),
        existing_volume_m3=33.0,
        existing_weight_tons=22.0,
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-002",
        company_id="CMP-0401",
        company_name="PT Borneo Express Line",
        origin="Surabaya",
        destination="Banjarmasin",
        date=date(2026, 7, 23),
        existing_volume_m3=0.0,
        existing_weight_tons=0.0,
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-005",
        company_id="CMP-0512",
        company_name="PT FastFlow Trans",
        origin="Jakarta",
        destination="Surabaya",
        date=date(2026, 7, 21),
        existing_volume_m3=12.0,
        existing_weight_tons=6.0,
    ),
    ContainerSlotDB(
        slot_id="CTN-BDG-001",
        company_id="CMP-0620",
        company_name="CV Priangan Cargo",
        origin="Bandung",
        destination="Denpasar",
        date=date(2026, 7, 26),
        existing_volume_m3=15.0,
        existing_weight_tons=21.0,
    ),
    ContainerSlotDB(
        slot_id="CTN-MKS-001",
        company_id="CMP-0715",
        company_name="PT Angin Mamiri Freight",
        origin="Makassar",
        destination="Surabaya",
        date=date(2026, 7, 28),
        existing_volume_m3=32.0,
        existing_weight_tons=8.0,
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-004",
        company_id="CMP-0091",
        company_name="PT Sumber Makmur Logistik", 
        origin="Jakarta", 
        destination="Medan", 
        date=date(2026, 7, 21), 
        existing_volume_m3=33.0, 
        existing_weight_tons=22.0
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-002", 
        company_id="CMP-0401", 
        company_name="PT Borneo Express Line", 
        origin="Surabaya", 
        destination="Banjarmasin", 
        date=date(2026, 7, 23), 
        existing_volume_m3=33.0, 
        existing_weight_tons=22.0
    ),
    ContainerSlotDB(
        slot_id="CTN-SMG-002", 
        company_id="CMP-0248", 
        company_name="UD Sejahtera Abadi", 
        origin="Semarang", 
        destination="Makassar", 
        date=date(2026, 7, 26), 
        existing_volume_m3=33.0, 
        existing_weight_tons=22.0
    ),
    ContainerSlotDB(
        slot_id="CTN-MDN-002", 
        company_id="CMP-0311", 
        company_name="PT Andalan Ekspedisi", 
        origin="Medan", 
        destination="Batam", 
        date=date(2026, 7, 19), 
        existing_volume_m3=33.0, 
        existing_weight_tons=22.0
    ),
    ContainerSlotDB(
        slot_id="CTN-BPN-001", 
        company_id="CMP-0888", 
        company_name="PT Samudera Jaya Logistik", 
        origin="Balikpapan", 
        destination="Surabaya", 
        date=date(2026, 8, 1), 
        existing_volume_m3=33.0, 
        existing_weight_tons=22.0
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-005", 
        company_id="CMP-0512", 
        company_name="PT FastFlow Trans", 
        origin="Jakarta", destination="Surabaya", 
        date=date(2026, 7, 21), 
        existing_volume_m3=0.0, 
        existing_weight_tons=0.0
    ),
    ContainerSlotDB(
        slot_id="CTN-DPS-001", 
        company_id="CMP-1050", 
        company_name="PT Nusa Dua Cargo", 
        origin="Denpasar", 
        destination="Surabaya", 
        date=date(2026, 8, 2), 
        existing_volume_m3=0.0, 
        existing_weight_tons=0.0
    ),
    ContainerSlotDB(
        slot_id="CTN-MKS-001", 
        company_id="CMP-0715", 
        company_name="PT Angin Mamiri Freight", 
        origin="Makassar", 
        destination="Ambon", 
        date=date(2026, 8, 3), 
        existing_volume_m3=0.0, 
        existing_weight_tons=0.0
    ),
    ContainerSlotDB(
        slot_id="CTN-BDG-001", 
        company_id="CMP-0620", 
        company_name="CV Priangan Cargo", 
        origin="Bandung", 
        destination="Denpasar", 
        date=date(2026, 7, 26), 
        existing_volume_m3=0.0, 
        existing_weight_tons=0.0
    ),
    ContainerSlotDB(
        slot_id="CTN-PLM-001", 
        company_id="CMP-1299", 
        company_name="CV Inti Raya Ekspedisi", 
        origin="Palembang", 
        destination="Jakarta", 
        date=date(2026, 8, 4), 
        existing_volume_m3=0.0, 
        existing_weight_tons=0.0
    ),
    ContainerSlotDB(
        slot_id="CTN-BDG-002", 
        company_id="CMP-0620", 
        company_name="CV Priangan Cargo", 
        origin="Bandung", 
        destination="Surabaya", 
        date=date(2026, 7, 27), 
        existing_volume_m3=10.0, 
        existing_weight_tons=21.5
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-006", 
        company_id="CMP-0091", 
        company_name="PT Sumber Makmur Logistik", 
        origin="Jakarta", 
        destination="Pontianak", 
        date=date(2026, 8, 1), 
        existing_volume_m3=12.0, 
        existing_weight_tons=21.8
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-003", 
        company_id="CMP-0203", 
        company_name="PT Trans Nusantara", 
        origin="Surabaya", 
        destination="Balikpapan", 
        date=date(2026, 8, 2), 
        existing_volume_m3=8.5, 
        existing_weight_tons=21.0
    ),
    ContainerSlotDB(
        slot_id="CTN-SMG-003", 
        company_id="CMP-1123", 
        company_name="PT Garuda Logistics Group", 
        origin="Semarang", 
        destination="Banjarmasin", 
        date=date(2026, 8, 3), 
        existing_volume_m3=14.0, 
        existing_weight_tons=21.9
    ),
    ContainerSlotDB(
        slot_id="CTN-MKS-002", 
        company_id="CMP-0715", 
        company_name="PT Angin Mamiri Freight", 
        origin="Makassar", 
        destination="Surabaya", 
        date=date(2026, 7, 28), 
        existing_volume_m3=32.2, 
        existing_weight_tons=5.0
    ),
    ContainerSlotDB(
        slot_id="CTN-BTM-001", 
        company_id="CMP-0942", 
        company_name="CV Merdeka Transport", 
        origin="Batam", 
        destination="Jakarta", 
        date=date(2026, 8, 2), 
        existing_volume_m3=32.5, 
        existing_weight_tons=8.0
    ),
    ContainerSlotDB(
        slot_id="CTN-PKU-001", 
        company_id="CMP-0311", 
        company_name="PT Andalan Ekspedisi", 
        origin="Pekanbaru", 
        destination="Jakarta", 
        date=date(2026, 8, 5), 
        existing_volume_m3=32.0, 
        existing_weight_tons=6.5
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-007", 
        company_id="CMP-0114", 
        company_name="CV Bintang Cargo", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 22), 
        existing_volume_m3=12.0, 
        existing_weight_tons=7.0
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-008", 
        company_id="CMP-0157", 
        company_name="PT Cipta Logistindo", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 22), 
        existing_volume_m3=20.0, 
        existing_weight_tons=15.0
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-009", 
        company_id="CMP-0203", 
        company_name="PT Trans Nusantara", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 23), 
        existing_volume_m3=3.0, 
        existing_weight_tons=2.0
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-010", 
        company_id="CMP-0401", 
        company_name="PT Borneo Express Line", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 23), 
        existing_volume_m3=28.0, 
        existing_weight_tons=18.0
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-011", 
        company_id="CMP-0512", 
        company_name="PT FastFlow Trans", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 24), 
        existing_volume_m3=15.0, 
        existing_weight_tons=10.0
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-012", 
        company_id="CMP-0091", 
        company_name="PT Sumber Makmur Logistik", 
        origin="Jakarta", 
        destination="Semarang", 
        date=date(2026, 7, 15), 
        existing_volume_m3=7.3, 
        existing_weight_tons=4.9
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-004", 
        company_id="CMP-0114", 
        company_name="CV Bintang Cargo", 
        origin="Surabaya", 
        destination="Medan", 
        date=date(2026, 7, 16), 
        existing_volume_m3=14.6, 
        existing_weight_tons=9.8
    ),
    ContainerSlotDB(
        slot_id="CTN-SMG-004", 
        company_id="CMP-0157", 
        company_name="PT Cipta Logistindo", 
        origin="Semarang", 
        destination="Makassar", 
        date=date(2026, 7, 17), 
        existing_volume_m3=21.9, 
        existing_weight_tons=14.7
    ),
    ContainerSlotDB(
        slot_id="CTN-MDN-003", 
        company_id="CMP-0203", 
        company_name="PT Trans Nusantara", 
        origin="Medan", 
        destination="Batam", 
        date=date(2026, 7, 18), 
        existing_volume_m3=29.2, 
        existing_weight_tons=19.6
    ),
    ContainerSlotDB(
        slot_id="CTN-MKS-003", 
        company_id="CMP-0248", 
        company_name="UD Sejahtera Abadi", 
        origin="Makassar", 
        destination="Balikpapan", 
        date=date(2026, 7, 19), 
        existing_volume_m3=3.5, 
        existing_weight_tons=2.5
    ),
    ContainerSlotDB(
        slot_id="CTN-BPN-002", 
        company_id="CMP-0311", 
        company_name="PT Andalan Ekspedisi", 
        origin="Balikpapan", 
        destination="Denpasar", 
        date=date(2026, 7, 20), 
        existing_volume_m3=10.8, 
        existing_weight_tons=7.4
    ),
    ContainerSlotDB(
        slot_id="CTN-BDJ-001", 
        company_id="CMP-0401", 
        company_name="PT Borneo Express Line", 
        origin="Banjarmasin", 
        destination="Semarang", 
        date=date(2026, 7, 21), 
        existing_volume_m3=18.1, 
        existing_weight_tons=12.3
    ),
    ContainerSlotDB(
        slot_id="CTN-DPS-002", 
        company_id="CMP-0512", 
        company_name="PT FastFlow Trans", 
        origin="Denpasar", 
        destination="Banjarmasin", 
        date=date(2026, 7, 22), 
        existing_volume_m3=25.4,
        existing_weight_tons=17.2
    ),
    ContainerSlotDB(
        slot_id="CTN-PLM-002", 
        company_id="CMP-0620", 
        company_name="CV Priangan Cargo", 
        origin="Palembang", 
        destination="Medan", 
        date=date(2026, 7, 23), 
        existing_volume_m3=32.7, 
        existing_weight_tons=0.1
    ),
    ContainerSlotDB(
        slot_id="CTN-PNK-001", 
        company_id="CMP-0715", 
        company_name="PT Angin Mamiri Freight", 
        origin="Pontianak", 
        destination="Palembang", 
        date=date(2026, 7, 24), 
        existing_volume_m3=7.0, 
        existing_weight_tons=5.0
    ),
    ContainerSlotDB(
        slot_id="CTN-PKU-002", 
        company_id="CMP-0888", 
        company_name="PT Samudera Jaya Logistik", 
        origin="Pekanbaru", 
        destination="Pontianak", 
        date=date(2026, 7, 25), 
        existing_volume_m3=14.3, 
        existing_weight_tons=9.9
    ),
    ContainerSlotDB(
        slot_id="CTN-BDG-003", 
        company_id="CMP-0942", 
        company_name="CV Merdeka Transport", 
        origin="Bandung", 
        destination="Ambon", 
        date=date(2026, 7, 26), 
        existing_volume_m3=21.6, 
        existing_weight_tons=14.8
    ),
    ContainerSlotDB(
        slot_id="CTN-BTM-002", 
        company_id="CMP-1050", 
        company_name="PT Nusa Dua Cargo", 
        origin="Batam", 
        destination="Pekanbaru", 
        date=date(2026, 7, 27), 
        existing_volume_m3=28.9, 
        existing_weight_tons=19.7
    ),
    ContainerSlotDB(
        slot_id="CTN-MND-001", 
        company_id="CMP-1123", 
        company_name="PT Garuda Logistics Group", 
        origin="Manado", 
        destination="Manado", 
        date=date(2026, 7, 28), 
        existing_volume_m3=3.2, 
        existing_weight_tons=2.6
    ),
    ContainerSlotDB(
        slot_id="CTN-AMB-001", 
        company_id="CMP-1299", 
        company_name="CV Inti Raya Ekspedisi", 
        origin="Ambon", 
        destination="Bandung", 
        date=date(2026, 7, 29), 
        existing_volume_m3=10.5, 
        existing_weight_tons=7.5
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-013", 
        company_id="CMP-0091", 
        company_name="PT Sumber Makmur Logistik", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 30), 
        existing_volume_m3=17.8, 
        existing_weight_tons=12.4
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-005", 
        company_id="CMP-0114", 
        company_name="CV Bintang Cargo", 
        origin="Surabaya", 
        destination="Jakarta", 
        date=date(2026, 7, 31), 
        existing_volume_m3=25.1, 
        existing_weight_tons=17.3
    ),
    ContainerSlotDB(
        slot_id="CTN-SMG-005", 
        company_id="CMP-0157", 
        company_name="PT Cipta Logistindo", 
        origin="Semarang", 
        destination="Makassar", 
        date=date(2026, 8, 1), 
        existing_volume_m3=32.4, 
        existing_weight_tons=0.2
    ),
    ContainerSlotDB(
        slot_id="CTN-MDN-004", 
        company_id="CMP-0203", 
        company_name="PT Trans Nusantara", 
        origin="Medan", 
        destination="Batam", 
        date=date(2026, 8, 2), 
        existing_volume_m3=6.7, 
        existing_weight_tons=5.1
    ),
    ContainerSlotDB(
        slot_id="CTN-MKS-004", 
        company_id="CMP-0248", 
        company_name="UD Sejahtera Abadi", 
        origin="Makassar", 
        destination="Balikpapan", 
        date=date(2026, 8, 3), 
        existing_volume_m3=14.0, 
        existing_weight_tons=10.0
    ),
    ContainerSlotDB(
        slot_id="CTN-BPN-003", 
        company_id="CMP-0311", 
        company_name="PT Andalan Ekspedisi", 
        origin="Balikpapan", 
        destination="Denpasar", 
        date=date(2026, 8, 4), 
        existing_volume_m3=21.3, 
        existing_weight_tons=14.9
    ),
    ContainerSlotDB(
        slot_id="CTN-BDJ-002", 
        company_id="CMP-0401", 
        company_name="PT Borneo Express Line", 
        origin="Banjarmasin", 
        destination="Semarang", 
        date=date(2026, 8, 5), 
        existing_volume_m3=28.6, 
        existing_weight_tons=19.8
    ),
    ContainerSlotDB(
        slot_id="CTN-DPS-003", 
        company_id="CMP-0512", 
        company_name="PT FastFlow Trans", 
        origin="Denpasar", 
        destination="Banjarmasin", 
        date=date(2026, 8, 6), 
        existing_volume_m3=2.9, 
        existing_weight_tons=2.7
    ),
    ContainerSlotDB(
        slot_id="CTN-PLM-003", 
        company_id="CMP-0620", 
        company_name="CV Priangan Cargo", 
        origin="Palembang", 
        destination="Medan", 
        date=date(2026, 8, 7), 
        existing_volume_m3=10.2, 
        existing_weight_tons=7.6
    ),
    ContainerSlotDB(
        slot_id="CTN-PNK-002", 
        company_id="CMP-0715", 
        company_name="PT Angin Mamiri Freight", 
        origin="Pontianak", 
        destination="Palembang", 
        date=date(2026, 8, 8), 
        existing_volume_m3=17.5, 
        existing_weight_tons=12.5
    ),
    ContainerSlotDB(
        slot_id="CTN-BTM-003", 
        company_id="CMP-1050", 
        company_name="PT Nusa Dua Cargo", 
        origin="Batam", 
        destination="Pekanbaru", 
        date=date(2026, 8, 11), 
        existing_volume_m3=6.4, 
        existing_weight_tons=5.2
    ),
    ContainerSlotDB(
        slot_id="CTN-MND-002", 
        company_id="CMP-1123", 
        company_name="PT Garuda Logistics Group", 
        origin="Manado", 
        destination="Manado", 
        date=date(2026, 8, 12), 
        existing_volume_m3=13.7, 
        existing_weight_tons=10.1
    ),
    ContainerSlotDB(
        slot_id="CTN-AMB-002", 
        company_id="CMP-1299", 
        company_name="CV Inti Raya Ekspedisi", 
        origin="Ambon", 
        destination="Bandung", 
        date=date(2026, 8, 13), 
        existing_volume_m3=21.0, 
        existing_weight_tons=15.0
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-014", 
        company_id="CMP-0091", 
        company_name="PT Sumber Makmur Logistik", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 15), 
        existing_volume_m3=28.3, 
        existing_weight_tons=19.9
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-006", 
        company_id="CMP-0114", 
        company_name="CV Bintang Cargo", 
        origin="Surabaya", 
        destination="Jakarta", 
        date=date(2026, 7, 16), 
        existing_volume_m3=2.6, 
        existing_weight_tons=2.8
    ),
    ContainerSlotDB(
        slot_id="CTN-SMG-006", 
        company_id="CMP-0157", 
        company_name="PT Cipta Logistindo", 
        origin="Semarang", 
        destination="Makassar", 
        date=date(2026, 7, 17), 
        existing_volume_m3=9.9, 
        existing_weight_tons=7.7
    ),
    ContainerSlotDB(
        slot_id="CTN-MDN-005", 
        company_id="CMP-0203", 
        company_name="PT Trans Nusantara", 
        origin="Medan", 
        destination="Batam", 
        date=date(2026, 7, 18), 
        existing_volume_m3=17.2, 
        existing_weight_tons=12.6
    ),
    ContainerSlotDB(
        slot_id="CTN-MKS-005", 
        company_id="CMP-0248", 
        company_name="UD Sejahtera Abadi", 
        origin="Makassar", 
        destination="Balikpapan", 
        date=date(2026, 7, 19), 
        existing_volume_m3=24.5, 
        existing_weight_tons=17.5
    ),
    ContainerSlotDB(
        slot_id="CTN-BPN-004", 
        company_id="CMP-0311",
        company_name="PT Andalan Ekspedisi",
        origin="Balikpapan",
        destination="Denpasar",
        date=date(2026, 7, 20),
        existing_volume_m3=31.8,
        existing_weight_tons=0.4
    ),
    ContainerSlotDB(
        slot_id="CTN-BDJ-003",
        company_id="CMP-0401",
        company_name="PT Borneo Express Line",
        origin="Banjarmasin",
        destination="Semarang",
        date=date(2026, 7, 21),
        existing_volume_m3=6.1,
        existing_weight_tons=5.3
    ),
    ContainerSlotDB(
        slot_id="CTN-DPS-004",
        company_id="CMP-0512",
        company_name="PT FastFlow Trans",
        origin="Denpasar",
        destination="Banjarmasin",
        date=date(2026, 7, 22),
        existing_volume_m3=13.4,
        existing_weight_tons=10.2
    ),
    ContainerSlotDB(
        slot_id="CTN-PLM-004", 
        company_id="CMP-0620", 
        company_name="CV Priangan Cargo", 
        origin="Palembang", 
        destination="Medan", 
        date=date(2026, 7, 23), 
        existing_volume_m3=20.7, 
        existing_weight_tons=15.1
    ),
    ContainerSlotDB(
        slot_id="CTN-PNK-003", 
        company_id="CMP-0715", 
        company_name="PT Angin Mamiri Freight", 
        origin="Pontianak", 
        destination="Palembang", 
        date=date(2026, 7, 24), 
        existing_volume_m3=28.0, 
        existing_weight_tons=20.0
    ),
    ContainerSlotDB(
        slot_id="CTN-MKS-039", 
        company_id="CMP-0248", 
        company_name="UD Sejahtera Abadi", 
        origin="Makassar", 
        destination="Balikpapan", 
        date=date(2026, 7, 19), 
        existing_volume_m3=18.5, 
        existing_weight_tons=8.5
    ),
    ContainerSlotDB(
        slot_id="CTN-BPN-038", 
        company_id="CMP-0311", 
        company_name="PT Andalan Ekspedisi", 
        origin="Balikpapan", 
        destination="Denpasar", 
        date=date(2026, 7, 20), 
        existing_volume_m3=25.8, 
        existing_weight_tons=13.4
),
    ContainerSlotDB(
        slot_id="CTN-BDJ-037", 
        company_id="CMP-0401", 
        company_name="PT Borneo Express Line", 
        origin="Banjarmasin", 
        destination="Semarang", 
        date=date(2026, 7, 21), 
        existing_volume_m3=0.1, 
        existing_weight_tons=18.3
    ),
    ContainerSlotDB(
        slot_id="CTN-DPS-038", 
        company_id="CMP-0512", 
        company_name="PT FastFlow Trans", 
        origin="Denpasar", 
        destination="Banjarmasin", 
        date=date(2026, 7, 22), 
        existing_volume_m3=7.4, 
        existing_weight_tons=1.2
    ),
    ContainerSlotDB(
        slot_id="CTN-PLM-038", 
        company_id="CMP-0620", 
        company_name="CV Priangan Cargo", 
        origin="Palembang", 
        destination="Medan", 
        date=date(2026, 7, 23), 
        existing_volume_m3=14.7, 
        existing_weight_tons=6.1
    ),
    ContainerSlotDB(
        slot_id="CTN-PNK-037", 
        company_id="CMP-0715", 
        company_name="PT Angin Mamiri Freight", 
        origin="Pontianak", 
        destination="Palembang", 
        date=date(2026, 7, 24), 
        existing_volume_m3=22.0, 
        existing_weight_tons=11.0
    ),
    ContainerSlotDB(
        slot_id="CTN-PKU-038", 
        company_id="CMP-0888", 
        company_name="PT Samudera Jaya Logistik", 
        origin="Pekanbaru", 
        destination="Pontianak", 
        date=date(2026, 7, 25), 
        existing_volume_m3=29.3, 
        existing_weight_tons=15.9
    ),
    ContainerSlotDB(
        slot_id="CTN-BDG-039", 
        company_id="CMP-0942", 
        company_name="CV Merdeka Transport", 
        origin="Bandung", 
        destination="Ambon", 
        date=date(2026, 7, 26), 
        existing_volume_m3=3.6, 
        existing_weight_tons=20.8
    ),
    ContainerSlotDB(
        slot_id="CTN-BTM-038", 
        company_id="CMP-1050", 
        company_name="PT Nusa Dua Cargo", 
        origin="Batam", 
        destination="Pekanbaru", 
        date=date(2026, 7, 27), 
        existing_volume_m3=10.9, 
        existing_weight_tons=3.7
    ),
    ContainerSlotDB(
        slot_id="CTN-MND-036", 
        company_id="CMP-1123", 
        company_name="PT Garuda Logistics Group", 
        origin="Manado", 
        destination="Manado", 
        date=date(2026, 7, 28), 
        existing_volume_m3=18.2, 
        existing_weight_tons=8.6
    ),
    ContainerSlotDB(
        slot_id="CTN-AMB-037", 
        company_id="CMP-1299", 
        company_name="CV Inti Raya Ekspedisi", 
        origin="Ambon", 
        destination="Bandung", 
        date=date(2026, 7, 29), 
        existing_volume_m3=25.5, 
        existing_weight_tons=13.5
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-049", 
        company_id="CMP-0091", 
        company_name="PT Sumber Makmur Logistik", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 30), 
        existing_volume_m3=32.8, 
        existing_weight_tons=18.4
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-041", 
        company_id="CMP-0114", 
        company_name="CV Bintang Cargo", 
        origin="Surabaya", 
        destination="Jakarta", 
        date=date(2026, 7, 31), 
        existing_volume_m3=7.1, 
        existing_weight_tons=1.3
    ),
    ContainerSlotDB(
        slot_id="CTN-SMG-041", 
        company_id="CMP-0157", 
        company_name="PT Cipta Logistindo", 
        origin="Semarang", 
        destination="Makassar", 
        date=date(2026, 8, 1), 
        existing_volume_m3=14.4, 
        existing_weight_tons=6.2
    ),
    ContainerSlotDB(
        slot_id="CTN-MDN-040", 
        company_id="CMP-0203", 
        company_name="PT Trans Nusantara", 
        origin="Medan", 
        destination="Batam", 
        date=date(2026, 8, 2), 
        existing_volume_m3=21.7, 
        existing_weight_tons=11.1
    ),
    ContainerSlotDB(
        slot_id="CTN-MKS-040", 
        company_id="CMP-0248", 
        company_name="UD Sejahtera Abadi", 
        origin="Makassar", 
        destination="Balikpapan", 
        date=date(2026, 8, 3), 
        existing_volume_m3=29.0, 
        existing_weight_tons=16.0
    ),
    ContainerSlotDB(
        slot_id="CTN-BPN-039", 
        company_id="CMP-0311", 
        company_name="PT Andalan Ekspedisi", 
        origin="Balikpapan", 
        destination="Denpasar", 
        date=date(2026, 8, 4), 
        existing_volume_m3=3.3, 
        existing_weight_tons=20.9
    ),
    ContainerSlotDB(
        slot_id="CTN-BDJ-038", 
        company_id="CMP-0401", 
        company_name="PT Borneo Express Line", 
        origin="Banjarmasin", 
        destination="Semarang", 
        date=date(2026, 8, 5), 
        existing_volume_m3=10.6, 
        existing_weight_tons=3.8
    ),
    ContainerSlotDB(
        slot_id="CTN-DPS-039", 
        company_id="CMP-0512", 
        company_name="PT FastFlow Trans", 
        origin="Denpasar", 
        destination="Banjarmasin", 
        date=date(2026, 8, 6), 
        existing_volume_m3=17.9, 
        existing_weight_tons=8.7
    ),
    ContainerSlotDB(
        slot_id="CTN-PNK-038", 
        company_id="CMP-0715", 
        company_name="PT Angin Mamiri Freight", 
        origin="Pontianak", 
        destination="Palembang", 
        date=date(2026, 8, 8), 
        existing_volume_m3=32.5, 
        existing_weight_tons=18.5
    ),
    ContainerSlotDB(
        slot_id="CTN-PKU-039", 
        company_id="CMP-0888", 
        company_name="PT Samudera Jaya Logistik", 
        origin="Pekanbaru", 
        destination="Pontianak", 
        date=date(2026, 8, 9), 
        existing_volume_m3=6.8, 
        existing_weight_tons=1.4
    ),
    ContainerSlotDB(
        slot_id="CTN-BDG-040", 
        company_id="CMP-0942", 
        company_name="CV Merdeka Transport", 
        origin="Bandung", 
        destination="Ambon", 
        date=date(2026, 8, 10), 
        existing_volume_m3=14.1, 
        existing_weight_tons=6.3
    ),
    ContainerSlotDB(
        slot_id="CTN-BTM-039", 
        company_id="CMP-1050", 
        company_name="PT Nusa Dua Cargo", 
        origin="Batam", 
        destination="Pekanbaru", 
        date=date(2026, 8, 11), 
        existing_volume_m3=21.4, 
        existing_weight_tons=11.2
    ),
    ContainerSlotDB(
        slot_id="CTN-MND-037", 
        company_id="CMP-1123", 
        company_name="PT Garuda Logistics Group", 
        origin="Manado", 
        destination="Manado", 
        date=date(2026, 8, 12), 
        existing_volume_m3=28.7, 
        existing_weight_tons=16.1
    ),
    ContainerSlotDB(
        slot_id="CTN-AMB-038", 
        company_id="CMP-1299", 
        company_name="CV Inti Raya Ekspedisi", 
        origin="Ambon", 
        destination="Bandung", 
        date=date(2026, 8, 13), 
        existing_volume_m3=3.0, 
        existing_weight_tons=21.0
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-050", 
        company_id="CMP-0091", 
        company_name="PT Sumber Makmur Logistik", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 15), 
        existing_volume_m3=10.3, 
        existing_weight_tons=3.9
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-042", 
        company_id="CMP-0114", 
        company_name="CV Bintang Cargo", 
        origin="Surabaya", 
        destination="Jakarta", 
        date=date(2026, 7, 16), 
        existing_volume_m3=17.6, 
        existing_weight_tons=8.8
    ),
    ContainerSlotDB(
        slot_id="CTN-SMG-042", 
        company_id="CMP-0157", 
        company_name="PT Cipta Logistindo", 
        origin="Semarang", 
        destination="Makassar", 
        date=date(2026, 7, 17), 
        existing_volume_m3=24.9, 
        existing_weight_tons=13.7
    ),
    ContainerSlotDB(
        slot_id="CTN-MDN-041", 
        company_id="CMP-0203", 
        company_name="PT Trans Nusantara", 
        origin="Medan", 
        destination="Batam", 
        date=date(2026, 7, 18), 
        existing_volume_m3=32.2, 
        existing_weight_tons=18.6
    ),
    ContainerSlotDB(
        slot_id="CTN-DPS-040", 
        company_id="CMP-0512", 
        company_name="PT FastFlow Trans", 
        origin="Denpasar", 
        destination="Banjarmasin", 
        date=date(2026, 7, 22), 
        existing_volume_m3=28.4, 
        existing_weight_tons=16.2
    ),
    ContainerSlotDB(
        slot_id="CTN-PLM-040", 
        company_id="CMP-0620", 
        company_name="CV Priangan Cargo", 
        origin="Palembang", 
        destination="Medan", 
        date=date(2026, 7, 23), 
        existing_volume_m3=2.7, 
        existing_weight_tons=21.1
    ),
    ContainerSlotDB(
        slot_id="CTN-PNK-039", 
        company_id="CMP-0715", 
        company_name="PT Angin Mamiri Freight", 
        origin="Pontianak", 
        destination="Palembang", 
        date=date(2026, 7, 24), 
        existing_volume_m3=10.0, 
        existing_weight_tons=4.0
    ),
    ContainerSlotDB(
        slot_id="CTN-PKU-040", 
        company_id="CMP-0888", 
        company_name="PT Samudera Jaya Logistik", 
        origin="Pekanbaru", 
        destination="Pontianak", 
        date=date(2026, 7, 25), 
        existing_volume_m3=17.3, 
        existing_weight_tons=8.9
    ),
    ContainerSlotDB(
        slot_id="CTN-BDG-041", 
        company_id="CMP-0942", 
        company_name="CV Merdeka Transport", 
        origin="Bandung", 
        destination="Ambon", 
        date=date(2026, 7, 26), 
        existing_volume_m3=24.6, 
        existing_weight_tons=14.8
    ),
    ContainerSlotDB(
        slot_id="CTN-BTM-040", 
        company_id="CMP-1050", 
        company_name="PT Nusa Dua Cargo", 
        origin="Batam", 
        destination="Pekanbaru", 
        date=date(2026, 7, 27), 
        existing_volume_m3=31.9, 
        existing_weight_tons=18.7
    ),
    ContainerSlotDB(
        slot_id="CTN-MND-038", 
        company_id="CMP-1123", 
        company_name="PT Garuda Logistics Group", 
        origin="Manado", 
        destination="Manado", 
        date=date(2026, 7, 28), 
        existing_volume_m3=6.2, 
        existing_weight_tons=1.6
    ),
    ContainerSlotDB(
        slot_id="CTN-AMB-039", 
        company_id="CMP-1299", 
        company_name="CV Inti Raya Ekspedisi", 
        origin="Ambon", 
        destination="Bandung", 
        date=date(2026, 7, 29), 
        existing_volume_m3=13.5, 
        existing_weight_tons=6.5
    ),
    ContainerSlotDB(
        slot_id="CTN-JKT-051", 
        company_id="CMP-0091", 
        company_name="PT Sumber Makmur Logistik", 
        origin="Jakarta", 
        destination="Surabaya", 
        date=date(2026, 7, 30), 
        existing_volume_m3=20.8, 
        existing_weight_tons=11.4
    ),
    ContainerSlotDB(
        slot_id="CTN-SBY-043", 
        company_id="CMP-0114", 
        company_name="CV Bintang Cargo", 
        origin="Surabaya", 
        destination="Jakarta", 
        date=date(2026, 7, 31), 
        existing_volume_m3=28.1, 
        existing_weight_tons=16.3
    ),
    ContainerSlotDB(
        slot_id="CTN-SMG-043", 
        company_id="CMP-0157", 
        company_name="PT Cipta Logistindo", 
        origin="Semarang", 
        destination="Makassar", 
        date=date(2026, 8, 1), 
        existing_volume_m3=2.4, 
        existing_weight_tons=21.2
    ),
    ContainerSlotDB(
        slot_id="CTN-MDN-042", 
        company_id="CMP-0203", 
        company_name="PT Trans Nusantara", 
        origin="Medan", 
        destination="Batam", 
        date=date(2026, 8, 2), 
        existing_volume_m3=9.7, 
        existing_weight_tons=4.1
    ),
    ContainerSlotDB(
        slot_id="CTN-MKS-042", 
        company_id="CMP-0248", 
        company_name="UD Sejahtera Abadi", 
        origin="Makassar", 
        destination="Balikpapan", 
        date=date(2026, 8, 3), 
        existing_volume_m3=17.0, 
        existing_weight_tons=9.0
    ),
    ContainerSlotDB(
        slot_id="CTN-BPN-041", 
        company_id="CMP-0311", 
        company_name="PT Andalan Ekspedisi", 
        origin="Balikpapan", 
        destination="Denpasar", 
        date=date(2026, 8, 4), 
        existing_volume_m3=24.3, 
        existing_weight_tons=13.9
    ),
    ContainerSlotDB(
        slot_id="CTN-BDJ-040", 
        company_id="CMP-0401", 
        company_name="PT Borneo Express Line", 
        origin="Banjarmasin", 
        destination="Semarang", 
        date=date(2026, 8, 5), 
        existing_volume_m3=31.6, 
        existing_weight_tons=18.8
    ),
    ContainerSlotDB(
        slot_id="CTN-DPS-041", 
        company_id="CMP-0512", 
        company_name="PT FastFlow Trans", 
        origin="Denpasar", 
        destination="Banjarmasin", 
        date=date(2026, 8, 6), 
        existing_volume_m3=5.9, 
        existing_weight_tons=1.7
    ),
    ContainerSlotDB(
        slot_id="CTN-PLM-041", 
        company_id="CMP-0620", 
        company_name="CV Priangan Cargo", 
        origin="Palembang", 
        destination="Medan", 
        date=date(2026, 8, 7), 
        existing_volume_m3=13.2, 
        existing_weight_tons=6.6
    ),
]