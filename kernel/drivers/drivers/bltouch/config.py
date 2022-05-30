import os

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "")
try:
    REDIS_PORT = int(os.getenv("REDIS_PORT", ""))
except ValueError:
    REDIS_PORT = 6379
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# bltouch sensor
BLTOUCH_SERIAL_PORT = os.getenv("BLTOUCH_SERIAL_PORT", "/dev/ttyACM1")
BLTOUCH_BAUDRATE = int(os.getenv("BLTOUCH_BAUDRATE", 9600))
