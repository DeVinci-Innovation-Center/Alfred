from typing import List, Union

import redis  # type: ignore


class RedisClient:
    """Client class for the controller Redis interface."""

    host: str
    port: int
    password: Union[str, None]
    redis_instance: redis.Redis
    subscribers: List[redis.client.PubSub]

    def __init__(self, host: str = "0.0.0.0", port: int = 6379, password: str = None):
        self.host = host
        self.port = port
        self.password = password

        self.redis_instance = self._connect_redis()

        self.subscribers = []

    def _connect_redis(self) -> redis.Redis:
        """Connect to Redis database"""

        r = redis.Redis(host=self.host, port=self.port, password=self.password)
        return r

    def add_subscriber(self, channels_and_handlers: dict) -> redis.client.PubSub:
        """Create a new subscriber and add it to subscribers list.
        Keyword args must be {channel: message_handler, ...}."""

        subscriber = self.redis_instance.pubsub()
        subscriber.subscribe(**channels_and_handlers)

        self.subscribers.append(subscriber)

        return subscriber

    @classmethod
    def print_message(cls, message: dict) -> dict:
        """Simple message handler: prints channel and message content."""

        print(
            f"from {message['channel'].decode('utf-8')}: {message['data'].decode('utf-8')}"
        )

        if message["data"] == b"stop":
            raise Exception("Stop thread.")

        return message
