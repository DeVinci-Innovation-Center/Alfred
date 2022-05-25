# pylint: disable=no-member
"""Gets data from a device, treats them, and sends them to Redis."""

import logging
import pickle
import time
from typing import Any

import numpy as np
import pyrealsense2 as rs
from redis import Redis

from realsense import config as cfg


class DataProducer:
    """Produces sensor data over Redis."""

    redis_instance: Redis
    channel: str

    def __init__(self, redis_instance: Redis, channel: str):
        self.logger = logging.getLogger(f"drivers.{cfg.DRIVER_NAME}")

        self.redis_instance = redis_instance
        self.channel = channel

        self.last_update = time.time()

        self.pipeline = rs.pipeline()
        self.config_flags = [[rs.stream.color, 640, 480, rs.format.bgr8, 30]]
        self.config = rs.config()
        self.configure_rs_config()

        # Try to connect and start streaming
        self.connect_loop()

    def configure_rs_config(self):
        """Enable streams as configured in config_flags."""

        for flag in self.config_flags:
            self.config.enable_stream(*flag)

    def connect_loop(self, t: float = 1.0):
        """Try to connect indefinitely, with t seconds between tries."""

        alert_cant_connect = True  # flag to enable logging of retry message
        while True:
            try:
                self.logger.info("Starting pipeline")
                self.pipeline.start(self.config)
                self.logger.info("Started realsense pipeline.")

                return

            except RuntimeError:
                if alert_cant_connect:
                    self.logger.error(
                        "Unable to start realsense pipeline. "
                        "Will try every %s second(s).",
                        t,
                        # exc_info=1,
                    )
                    alert_cant_connect = False  # only alert once

                time.sleep(t)

    def recover_disconnected(self):
        """Recover from the camera being disconnected."""

        self.logger.error("Camera disconnected. Recovering.")

        loop = True
        while loop:
            try:
                self.pipeline = rs.pipeline()
                self.config = rs.config()
                self.configure_rs_config()

                self.pipeline.start(self.config)
            except RuntimeError:
                pass
            finally:
                try:
                    a = self.pipeline.try_wait_for_frames(1000)
                    loop = not a[0]
                    self.logger.debug("%s | %s", a, loop)
                except RuntimeError:
                    pass

        self.logger.info("Recovered.")

    def get_data(self):
        """Get data from device."""

        try:
            frames = self.pipeline.wait_for_frames(1000)
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
