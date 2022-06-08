"""Gets data from a device, treats them, and sends them to Redis."""

import logging
import pickle
import time
from typing import Optional, Tuple

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
        self.channel_color = channel
        self.channel_depth = f"{self.channel_color}-depth"

        self.last_update = time.time()

        self.rs_manager = rs_manager

    def get_data(self) -> Optional[Tuple[bytes, bytes]]:
        """Get data from device."""

        try:
            frames = self.rs_manager.wait_for_frames(1000)
        except RuntimeError as e:
            if "Frame didn't arrive within" in e.args[0]:
                self.rs_manager.recover_disconnected()
                return None

            raise e

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            return None

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        return pickle.dumps(color_image), pickle.dumps(depth_image)

    def produce_data(self, data: bytes, *, frame_type: str):
        """Produce data to Redis."""

        if frame_type == "color":
            self.redis_instance.publish(channel=self.channel_color, message=data)
        elif frame_type == "depth":
            self.redis_instance.publish(channel=self.channel_depth, message=data)

    def loop(self):
        """Get and produce data indefinitely."""

        while True:
            data = self.get_data()
            if data is not None:
                color, depth = data

                self.produce_data(color, frame_type="color")
                self.produce_data(depth, frame_type="depth")
