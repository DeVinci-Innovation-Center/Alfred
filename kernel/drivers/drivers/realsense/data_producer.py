# pylint: disable=no-member
"""Gets data from a device, treats them, and sends them to Redis."""

import time
from typing import Any
import pickle

from redis import Redis
import numpy as np
import pyrealsense2 as rs


class DataProducer:
    """Produces sensor data over Redis."""

    redis_instance: Redis
    channel: str

    def __init__(self, redis_instance: Redis, channel: str):
        self.redis_instance = redis_instance
        self.channel = channel

        self.last_update = time.time()

        self.pipeline = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)

    def get_data(self):
        """Get data from device."""

        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            return None

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        return pickle.dumps(color_image)

    def produce_data(self, data: Any):
        """Produce data to Redis."""

        self.redis_instance.publish(channel=self.channel, message=data)

    def loop(self):
        """Get and produce data indefinitely."""

        while True:
            data = self.get_data()
            if data is not None:
                self.produce_data(data)

        # pipe.stop()
