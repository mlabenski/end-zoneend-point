import os
from urllib.parse import urlparse
import redis

r = redis.from_urk(os.environ.get("REDIS_URL"))