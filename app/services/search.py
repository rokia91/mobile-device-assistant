# Q5.2 - Q5.5 BM25 + Dense + RRF + hybrid_search()
from typing import List, Tuple

import numpy as np

from app.data.devices import DOCUMENTS
from app.utils.bm25_index import bm25, tokenize
from app.utils.embeddings import model, doc_embeddings

RRF_K = 60


def sparse_search(query: str) -> List[int]:
    scores = bm25.get_scores(tokenize(query))
    return np.argsort(-scores).tolist()


def dense_search(query: str) -> List[int]:
    query_emb = model.encode(query, normalize_embeddings=True)
    scores = doc_embeddings @ query_emb
    return np.argsort(-scores).tolist()


def rrf_fusion(sparse_ranking: List[int], dense_ranking: List[int], k: int = RRF_K) -> dict:
    fused = {}
    for ranking in (sparse_ranking, dense_ranking):
        for rank, doc_idx in enumerate(ranking, start=1):
            fused[doc_idx] = fused.get(doc_idx, 0.0) + 1.0 / (k + rank)
    return fused


def hybrid_search(query: str, k: int = 3) -> List[Tuple[str, float]]:
    fused = rrf_fusion(sparse_search(query), dense_search(query))
    top = sorted(fused.items(), key=lambda x: x[1], reverse=True)[:k]
    return [(DOCUMENTS[idx], float(score)) for idx, score in top]