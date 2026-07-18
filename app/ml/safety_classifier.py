
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from app.ml.reference_data import DANGEROUS_GOODS_TRAINING_DATA


@dataclass
class SafetyPrediction:
    is_dangerous: bool
    confidence: float  


def _build_pipeline() -> Pipeline:
    texts = [text for text, _ in DANGEROUS_GOODS_TRAINING_DATA]
    labels = [label for _, label in DANGEROUS_GOODS_TRAINING_DATA]

    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="word",
                    ngram_range=(1, 2),
                    min_df=1,
                    lowercase=True,
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    pipeline.fit(texts, labels)
    return pipeline


@lru_cache
def load_classifier() -> Pipeline:
    """Process-wide singleton: trained once, reused for every request."""
    return _build_pipeline()


def predict(text: str) -> SafetyPrediction:
    """Classifies `text` (item name, or the full raw shipment request) as
    dangerous goods (1) or safe general cargo (0)."""
    pipeline = load_classifier()
    proba = pipeline.predict_proba([text])[0]
    class_index = int(proba.argmax())
    is_dangerous = bool(pipeline.classes_[class_index] == 1)
    confidence = float(proba[class_index])
    return SafetyPrediction(is_dangerous=is_dangerous, confidence=confidence)
