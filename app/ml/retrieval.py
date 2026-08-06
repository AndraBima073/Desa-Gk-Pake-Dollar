
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.ml.reference_data import DANGEROUS_GOODS_TRAINING_DATA

_DEFAULT_TOP_K = 5


@dataclass
class RetrievedExample:
    text: str
    is_dangerous: bool
    similarity: float


@lru_cache
def _build_index() -> tuple[TfidfVectorizer, object, list[str], list[int]]:
    texts = [text for text, _ in DANGEROUS_GOODS_TRAINING_DATA]
    labels = [label for _, label in DANGEROUS_GOODS_TRAINING_DATA]
    vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), lowercase=True)
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix, texts, labels


def retrieve_similar_examples(query: str, top_k: int = _DEFAULT_TOP_K) -> list[RetrievedExample]:
    vectorizer, matrix, texts, labels = _build_index()
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, matrix)[0]
    ranked_indices = similarities.argsort()[::-1][:top_k]
    return [
        RetrievedExample(text=texts[i], is_dangerous=bool(labels[i]), similarity=float(similarities[i]))
        for i in ranked_indices
        if similarities[i] > 0
    ]
