from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_match_found_for_known_route():
    payload = {
        "raw_text": (
            "Halo, saya mau kirim tekstil 8 m3 berat 5 ton dari Jakarta ke Surabaya "
            "tanggal 20 Juli 2026."
        )
    }
    r = client.post("/api/v1/consolidate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "MATCH_FOUND"
    assert body["match"] is not None
    assert body["extracted_data"]["origin"] == "Jakarta"
    assert body["extracted_data"]["destination"] == "Surabaya"
    # Anonymity contract: no company/slot-owner field ever leaks to the client.
    assert "company_name" not in body["match"]
    assert "slot_id" not in body["match"]

    # Feature: explicit cost-savings comparison vs a dedicated container.
    pricing = body["pricing"]
    assert pricing["dedicated_container_price_idr"] > pricing["recommended_split_price_idr"]
    assert pricing["savings_idr"] == (
        pricing["dedicated_container_price_idr"] - pricing["recommended_split_price_idr"]
    )
    assert 0 <= pricing["savings_percent"] <= 100

    # Feature: capacity urgency label derived from remaining space.
    assert body["match"]["capacity_urgency"] in ("low", "medium", "high")

    # Feature: alternative-candidate transparency — Jakarta->Surabaya has 3
    # compatible mock slots, so the message should surface the other two.
    assert "alternatif" in body["notification_message"]

    # Feature: structured alternatives list (best match + other feasible
    # slots), each carrying its own utility data, for the frontend to render.
    assert len(body["alternatives"]) == 2
    for alt in body["alternatives"]:
        assert "company_name" not in alt
        assert "slot_id" not in alt
        assert alt["capacity_urgency"] in ("low", "medium", "high")
    utilizations = [a["space_utilization_percent"] for a in body["alternatives"]]
    assert utilizations == sorted(utilizations, reverse=True)
    # The winning match must not also appear in the alternatives list.
    assert body["match"]["anonymous_slot_reference"] not in {
        a["anonymous_slot_reference"] for a in body["alternatives"]
    }


def test_no_alternatives_key_when_no_match():
    payload = {
        "raw_text": "kirim tekstil 8 m3 berat 5 ton dari Jayapura ke Ambon tanggal 20 Juli 2026"
    }
    r = client.post("/api/v1/consolidate", json=payload)
    assert r.status_code == 200
    assert r.json()["alternatives"] == []


def test_no_match_for_unknown_route():
    payload = {
        "raw_text": "kirim tekstil 8 m3 berat 5 ton dari Jayapura ke Ambon tanggal 20 Juli 2026"
    }
    r = client.post("/api/v1/consolidate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "NO_MATCH_DEDICATED_CONTAINER"
    assert body["match"] is None


def test_rejects_negative_weight():
    payload = {"raw_text": "kirim -5 ton barang dari jakarta ke surabaya besok"}
    r = client.post("/api/v1/consolidate", json=payload)
    assert r.status_code == 400


def test_rejects_dangerous_goods():
    payload = {"raw_text": "kirim bensin 5 ton dari jakarta ke surabaya besok"}
    r = client.post("/api/v1/consolidate", json=payload)
    assert r.status_code == 400


def test_rejects_nonsense_input():
    payload = {"raw_text": "halo apa kabar semoga sehat selalu ya"}
    r = client.post("/api/v1/consolidate", json=payload)
    assert r.status_code == 422


def test_rejects_too_short_raw_text():
    r = client.post("/api/v1/consolidate", json={"raw_text": "hi"})
    assert r.status_code == 422


def test_list_available_routes():
    r = client.get("/api/v1/routes")
    assert r.status_code == 200
    routes = r.json()
    assert len(routes) == 6  # matches len(MOCK_CONTAINER_DB)
    first = routes[0]
    assert {"origin", "destination", "date", "available_volume_m3",
            "available_weight_tons", "space_utilization_percent"} <= first.keys()
    # Anonymity contract: no company/slot-owner field ever leaks to the client.
    assert "company_name" not in first
    assert "slot_id" not in first
