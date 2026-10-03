# Steps 7-9: compare BM25 vs Dense vs RRF
from app.data.devices import DOCUMENTS
from app.services.search import sparse_search, dense_search, hybrid_search

q = "best phone for low light photography"
print("BM25 :", [DOCUMENTS[i][:30] for i in sparse_search(q)[:3]])
print("Dense:", [DOCUMENTS[i][:30] for i in dense_search(q)[:3]])
print("RRF  :", hybrid_search(q))