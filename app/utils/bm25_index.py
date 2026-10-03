# Q5.2 Sparse retrieval index (built once, reused)
from rank_bm25 import BM25Okapi

from app.data.devices import DOCUMENTS


def tokenize(text: str):
    return text.lower().split()


bm25 = BM25Okapi([tokenize(doc) for doc in DOCUMENTS])