"""Gets data from a device, treats them, and sends them to Redis."""

import logging
import pickle
import time
from typing import Any

import cv2
from redis import Redis

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__file__)


class DataProducer:
    """Produces sensor data over Redis."""

    redis_instance: Redis
    channel: str

    cap: cv2.VideoCapture

    def __init__(self, redis_instance: Redis, channel: str, video_path: str):
        self.redis_instance = redis_instance
        self.channel = channel

        self.cap = cv2.VideoCapture(video_path)

        self.last_update = time.time()

        logger.info("initialized data producer")

    def get_data(self):
        """Get data from device."""

        _, frame = self.cap.read()
        if frame is not None:
            frame_serialized = pickle.dumps(frame)
            return frame_serialized

        return None

    def produce_data(self, data: Any):
        """Produce data to Redis."""

        self.redis_instance.publish(channel=self.channel, message=data)

    def loop(self):
        """Get and produce data indefinitely."""

        while True:
            data = self.get_data()
            if data is not None:
                self.produce_data(data)
