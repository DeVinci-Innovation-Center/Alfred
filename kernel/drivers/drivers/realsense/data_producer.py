"""Gets data from a device, treats them, and sends them to Redis."""

import logging
import pickle
import time
from typing import Any

import numpy as np
from redis import Redis

from realsense import config as cfg
from realsense.realsense_manager import RealsenseManager


class DataProducer:
    """Produces sensor data over Redis."""

    redis_instance: Redis
    channel: str

    def __init__(
        self, redis_instance: Redis, channel: str, rs_manager: RealsenseManager
    ):
        self.logger = logging.getLogger(f"drivers.{cfg.DRIVER_NAME}")

        self.redis_instance = redis_instance
        self.channel = channel

        self.last_update = time.time()

        self.rs_manager = rs_manager

    def get_data(self):
        """Get data from device."""

        try:
            frames = self.rs_manager.wait_for_frames(1000)
        except RuntimeError as e:
            if "Frame didn't arrive within" in e.args[0]:
                self.recover_disconnected()
                return None

            raise e

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
