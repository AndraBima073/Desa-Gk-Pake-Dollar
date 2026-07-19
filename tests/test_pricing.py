from app.ml.pricing import recommend_price


def test_price_is_always_at_least_one_rupiah():
    result = recommend_price(volume_m3=0.0, weight_tons=0.0)
    assert result.recommended_split_price_idr >= 1


def test_binding_ratio_picks_the_larger_constraint():
    # weight ratio (5/22 = 22.7%) > volume ratio (1/33 = 3%) -> weight binds.
    result = recommend_price(volume_m3=1.0, weight_tons=5.0)
    assert "berat" in result.negotiation_basis


def test_larger_shipment_costs_more():
    small = recommend_price(volume_m3=2.0, weight_tons=1.0)
    large = recommend_price(volume_m3=16.0, weight_tons=8.0)
    assert large.recommended_split_price_idr > small.recommended_split_price_idr
