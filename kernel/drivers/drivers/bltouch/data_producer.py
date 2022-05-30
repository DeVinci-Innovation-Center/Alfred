"""Gets data from a device, treats them, and sends them to Redis."""

import time
import uuid
from typing import Any

from redis import Redis

from bltouch import sensor


class DataProducer:
    """Produces sensor data over Redis."""

    redis_instance: Redis
    channel: str

    def __init__(
        self, redis_instance: Redis, channel: str, sensor: sensor.BLTouch
    ) -> None:
        self.redis_instance = redis_instance
        self.channel = channel
        self.blt = sensor

        self.last_update = time.time()

    def get_data(self) -> str:
        """Get data from device."""

        data = self.blt.get_data()
        return data

    def produce_data(self, data: Any) -> None:
        """Produce data to Redis."""

        self.redis_instance.publish(channel=self.channel, message=data)

    def loop(self):
        """Get and produce data indefinitely."""

        while True:
            data = (
                self.get_data()
            )  # if nothing on serial is detected, after "timeout" seconds, it returns: ""
            if data != "":
                self.produce_data(data)  # send only if something is detected
            time.sleep(0.05)
