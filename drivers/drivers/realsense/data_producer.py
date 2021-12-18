"""Gets data from a device, treats them, and sends them to Redis."""

import time
import uuid
from typing import Any

from redis import Redis


class DataProducer:
    """Produces sensor data over Redis."""

    redis_instance: Redis
    channel: str

    def __init__(self, redis_instance: Redis, channel: str):
        self.redis_instance = redis_instance
        self.channel = channel

        self.last_update = time.time()

    def get_data(self):
        """Get data from device."""

        data = str(uuid.uuid4())

        return data

    def produce_data(self, data: Any):
        """Produce data to Redis."""

        self.redis_instance.publish(channel=self.channel, message=data)

    def loop(self):
        """Get and produce data indefinitely."""

        while True:
            data = self.get_data()
            self.produce_data(data)
            time.sleep(1)
