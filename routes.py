import hashlib
import time
from fastapi import APIRouter
from pydantic import BaseModel 
from app.cache import cache
from app.rag import generate_rag_response
from app.logger import logger

router = APIRouter()

class ChatInput(BaseModel):
    message: str

@router.post("/chat")
async def chat(payload: ChatInput):
    start_time = time.time()
    user_query = payload.message.strip()

    # Create a unique tracking fingerprint hash for this specific sentence string
    query_hash = f"msg:{hashlib.md5(user_query.lower().encode()).hexdigest()}"

    # 1. Attempt to resolve via Redis Cache first
    cached_reply = cache.get(query_hash)
    if cached_reply:
        latency = int((time.time() - start_time) * 1000)
        logger.info("Request resolved", extra={"extra_metric": {"latency_ms": latency, "cached": True}})
        return cached_reply

    # 2. Execute active inference pipeline if cache misses
    ai_response = await generate_rag_response(user_query)

    # 3. Store result in cache for future inquiries
    cache.set(query_hash, ai_response, ttl=600)

    latency = int((time.time() - start_time) * 1000)
    logger.info("Request resolved", extra={
        "extra_metric": {"latency_ms": latency, "cached": False, "tool_triggered": ai_response["tool_used"]}
    })

    return ai_response