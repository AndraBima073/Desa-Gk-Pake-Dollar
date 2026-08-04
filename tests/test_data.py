from __future__ import annotations

# 1. REFERENCE DATA KAMU
CITY_ALIASES: dict[str, list[str]] = {
    "Jakarta": [
        "jakarta",
        "jkt",
        "dki jakarta",
        "jakarta pusat",
        "jakarta utara",
        "jakarta selatan",
        "jakarta barat",
        "jakarta timur",
        "jakpus",
        "jaksel",
        "jaktim",
        "jakbar",
        "jakut",
    ],
    "Surabaya": ["surabaya", "sby", "suroboyo"],
    "Yogyakarta": ["yogyakarta", "jogja", "yogya", "diy", "ykg"],
    "Denpasar": ["denpasar", "bali", "dps"],
    # ... masukan sisa data kamu di sini
}


# 2. FUNGSI PENJALAN / NORMALISASI
def normalize_city(user_input: str) -> str | None:
    cleaned_input = user_input.strip().lower()
    for official_name, aliases in CITY_ALIASES.items():
        if cleaned_input in aliases or cleaned_input == official_name.lower():
            return official_name
    return None


# 3. SCRIPT VALIDASI AUTO-CHECK (CEK ERROR)
def run_diagnostics():
    print("🔍 Menjalankan Pemeriksaan Kode & Reference Data...\n")
    errors_found = 0
    warnings_found = 0

    seen_aliases: dict[str, str] = {}

    # CEK 1: Mencegah Alias Ganda (Duplikat)
    for official_name, aliases in CITY_ALIASES.items():
        for alias in aliases:
            clean_alias = alias.strip().lower()
            if clean_alias in seen_aliases:
                print(
                    f"❌ ERROR [Duplikat Alias]: '{clean_alias}' dipakai di '{official_name}' DAN '{seen_aliases[clean_alias]}'"
                )
                errors_found += 1
            else:
                seen_aliases[clean_alias] = official_name

            # CEK 2: Memastikan alias tidak kosong
            if not clean_alias:
                print(
                    f"⚠️ WARNING [Alias Kosong]: Ada alias kosong di kota '{official_name}'"
                )
                warnings_found += 1

    # CEK 3: Tes Fungsi Normalisasi dengan Sampel Nyata
    test_cases = {
        "jakbar": "Jakarta",
        "SBY": "Surabaya",
        "jogja": "Yogyakarta",
        "dps": "Denpasar",
        "KOTA_ASAL_GHOIB": None,  # Harus bernilai None jika tidak ada di data
    }

    print("\n🧪 Menjalankan Tes Simulasi Input User:")
    for test_input, expected in test_cases.items():
        result = normalize_city(test_input)
        if result == expected:
            print(f"  ✅ Input: '{test_input}' ➔ Result: '{result}' (PASS)")
        else:
            print(
                f"  ❌ Input: '{test_input}' ➔ Result: '{result}' | Expected: '{expected}' (FAILED)"
            )
            errors_found += 1

    # HASIL AKHIR
    print("\n--------------------------------------------------")
    if errors_found == 0:
        print("🎉 SUCCESS: KODE & REFERENCE DATA BEBAS DARI ERROR!")
    else:
        print(f"🚨 FAILED: Ditemukan {errors_found} Error. Harap perbaiki data di atas.")


# --- JALANKAN PEMERIKSAAN ---
if __name__ == "__main__":
    run_diagnostics()