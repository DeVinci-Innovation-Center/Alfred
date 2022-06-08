"""Class for managing the Realsense camera."""

import logging
import time
from typing import Any, Tuple

import pyrealsense2 as rs

from realsense import config as cfg


class RealsenseManager:
    """Manages the Realsense camera."""

    def __init__(self):
        self.logger = logging.getLogger(f"drivers.{cfg.DRIVER_NAME}")

        self.pipeline = rs.pipeline()
        self.config_flags = [
            [rs.stream.color, 640, 480, rs.format.bgr8, 30],
            [rs.stream.depth, 640, 480, rs.format.z16, 30],
        ]
        self.config = rs.config()
        self.configure_rs_config()

        # Try to connect and start streaming
        self.connect_loop()

    def configure_rs_config(self):
        """Enable streams as configured in config_flags."""

        for flag in self.config_flags:
            self.config.enable_stream(*flag)

    def restart_camera(self):
        """Restart the camera."""

        self.logger.info("Restarting camera.")
        self.pipeline.stop()
        self.configure_rs_config()
        self.connect_loop()

    def connect_loop(self, t: float = 1.0):
        """Try to connect indefinitely, with t seconds between tries."""

        self.logger.info("Starting pipeline")
        alert_cant_connect = True  # flag to enable logging of retry message

        while True:
            try:
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
                break

            except RuntimeError:
                pass

        self.logger.info("Recovered.")

    def try_wait_for_frames(self, timeout_ms: int = 5000) -> Tuple[bool, Any]:
        """Try to get frames from the pipeline. First element is True if a
        frame was received, second is the frame."""

        return self.pipeline.try_wait_for_frames(timeout_ms)

    def wait_for_frames(self, timeout_ms: int = 5000) -> Any:
        """Try to get frames from the pipeline, throws error if times out."""

        return self.pipeline.wait_for_frames(timeout_ms)
