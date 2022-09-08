import os

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "")
try:
    REDIS_PORT = int(os.getenv("REDIS_PORT", ""))
except ValueError:
    REDIS_PORT = 6379
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

#FSR sensor
FSR_SERIAL_PORT=os.getenv("FSR_SERIAL_PORT","/dev/ttyACM1")
FSR_BAUDRATE=int(os.getenv("FSR_BAUDRATE",9600))
