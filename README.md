# Mobile Device Assistant API

FastAPI service with two features:
- POST /extract: structured device spec extraction using an LLM (Pydantic validation, 2 retries, prompt injection defense).
- POST /search: hybrid search using BM25 + dense embeddings + Reciprocal Rank Fusion (RRF).

## Setup
1. pip install -r requirements.txt
2. Copy .env.example to .env and add your API key.
3. uvicorn app.main:app --reload
4. Open http://127.0.0.1:8000/docs

## Note
Groq (OpenAI-compatible API) was used for the LLM with the model openai/gpt-oss-20b.
Set OPENAI_BASE_URL in .env to switch to OpenAI.