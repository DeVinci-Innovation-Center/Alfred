"""Gets data from a device, treats them, and sends them to Redis."""

import pickle
import time
from typing import Any

from redis import Redis

from microphone.mic_driver import MicDriver


class DataProducer:
    """Produces sensor data over Redis."""

    redis_instance: Redis
    channel: str

    def __init__(
        self, redis_instance: Redis, channel: str, mic_driver: MicDriver
    ):
        self.redis_instance = redis_instance
        self.channel = channel
        self.mic_driver = mic_driver

        self.last_update = time.time()

        self.mic_driver.capture_thread.start()
        self.mic_driver.recog_thread.start()

    def get_data(self):
        """Get data from device."""

        mic_data = self.mic_driver.read_frame(check_ready=True)
        speech_data = self.mic_driver.read_result(check_ready=True)

        return mic_data, speech_data

    def produce_data(self, data: Any):
        """Produce data to Redis."""

        mic_data, speech_data = data

        if mic_data is not None:
            self.redis_instance.publish(
                channel=f"{self.channel}-mic", message=pickle.dumps(mic_data)
            )

        if speech_data is not None:
            self.redis_instance.publish(
                channel=f"{self.channel}-speech", message=str(speech_data)
            )

    def loop(self):
        """Get and produce data indefinitely."""

        while True:
            data = self.get_data()
            self.produce_data(data)
            time.sleep(0.001)
