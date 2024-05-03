# _redis.py
# Redis tools

# Imports
import redis

def redis_conn():
  """
  Connect to redis
  """

  redis_host = 'localhost'
  redis_port = 6379
  redis_password = None
  redis_db = 0

  r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)

  return r