"""Static reference data for the self-hosted (no external API) shipment
intelligence pipeline: a city/port gazetteer for origin/destination
matching, and a labeled training set for the dangerous-goods safety
classifier. Andra: extend `DANGEROUS_GOODS_TRAINING_DATA` with real
labeled examples (or swap it for a proper dataset) to retrain the
classifier in `app/ml/safety_classifier.py` — nothing else needs to change.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# City / port gazetteer. Keys are canonical names (as used in
# app.database.MOCK_CONTAINER_DB); values are alternate spellings/aliases
# that should resolve to the same canonical city during extraction.
# ---------------------------------------------------------------------------
CITY_ALIASES: dict[str, list[str]] = {
    "Jakarta": ["jakarta", "jkt", "dki jakarta", "jakarta pusat", "jakarta utara"],
    "Surabaya": ["surabaya", "sby"],
    "Makassar": ["makassar", "ujung pandang", "mks"],
    "Semarang": ["semarang", "smg"],
    "Balikpapan": ["balikpapan", "bpp"],
    "Medan": ["medan", "mdn"],
    "Bandung": ["bandung", "bdg"],
    "Yogyakarta": ["yogyakarta", "jogja", "yogya", "diy"],
    "Solo": ["solo", "surakarta"],
    "Denpasar": ["denpasar", "bali", "dps"],
    "Palembang": ["palembang", "plg"],
    "Batam": ["batam"],
    "Pekanbaru": ["pekanbaru", "riau"],
    "Padang": ["padang"],
    "Banjarmasin": ["banjarmasin", "bjm"],
    "Pontianak": ["pontianak", "ptk"],
    "Manado": ["manado"],
    "Ambon": ["ambon"],
    "Jayapura": ["jayapura", "papua"],
    "Malang": ["malang"],
    "Cirebon": ["cirebon"],
    "Bekasi": ["bekasi"],
    "Tangerang": ["tangerang"],
    "Bogor": ["bogor"],
    "Depok": ["depok"],
    "Lampung": ["lampung", "bandar lampung"],
    "Cilegon": ["cilegon"],
    "Gresik": ["gresik"],
}

# ---------------------------------------------------------------------------
# Dangerous-goods training set: (text, label). label=1 -> dangerous / unsafe
# to consolidate, label=0 -> safe general cargo. Text mixes item names and
# short phrases (Bahasa Indonesia + English) so the TF-IDF vectorizer sees
# realistic tokens from free-form shipment requests, not just single words.
# ---------------------------------------------------------------------------
DANGEROUS_GOODS_TRAINING_DATA: list[tuple[str, int]] = [
    # --- Explosives ---
    ("bahan peledak", 1),
    ("dinamit", 1),
    ("kembang api", 1),
    ("petasan besar", 1),
    ("amunisi peluru", 1),
    ("mesiu", 1),
    ("tnt", 1),
    ("detonator", 1),
    ("bom asap", 1),
    # --- Gases ---
    ("tabung gas lpg", 1),
    ("elpiji", 1),
    ("gas oksigen bertekanan", 1),
    ("gas alam cair lng", 1),
    ("gas beracun", 1),
    ("tabung gas elpiji 12kg", 1),
    ("gas nitrogen cair", 1),
    ("aerosol bertekanan tinggi", 1),
    # --- Flammable liquids/solids ---
    ("bensin", 1),
    ("solar", 1),
    ("minyak tanah", 1),
    ("alkohol murni", 1),
    ("spiritus", 1),
    ("thinner", 1),
    ("cat minyak mudah terbakar", 1),
    ("pelarut kimia mudah terbakar", 1),
    ("avtur", 1),
    ("korek api batangan", 1),
    ("fosfor putih", 1),
    ("magnesium serbuk", 1),
    ("bahan bakar cair", 1),
    ("minyak bakar industri", 1),
    # --- Oxidizers ---
    ("kalium permanganat", 1),
    ("hidrogen peroksida pekat", 1),
    ("pupuk amonium nitrat", 1),
    ("kalsium hipoklorit", 1),
    # --- Toxic / infectious ---
    ("pestisida", 1),
    ("insektisida racun", 1),
    ("limbah medis infeksius", 1),
    ("bahan kimia beracun", 1),
    ("sianida", 1),
    ("racun tikus", 1),
    ("herbisida cair", 1),
    ("limbah b3", 1),
    # --- Radioactive ---
    ("bahan radioaktif", 1),
    ("uranium", 1),
    ("limbah nuklir", 1),
    ("sumber radiasi medis", 1),
    # --- Corrosives ---
    ("asam sulfat", 1),
    ("asam klorida", 1),
    ("soda api", 1),
    ("baterai asam basah", 1),
    ("air keras", 1),
    ("cairan pembersih korosif industri", 1),
    # --- Misc dangerous ---
    ("baterai lithium jumlah besar", 1),
    ("aki bekas mengandung asam", 1),
    ("merkuri", 1),
    ("asbes", 1),
    ("gas air mata", 1),
    ("senjata api", 1),
    ("bubuk kimia berbahaya tidak berlabel", 1),
    # --- Safe: textiles / apparel ---
    ("tekstil", 0),
    ("kain katun", 0),
    ("pakaian jadi", 0),
    ("baju kaos", 0),
    ("sepatu olahraga", 0),
    ("tas kulit sintetis", 0),
    ("kain batik", 0),
    ("celana jeans", 0),
    ("jaket musim dingin", 0),
    # --- Safe: electronics (consumer, not bulk battery) ---
    ("handphone baru", 0),
    ("laptop", 0),
    ("komponen elektronik kecil", 0),
    ("televisi led", 0),
    ("kabel listrik", 0),
    ("charger hp", 0),
    ("speaker bluetooth", 0),
    # --- Safe: furniture / household ---
    ("furniture kayu", 0),
    ("mebel jati", 0),
    ("kursi plastik", 0),
    ("lemari pakaian", 0),
    ("peralatan rumah tangga", 0),
    ("karpet", 0),
    ("gorden", 0),
    ("sprei dan bantal", 0),
    ("perabot dapur stainless", 0),
    # --- Safe: goods / consumables ---
    ("mainan anak", 0),
    ("buku pelajaran", 0),
    ("alat tulis kantor", 0),
    ("kertas hvs", 0),
    ("makanan kering kemasan", 0),
    ("snack ringan", 0),
    ("kopi bubuk", 0),
    ("teh celup", 0),
    ("beras", 0),
    ("gula pasir", 0),
    ("keramik lantai", 0),
    ("gelas kaca pecah belah", 0),
    ("sparepart motor non aki", 0),
    ("kosmetik non aerosol", 0),
    ("sayur segar", 0),
    ("buah-buahan", 0),
    ("ikan beku kemasan", 0),
    ("daging beku kemasan", 0),
    ("obat resep non narkotik", 0),
    ("produk kertas tisu", 0),
    ("boneka mainan", 0),
    ("alat olahraga raket", 0),
    ("sepeda lipat", 0),
    ("aksesoris fashion", 0),
    ("perhiasan imitasi", 0),
    ("produk kulit dompet", 0),
    ("botol plastik kosong", 0),
    ("kardus kosong", 0),
    ("plastik kemasan jadi", 0),
    ("payung lipat", 0),
    ("koper travel", 0),
    ("peralatan kantor printer", 0),
]
