import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# ==============================================================================
# 1. TEMPLATE & VARIABEL PER MODE BAHASA (ID, EN, ZH, MIXED ID-EN)
# ==============================================================================

LANG_CONFIG = {
    # --- BAHASA INDONESIA FULL ---
    "id": {
        "templates": [
            "{prefix} {qty} {unit} {raw_item_name} dari {orig_code} ke {dest_code} tgl {date_str}",
            "{prefix} {qty} {unit} {raw_item_name} dari {orig_name} ke {dest_name}",
            "Pengiriman {raw_item_name} sebanyak {qty} {unit} rute {orig_code}-{dest_code} berat {weight} tgl {date_str}",
            "{qty} {unit} {raw_item_name} {orig_code} ke {dest_code} berat {weight}",
            "tolong kirim {raw_item_name} {qty} {unit} rute {orig_code}-{dest_code} tgl {date_str} brt {weight}",
            "ORDER: {raw_item_name} | QTY: {qty} {unit} | RUTE: {orig_name} -> {dest_name} | TGL: {date_str}",
            "[{orig_code}-{dest_code}] {raw_item_name} - {qty} {unit} ({weight}) - {date_str}",
        ],
        "prefixes": ["", "", "Kirim", "Tolong kirim", "Proses pengiriman", "Input pengiriman", "Mohon kirim", "CARGO:"],
        "units": ["dus", "box", "koli", "pcs", "karton", "botol", "karung", "pak", "galon", "kg", "ton", "roll", "drum", "palet"]
    },

    # --- BAHASA INGGRIS FULL ---
    "en": {
        "templates": [
            "{prefix} {qty} {unit} of {raw_item_name} from {orig_code} to {dest_code} date {date_str}",
            "{prefix} {qty} {unit} {raw_item_name} from {orig_name} to {dest_name}",
            "Shipment of {raw_item_name} ({qty} {unit}) route {orig_code}-{dest_code} on {date_str}",
            "{qty} {unit} {raw_item_name} deliver from {orig_code} to {dest_code} weight {weight}",
            "ORDER: {raw_item_name} | QTY: {qty} {unit} | ROUTE: {orig_name} -> {dest_name} | DATE: {date_str}",
            "MANIFEST: {qty} {unit} {raw_item_name} | ORIGIN: {orig_code} | DESTINATION: {dest_code} | DATE: {date_str}",
        ],
        "prefixes": ["", "", "Please send", "Please ship", "Dispatch", "Deliver", "Process shipment", "Urgent shipment"],
        "units": ["boxes", "cartons", "crates", "packages", "parcels", "bags", "barrels", "sacks", "pallets", "pcs", "units"]
    },

    # --- BAHASA MANDARIN FULL (MURNI CINA) ---
    "zh": {
        "templates": [
            "{prefix} {qty}{unit}{raw_item_name} 从{orig_code}到{dest_code} 日期 {date_str}",
            "{prefix} {qty}{unit} {raw_item_name} 从 {orig_name} 发往 {dest_name}",
            "{raw_item_name} {qty}{unit} {orig_code}至{dest_code} 重量{weight} 日期 {date_str}",
            "发货单: {raw_item_name} | 数量: {qty}{unit} | 重量: {weight} | 路线: {orig_name} -> {dest_name} | 日期: {date_str}",
            "{prefix} 寄 {qty}{unit} {raw_item_name} {orig_code} 到 {dest_code}"
        ],
        "prefixes": ["", "", "请发送", "请寄", "发货:", "托运", "请处理", "安排发货", "加急发货"],
        "units": ["箱", "包", "件", "个", "桶", "袋", "公斤", "吨", "卷", "托盘", "盒", "瓶"]
    },

    # --- MIXED INDONESIA - INGGRIS (INDONGLISH) ---
    "mixed": {
        "templates": [
            "{prefix} {qty} {unit} {raw_item_name} dari {orig_code} to {dest_code} tgl {date_str}",
            "Please kirim {qty} {unit} {raw_item_name} from {orig_name} ke {dest_name}",
            "Need to ship {raw_item_name} ({qty} {unit}) dari {orig_code} to {dest_code} weight {weight}",
            "Tolong process {qty} {unit} {raw_item_name} {orig_code} to {dest_code} date {date_str}",
            "Help process pengiriman {qty} {unit} {raw_item_name} from {orig_code} ke {dest_code}",
            "Request delivery {raw_item_name} {qty} {unit} rute {orig_code} ke {dest_code} weight {weight}"
        ],
        "prefixes": ["", "", "Please kirim", "Tolong send", "Help kirim", "Tolong process", "Need to ship", "Please inputkan"],
        "units": ["box", "pcs", "carton", "dus", "koli", "units", "packages", "pack"]
    }
}


# ==============================================================================
# 2. MASTER DATA BARANG (DENGAN STRUKTUR BAHASA TERPISAH)
# ==============================================================================

SAFE_ITEMS = [
    {
        "clean_name": "minyak goreng bimoli",
        "id": "minyak goreng bimoli",
        "en": "Bimoli cooking oil",
        "zh": "Bimoli食用油",
        "mixed": "cooking oil bimoli"
    },
    {
        "clean_name": "kaos oblong katun",
        "id": "kaos oblong katun 30s",
        "en": "cotton t-shirt 30s",
        "zh": "纯棉T恤衫",
        "mixed": "kaos cotton t-shirt"
    },
    {
        "clean_name": "sepatu sneakers",
        "id": "sepatu sneakers lokal",
        "en": "casual sneakers shoes",
        "zh": "休闲运动鞋",
        "mixed": "sepatu sneakers shoes"
    },
    {
        "clean_name": "kertas A4",
        "id": "kertas A4 80gr paperone",
        "en": "A4 printing paper 80gsm",
        "zh": "A4打印纸 80克",
        "mixed": "paperone paper A4 80gr"
    },
    {
        "clean_name": "pakaian bekas",
        "id": "pakaian bekas / baju thrift",
        "en": "secondhand clothes",
        "zh": "二手衣服",
        "mixed": "thrifted baju bekas"
    },
    {
        "clean_name": "sparepart motor",
        "id": "sparepart motor non aki",
        "en": "motorcycle spare parts no battery",
        "zh": "摩托车零配件 非电池",
        "mixed": "sparepart motor no battery"
    },
    {
        "clean_name": "susu UHT",
        "id": "susu kotak uht ultra",
        "en": "Ultra UHT milk carton",
        "zh": "Ultra利乐包纯牛奶",
        "mixed": "ultra uht milk kotak"
    },
    {
        "clean_name": "buku tulis",
        "id": "buku tulis sekolah sidu",
        "en": "Sidu school notebook",
        "zh": "Sidu学生练习本",
        "mixed": "buku tulis notebook sidu"
    },
    {
        "clean_name": "makanan kering",
        "id": "makanan kering biskuit",
        "en": "dry biscuit food",
        "zh": "饼干干粮",
        "mixed": "dry food biskuit"
    },
    {
        "clean_name": "kosmetik",
        "id": "kosmetik skincare wajah",
        "en": "facial skincare cosmetics",
        "zh": "护肤化妆品",
        "mixed": "skincare cosmetic wajah"
    }
]

DANGEROUS_ITEMS = [
    {
        "clean_name": "tabung gas LPG 3kg",
        "id": "tabung gas lpg 3kg isi full",
        "en": "full 3kg LPG gas cylinder",
        "zh": "3kg液化气钢瓶",
        "mixed": "LPG gas tank 3kg isi full"
    },
    {
        "clean_name": "baterai lithium ion",
        "id": "batre lithium ion 18650",
        "en": "18650 lithium ion battery pack",
        "zh": "18650锂电池包",
        "mixed": "lithium ion battery 18650"
    },
    {
        "clean_name": "alkohol 70%",
        "id": "alkohol murni 70 persen",
        "en": "pure 70 percent alcohol disinfectant",
        "zh": "70%医用消毒酒精",
        "mixed": "pure alcohol 70 persen"
    },
    {
        "clean_name": "thinner cat",
        "id": "thinner cat avian tiner",
        "en": "Avian paint thinner liquid",
        "zh": "Avian油漆稀释剂",
        "mixed": "paint thinner avian"
    },
    {
        "clean_name": "cat semprot",
        "id": "cat semprot pylox pilok",
        "en": "Pylox aerosol spray paint",
        "zh": "Pylox自动喷漆",
        "mixed": "spray paint pylox pilok"
    },
    {
        "clean_name": "racun tikus",
        "id": "racun tikus cair seng fosfida",
        "en": "liquid rat poison zinc phosphide",
        "zh": "液体灭鼠药",
        "mixed": "liquid rat poison racun tikus"
    },
    {
        "clean_name": "pemutih pakaian",
        "id": "pemutih pakaian bayclin clorox",
        "en": "Bayclin clothes bleach liquid",
        "zh": "Bayclin漂白水",
        "mixed": "bleach pemutih pakaian bayclin"
    },
    {
        "clean_name": "aki basah",
        "id": "aki basah kendaraan motor",
        "en": "wet lead acid battery for motorcycle",
        "zh": "摩托车铅酸水电池",
        "mixed": "wet battery aki motor"
    },
    {
        "clean_name": "korek api gas",
        "id": "korek api gas isi ulang",
        "en": "gas lighter refill container",
        "zh": "气体打火机",
        "mixed": "gas lighter korek api"
    }
]

LOCATIONS = [
    ("JKT", "Jakarta"), ("SBY", "Surabaya"), ("BDG", "Bandung"), 
    ("MES", "Medan"), ("SUB", "Surabaya"), ("BPN", "Balikpapan"), 
    ("UPG", "Makassar"), ("DPS", "Denpasar"), ("JOG", "Yogyakarta"), 
    ("PKU", "Pekanbaru"), ("BTM", "Batam"), ("PLM", "Palembang"),
    ("SRG", "Semarang"), ("MDC", "Manado"), ("PNK", "Pontianak")
]

DATE_FORMATS = [
    "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d %b %Y", "%Y.%m.%d",
    "%d/%m/%y", "%d-%m-%y"
]


# ==============================================================================
# 3. LOGIKA GENERATOR
# ==============================================================================

def generate_random_date():
    start_date = datetime(2025, 1, 1)
    dt = start_date + timedelta(days=random.randint(0, 600))
    fmt = random.choice(DATE_FORMATS)
    date_str = dt.strftime(fmt)
    
    # Kadang ubah nama bulan ke Bahasa Indonesia
    months_id = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agt", "Sep", "Okt", "Nov", "Des"]
    if random.random() < 0.2:
        date_str = f"{dt.day} {months_id[dt.month-1]} {dt.year}"
        
    return date_str, dt.strftime("%Y-%m-%d")


def build_raw_text(lang_mode, raw_item_name, orig_code, orig_name, dest_code, dest_name, qty, unit, weight, date_str):
    cfg = LANG_CONFIG[lang_mode]
    template = random.choice(cfg["templates"])
    prefix_text = random.choice(cfg["prefixes"])
    clean_weight = weight if weight else ""

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
    
    # Rapikan spasi ganda / spasi berlebih
    return " ".join(formatted_text.split())


def generate_dataset(start_id=1, count=5000):
    dataset = []
    
    # Rasio presisi 50:50 dangerous vs safe
    half_count = count // 2
    is_dangerous_list = [True] * half_count + [False] * (count - half_count)
    random.shuffle(is_dangerous_list)

    # Distribusi Bahasa: ID (30%), EN (25%), ZH (25%), MIXED ID-EN (20%)
    lang_modes = ["id", "en", "zh", "mixed"]
    lang_weights = [0.30, 0.25, 0.25, 0.20]

    for i in range(count):
        current_id = start_id + i
        is_dangerous = is_dangerous_list[i]
        
        # Pilih Mode Bahasa untuk baris data ini
        lang_mode = random.choices(lang_modes, weights=lang_weights, k=1)[0]
        
        # Pilih Barang sesuai daftar
        item_obj = random.choice(DANGEROUS_ITEMS if is_dangerous else SAFE_ITEMS)
        clean_item_name = item_obj["clean_name"]
        raw_item_name = item_obj[lang_mode]  # Ambil nama barang spesifik untuk mode bahasa ini

        # Lokasi
        orig_code, orig_name = random.choice(LOCATIONS)
        dest_code, dest_name = random.choice(LOCATIONS)
        while dest_code == orig_code:
            dest_code, dest_name = random.choice(LOCATIONS)

        qty = random.randint(1, 1000)
        unit = random.choice(LANG_CONFIG[lang_mode]["units"])
        weight = f"{random.randint(1, 500)}kg" if random.random() > 0.3 else None
        date_str, iso_date = generate_random_date()

        raw_text = build_raw_text(
            lang_mode, raw_item_name, orig_code, orig_name, dest_code, dest_name, 
            qty, unit, weight, date_str
        )

        dataset.append({
            "id": current_id,
            "raw_text": raw_text,
            "ground_truth": {
                "origin": orig_code,
                "destination": dest_code,
                "date": iso_date,
                "item": clean_item_name,  # Tetap standar baku Bahasa Indonesia
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

    TOTAL_COUNT = 5000  # Jumlah total data
    
    print(f"⚙️ Memproses pembuatan TEPAT {TOTAL_COUNT} data...")
    print("   - Bahasa Indonesia Full: ~30%")
    print("   - Bahasa Inggris Full: ~25%")
    print("   - Bahasa Mandarin Full: ~25%")
    print("   - Mixed Indo-English: ~20%")

    clean_data = generate_dataset(start_id=1, count=TOTAL_COUNT)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Selesai! File '{file_path}' berhasil diperbarui dengan {len(clean_data)} data yang rapi.")