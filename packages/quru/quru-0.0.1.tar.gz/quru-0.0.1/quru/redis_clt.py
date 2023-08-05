import redis
from .env import REDIS_HOST, REDIS_PORT

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
redis_client = redis.Redis(connection_pool=pool)