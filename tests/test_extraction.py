from datetime import date

from app.ml.extraction import extract

REFERENCE_DATE = date(2026, 7, 13)


def test_extracts_full_shipment_details():
    text = (
        "Halo, saya mau kirim tekstil 8 m3 berat 5 ton dari Jakarta ke Surabaya "
        "tanggal 20 Juli 2026."
    )
    result = extract(text, REFERENCE_DATE)
    assert result.origin == "Jakarta"
    assert result.destination == "Surabaya"
    assert result.date_iso == "2026-07-20"
    assert result.item_name == "tekstil"
    assert result.volume_m3 == 8.0
    assert result.weight_tons == 5.0
    assert result.has_any_signal is True


def test_resolves_relative_dates():
    result = extract("kirim barang dari jakarta ke surabaya besok", REFERENCE_DATE)
    assert result.date_iso == "2026-07-14"


def test_converts_liter_to_m3_and_kg_to_tons():
    result = extract("kirim 500 liter dan 2000 kg barang dari jakarta ke surabaya", REFERENCE_DATE)
    assert result.volume_m3 == 0.5
    assert result.weight_tons == 2.0


def test_preserves_negative_numbers_for_safety_guardian():
    # A negative-value injection attempt must survive extraction as a
    # negative number, not get silently absorbed as positive — the numeric
    # safety-guardian check downstream depends on seeing the true sign.
    result = extract("kirim -5 ton barang dari jakarta ke surabaya besok", REFERENCE_DATE)
    assert result.weight_tons == -5.0


def test_nonsense_text_has_no_signal():
    result = extract("halo apa kabar semoga sehat selalu", REFERENCE_DATE)
    assert result.has_any_signal is False
    assert result.origin is None
    assert result.destination is None


def test_extracts_item_name_when_quantity_precedes_it():
    result = extract("kirim 3 ton gas lpg dari semarang menuju balikpapan", REFERENCE_DATE)
    assert result.item_name == "gas lpg"
    assert result.origin == "Semarang"
    assert result.destination == "Balikpapan"
