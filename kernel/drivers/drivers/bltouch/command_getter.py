"""Get commands from Redis, treat them, and send them to the device."""

import json
import time
from typing import Any

from redis import Redis
from redis.client import PubSub

from bltouch import sensor


class CommandGetter:
    """Gets commands over Redis."""

    redis_instance: Redis
    pubsub: PubSub
    channel: str

    def __init__(self, redis_instance: Redis, channel: str, sensor: sensor.BLTouch):
        self.redis_instance = redis_instance
        self.pubsub = self.redis_instance.pubsub()
        self.channel = channel
        self.blt = sensor

        self.pubsub.subscribe(self.channel)

    def get_command(self) -> Any:
        """Get command from Redis."""

        message = self.pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            # do something with the message
            command = message["data"].decode("utf-8")
            return command

    def execute_command(self, command: Any):
        """Send command to device."""
        command_dict: dict = json.loads(command)
        if command_dict.get("function") == "activate-bltouch":
            print("send_command")
            self.blt.send_command()

    def loop(self):
        """Get and produce data indefinitely."""
        while True:
            command = self.get_command()
            if command:
                self.execute_command(command)
            time.sleep(0.001)  # be nice to the system :)
