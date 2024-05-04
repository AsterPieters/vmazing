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

def redis_increment(key):
  """
  Get a redis key and increment it
  """

  # Connect to redis
  r = redis_conn()

  # Retrieve the key
  old_value = r.get(key)

  # Increment by one
  new_value = int(old_value) + 1
  r.set(key, new_value)

  # Check if the key exists and print the value
  if new_value is not None:
      return new_value
  else:
      return False