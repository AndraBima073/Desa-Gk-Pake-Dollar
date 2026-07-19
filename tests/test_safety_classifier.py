import pytest

from app.ml.safety_classifier import predict

DANGEROUS_SAMPLES = ["bensin", "gas lpg", "asam sulfat", "bahan peledak", "pestisida"]
SAFE_SAMPLES = ["tekstil", "furniture kayu", "sepatu olahraga", "buku pelajaran", "mainan anak"]


@pytest.mark.parametrize("text", DANGEROUS_SAMPLES)
def test_classifies_known_dangerous_goods(text):
    result = predict(text)
    assert result.is_dangerous is True


@pytest.mark.parametrize("text", SAFE_SAMPLES)
def test_classifies_known_safe_goods(text):
    result = predict(text)
    assert result.is_dangerous is False


def test_confidence_is_a_probability():
    result = predict("bensin")
    assert 0.0 <= result.confidence <= 1.0
