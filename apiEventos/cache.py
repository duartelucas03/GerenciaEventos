import redis
import json

cache = redis.Redis(host="localhost", port=6380, decode_responses=True)


def get_cache(key):
    value = cache.get(key)
    if value:
        return json.loads(value)
    return None

def set_cache(key, data, ttl=60):
    cache.setex(key, ttl, json.dumps(data))

# comando para iniciar o redis
# .\redis-server.exe --port 6380