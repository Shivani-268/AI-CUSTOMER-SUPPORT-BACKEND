import redis
import json
from app.config import settings

class CacheManager:
    def __init__(self):
        # decode_responses=True converts byte responses from Redis into standard strings
        self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    def get(self, key: str):
        try:
            data = self.client.get(key)
            return json.loads(data) if data else None
        except redis.RedisError:
            return None # If Redis drops out, fail safely without crashing the backend

    def set(self, key: str, value: dict, ttl: int = 600):
        try:
            # Save data with a Time-To-Live (TTL) of 10 minutes (600 seconds)
            self.client.setex(key, ttl, json.dumps(value))
        except redis.RedisError:
            pass

cache = CacheManager()