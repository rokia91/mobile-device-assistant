# Q4.4 Injection check + Q6.2 / Q6.3 Endpoints and configuration
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.schema.device import (
    ExtractRequest, ExtractResponse,
    SearchRequest, SearchResponse, SearchResult,
)
from app.services.extraction import extract_device
from app.services.search import hybrid_search

load_dotenv()
app = FastAPI(title="Mobile Device Assistant API")

SUSPICIOUS_PHRASES = [
    "ignore previous",
    "ignore all previous",
    "system prompt",
    "you are now",
    "disregard the above",
    "forget your instructions",
]


def is_suspicious(text: str) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in SUSPICIOUS_PHRASES)


@app.post("/extract", response_model=ExtractResponse)
def extract(req: ExtractRequest):
    if is_suspicious(req.text):
        raise HTTPException(status_code=400, detail="Suspicious input detected.")
    try:
        return extract_device(req.text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    results = hybrid_search(req.q)
    return SearchResponse(
        results=[SearchResult(document=doc, score=score) for doc, score in results]
    )