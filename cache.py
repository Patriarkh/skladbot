import redis
import os
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=0
)

def cache_warehouse(warehouse_name, data):
    redis_client.set(warehouse_name, data)

def get_from_cache(warehouse_name):
    data = redis_client.get(warehouse_name)
    return data.decode('utf-8') if data else None
