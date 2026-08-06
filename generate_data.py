import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# 1. TEMPLATE RAW TEXT VARIASI JIKA ADA YANG DIPERLUKAN UNTUK DITAMBAHKAN


RAW_TEXT_TEMPLATES = [
   
    "{qty} {unit} {raw_item_name} dari {orig_code} ke {dest_code}",
    "{qty} {unit} {raw_item_name} {orig_name} ke {dest_name} tgl {date_str}",
    "{qty} {unit} {raw_item_name} rute {orig_code}-{dest_code} brt {weight}",
    "{qty} {unit} {raw_item_name} {orig_code} ke {dest_code} berat total {weight} tgl {date_str}",
    "{raw_item_name} {qty} {unit} dari {orig_name} ke {dest_name}",
    "{raw_item_name} ({qty} {unit}) rute {orig_code} -> {dest_code} {date_str}",

    "{prefix} {qty} {unit} {raw_item_name} dari {orig_code} ke {dest_code} tgl {date_str}",
    "{prefix} {raw_item_name} {qty} {unit} ke {dest_name} dari {orig_name}",
    "{prefix} {raw_item_name} {qty} {unit} kirim dari {orig_code} ke {dest_code} tgl {date_str} brt {weight}",
    "{prefix} {qty} {unit} {raw_item_name} {orig_code} ke {dest_code} berat {weight}",
    "Tgl {date_str} mau kirim {weight} {raw_item_name} ({qty} {unit}) dari {orig_code} ke {dest_code}",
    
    "ORDER: {raw_item_name} | QTY: {qty} {unit} | WEIGHT: {weight} | ROUTE: {orig_name} -> {dest_name} | DATE: {date_str}",
    "[{orig_code}-{dest_code}] {raw_item_name} - {qty} {unit} ({weight}) - {date_str}",
    "Pengiriman {raw_item_name} ({qty} {unit} / {weight}) rute {orig_name} ke {dest_name} tanggal {date_str}",
    "MANIFEST: {qty} {unit} {raw_item_name} | ASAL: {orig_code} | TUJUAN: {dest_code} | TGL: {date_str}",
]

# 2. DAFAR PREFIXES & UNITS SUPER VARIAN 


PREFIXES = [
   
    "", "", "", "", "", "",
    
    # --- Gaya Perintah Formal ---
    "Kirim", "Kirimkan", "Tolong kirim", "Tolong kirimkan", "Bantu kirim", "Minta tolong kirim",
    "Tolong proses", "Proses pengiriman", "Proseskan", "Tolong catat", "Catat pengiriman",
    "Tolong daftarkan", "Daftarkan", "Input pengiriman", "Masukkan data", "Catat manifest",
    "Kerjakan pengiriman", "Tolong inputkan", "Input manifest", "Mohon diproses",
    
    # --- Gaya Chat Santai ---
    "Krm", "Krmkan", "Kirim dong", "Bisa kirim", "Tolong dibantu kirim",
    "Gan kirim", "Mas tolong kirim", "Min tolong kirim", "Bos kirim", "Bro tolong kirim",
    "Mas kirim", "Gan tolong", "Min kirim", "Bos tolong", "Pak kirimkan", "Om tolong kirim",
    
    # --- Tag Ekspedisi ---
    "CARGO:", "MANIFEST:", "ORDER:", "SHIPMENT:", "PENGIRIMAN:", "PO:", "SJ:",
    "Info pengiriman:", "Detail pengiriman:", "Data kiriman:", "Daftar barang:", "Info manifest:"
]

# --- satuan units ---


UNITS = [
    "koli", "dus", "box", "pcs", "pack", "pak", "karton", "galon", "kg", "ton", 
    "btl", "botol", "karung", "roll", "rol", "drum", "palet", "pallet", "ikat", 
    "slop", "bal", "keranjang", "kaleng", "can", "unit", "set", "pouch", "sak"
]

# --- DATA ACUAN KOTA & BARANG ---


LOCATIONS = [
    ("JKT", "Jakarta"), ("SBY", "Surabaya"), ("BDG", "Bandung"), 
    ("MES", "Medan"), ("SUB", "Surabaya"), ("BPN", "Balikpapan"), 
    ("UPG", "Makassar"), ("DPS", "Denpasar"), ("JOG", "Yogyakarta"), 
    ("PKU", "Pekanbaru"), ("BTM", "Batam"), ("PLM", "Palembang"),
    ("SRG", "Semarang"), ("MDC", "Manado"), ("PNK", "Pontianak")
]

SAFE_ITEMS = [
    ("miyak goreng bimoli", "minyak goreng bimoli"),
    ("kaos oblong katun 30s", "kaos oblong katun"),
    ("sepatu sneakers lokal", "sepatu sneakers"),
    ("kertas A4 80gr paperone", "kertas A4"),
    ("pakaian bekas / baju thrift", "pakaian bekas"),
    ("sparepart motor non aki", "sparepart motor"),
    ("susu kotak uht ultra", "susu UHT"),
    ("buku tulis sekolah sidu", "buku tulis"),
    ("makanan kering biskuit", "makanan kering"),
    ("kosmetik skincare wajah", "kosmetik"),
    ("aksesoris hp casing", "aksesoris hp")
]

DANGEROUS_ITEMS = [
    ("tabung gas lpg 3kg isi full", "tabung gas LPG 3kg"),
    ("batre lithium ion 18650", "baterai lithium ion"),
    ("alkohol murni 70 persen", "alkohol 70%"),
    ("thinner cat avian tiner", "thinner cat"),
    ("cat semprot pylox pilok", "cat semprot"),
    ("racun tikus cair seng fosfida", "racun tikus"),
    ("pemutih pakaian bayclin clorox", "pemutih pakaian"),
    ("aki basah kendaraan motor", "aki basah"),
    ("korek api gas korek kayu", "korek api gas")
]

DATE_FORMATS = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d %b %Y", "%Y.%m.%d"]



def generate_random_date():
    start_date = datetime(2025, 1, 1)
    dt = start_date + timedelta(days=random.randint(0, 600))
    return dt.strftime(random.choice(DATE_FORMATS)), dt.strftime("%Y-%m-%d")


def build_raw_text(raw_item_name, orig_code, orig_name, dest_code, dest_name, qty, unit, weight, date_str):
    template = random.choice(RAW_TEXT_TEMPLATES)
    clean_weight = weight if weight else "0kg"
    prefix_text = random.choice(PREFIXES)
    
    formatted_text = template.format(
        raw_item_name=raw_item_name,
        orig_code=orig_code,
        orig_name=orig_name,
        dest_code=dest_code,
        dest_name=dest_name,
        qty=qty,
        unit=unit,
        weight=clean_weight,
        date_str=date_str,
        prefix=prefix_text
    )

    
    return " ".join(formatted_text.split())


def generate_dataset(start_id=1, count=10000):
    dataset = []
    for i in range(count):
        current_id = start_id + i
        is_dangerous = random.choice([True, False])
        raw_item_name, clean_item_name = random.choice(
            DANGEROUS_ITEMS if is_dangerous else SAFE_ITEMS
        )

        orig_code, orig_name = random.choice(LOCATIONS)
        dest_code, dest_name = random.choice(LOCATIONS)
        while dest_code == orig_code:
            dest_code, dest_name = random.choice(LOCATIONS)

        qty = random.randint(1, 1000)
        unit = random.choice(UNITS)
        weight = f"{random.randint(1, 500)}kg" if random.random() > 0.3 else None
        date_str, iso_date = generate_random_date()

        raw_text = build_raw_text(
            raw_item_name, orig_code, orig_name, dest_code, dest_name, 
            qty, unit, weight, date_str
        )

        dataset.append({
            "id": current_id,
            "raw_text": raw_text,
            "ground_truth": {
                "origin": orig_code,
                "destination": dest_code,
                "date": iso_date,
                "item": clean_item_name,
                "volume": f"{qty} {unit}",
                "weight": weight,
                "is_dangerous": is_dangerous,
            },
        })
    return dataset


if __name__ == "__main__":
    output_dir = Path("app/ml")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / "manifest_dataset.json"


    existing_data = []
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            print(f"📖 Ditemukan {len(existing_data)} data lama.")
        except json.decoder.JSONDecodeError:
            existing_data = []

    
    start_id = len(existing_data) + 1
    ADDITIONAL_COUNT = 7000
    
    print(f"⚙️ Memproses pembuatan {ADDITIONAL_COUNT} data variatif baru...")
    new_data = generate_dataset(start_id=start_id, count=ADDITIONAL_COUNT)

   
    total_data = existing_data + new_data

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(total_data, f, indent=2, ensure_ascii=False)

    print(f"➕ Berhasil menambahkan {ADDITIONAL_COUNT} data baru (ID {start_id} s/d {start_id + ADDITIONAL_COUNT - 1}).")
    print(f"✅ BINGO! Total akumulasi data sekarang: {len(total_data)} di '{file_path}'")