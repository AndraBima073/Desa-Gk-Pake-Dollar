import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Lokasi & Kodifikasi
LOCATIONS = [
    ("JKT", "Jakarta"), ("SBY", "Surabaya"), ("BDG", "Bandung"), 
    ("MES", "Medan"), ("SUB", "Surabaya"), ("BPN", "Balikpapan"), 
    ("UPG", "Makassar"), ("DPS", "Denpasar"), ("JOG", "Yogyakarta"), 
    ("PKU", "Pekanbaru"), ("BTM", "Batam"), ("PLM", "Palembang"),
    ("SRG", "Semarang"), ("MDC", "Manado"), ("PNK", "Pontianak")
]

# Barang Aman (General Cargo)
SAFE_ITEMS = [
    ("miyak goreng bimoli", "minyak goreng bimoli"),
    ("minyak kelapa sawit", "minyak kelapa sawit"),
    ("kaos oblong katun 30s", "kaos oblong katun"),
    ("sepatu sneakers lokal", "sepatu sneakers"),
    ("kertas A4 80gr paperone", "kertas A4"),
    ("kerupuk udang renyah", "kerupuk udang"),
    ("buku tulis sekolah sidu", "buku tulis"),
    ("susu kotak uht ultra", "susu UHT"),
    ("kopi bubuk kapal api", "kopi bubuk"),
    ("pakaian bekas / baju thrift", "pakaian bekas"),
    ("sparepart motor non aki", "sparepart motor")
]

# Barang Berbahaya (Hazmat)
DANGEROUS_ITEMS = [
    ("minyak tanah murni 1L", "minyak tanah"),
    ("minyak tnh cair", "minyak tanah"),
    ("batre lithium ion 18650", "baterai lithium ion"),
    ("btre litium 5000mah laptop", "baterai lithium"),
    ("tabung gas lpg 3kg isi full", "tabung gas LPG 3kg"),
    ("alkohol murni 70 persen", "alkohol 70%"),
    ("thinner cat avian tiner", "thinner cat"),
    ("cat semprot pylox pilok", "cat semprot"),
    ("racun tikus cair seng fosfida", "racun tikus"),
    ("pemutih pakaian bayclin clorox", "pemutih pakaian")
]

DATE_FORMATS = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d %b %Y", "%Y.%m.%d"]
PREFIXES = ["Krim", "Kirim", "Pengiriman:", "Kiriman urgent", "Tolong kirim", "CARGO:", "Krm"]
UNITS = ["btl", "karton", "koli", "pcs", "box", "galon", "kg", "ton", "dus"]

def generate_random_date():
    start_date = datetime(2025, 1, 1)
    dt = start_date + timedelta(days=random.randint(0, 600))
    return dt.strftime(random.choice(DATE_FORMATS)), dt.strftime("%Y-%m-%d")

def generate_dataset(total_count=5000):
    dataset = []
    for i in range(total_count):
        is_dangerous = random.choice([True, False])
        raw_item_name, clean_item_name = random.choice(DANGEROUS_ITEMS if is_dangerous else SAFE_ITEMS)
        
        orig_code, orig_name = random.choice(LOCATIONS)
        dest_code, dest_name = random.choice(LOCATIONS)
        while dest_code == orig_code:
            dest_code, dest_name = random.choice(LOCATIONS)
            
        qty = random.randint(1, 1000)
        unit = random.choice(UNITS)
        weight = f"{random.randint(1, 500)}kg" if random.random() > 0.3 else None
        date_str, iso_date = generate_random_date()
        
        raw_text = f"{random.choice(PREFIXES)} {qty} {unit} {raw_item_name} dari {orig_code} ke {dest_code} tgl {date_str}"
        if weight:
            raw_text += f" brt {weight}"

        dataset.append({
            "id": i + 1,
            "raw_text": raw_text,
            "ground_truth": {
                "origin": orig_code,
                "destination": dest_code,
                "date": iso_date,
                "item": clean_item_name,
                "volume": f"{qty} {unit}",
                "weight": weight,
                "is_dangerous": is_dangerous
            }
        })
    return dataset

if __name__ == "__main__":
    data = generate_dataset(5000)
    output_dir = Path("app/ml")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / "manifest_dataset.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ BINGO! Berhasil membuat {len(data)} data di '{file_path}'")