"""Get commands from Redis, treat them, and send them to the device."""

import time
from typing import Any

from redis import Redis
from redis.client import PubSub


class CommandGetter:
    """Gets commands over Redis."""

    redis_instance: Redis
    pubsub: PubSub
    channel: str

    def __init__(self, redis_instance: Redis, channel: str, *args, **kwargs):
        self.redis_instance = redis_instance
        self.pubsub = self.redis_instance.pubsub()
        self.channel = channel

        self.pubsub.subscribe(self.channel)

    def get_command(self) -> Any:
        """Get command from Redis."""

        message = self.pubsub.get_message()
        if message:
            # do something with the message
            print(message)

        return message

    def execute_command(self, command: Any):
        """Send command to device."""

    def loop(self):
        """Get and produce data indefinitely."""

        while True:
            command = self.get_command()
            if command:
                self.execute_command(command)
            time.sleep(0.001)  # be nice to the system :)
