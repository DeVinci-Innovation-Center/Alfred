import os

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "")
try:
    REDIS_PORT = int(os.getenv("REDIS_PORT", ""))
except ValueError:
    REDIS_PORT = 6379
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


# MongoDB
MONGODB_HOST = os.getenv("MONGODB_HOST")
try:
    MONGODB_PORT = int(os.getenv("MONGODB_PORT", "27017"))
except ValueError:
    MONGODB_PORT = 27017
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

if MONGODB_USERNAME is None or MONGODB_PASSWORD is None:
    credentials = ""
else:
    credentials = f"{MONGODB_USERNAME}:{MONGODB_PASSWORD}@"

MONGO_CONN_STRING = f"mongodb://{credentials}{MONGODB_HOST}:{MONGODB_PORT}"
