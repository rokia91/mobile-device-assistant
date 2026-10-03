# Q5.3 Dense retrieval model + document embeddings (computed once)
from sentence_transformers import SentenceTransformer

from app.data.devices import DOCUMENTS

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
doc_embeddings = model.encode(DOCUMENTS, normalize_embeddings=True)