"""Get commands from Redis, treat them, and send them to the device."""

import json
import time
from typing import Optional

from redis import Redis
from redis.client import PubSub

from realsense.realsense_manager import RealsenseManager


class CommandGetter:
    """Gets commands over Redis."""

    redis_instance: Redis
    pubsub: PubSub
    channel: str

    def __init__(
        self, redis_instance: Redis, channel: str, rs_manager: RealsenseManager
    ):
        self.redis_instance = redis_instance
        self.channel = channel
        self.rs_manager = rs_manager

        self.pubsub = self.redis_instance.pubsub()
        self.pubsub.subscribe(self.channel)

    def get_command(self) -> Optional[dict]:
        """Get command from Redis."""

        message = self.pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            # parse message
            message_bytes: bytes = message.get("data")  # type: ignore
            message_str = message_bytes.decode("utf-8")
            message_dict: dict = json.loads(message_str)
            return message_dict

        return None

    def execute_command(self, command: dict):
        """Send command to device."""

    def loop(self):
        """Get and produce data indefinitely."""

        while True:
            command = self.get_command()
            if command is not None:
                self.execute_command(command)
            time.sleep(0.001)  # be nice to the system :)
