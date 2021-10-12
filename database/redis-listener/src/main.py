import logging
import os
import time
from typing import Any, Dict, Union

import pymongo
import redis  # type: ignore

MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_PORT = os.getenv("MONGODB_PORT")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


def setup_logger(logger_name):
    """Init logger, set handler with format and level."""

    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s --> %(message)s"
    )
    ch.setFormatter(formatter)  # add formatter to ch
    log.addHandler(ch)  # add ch to logger


LOGGER_NAME = __name__
setup_logger(LOGGER_NAME)
logger = logging.getLogger(LOGGER_NAME)


class MongoDBClient:
    """Client class for the MongoDB interface."""

    host: str
    port: int
    username: Union[str, None]
    password: Union[str, None]
    database_name: str

    client: pymongo.MongoClient
    database: pymongo.database.Database
    collections: Dict[str, pymongo.collection.Collection]

    blacklisted_collection_names = ["*"]

    def __init__(
        self,
        host: str,
        port: str,
        username: Union[str, None],
        password: Union[str, None],
        database_name: str,
    ):
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.database_name = database_name

        self.collections = {}

        self._connect()

    def _get_conn_str(self):
        """Get a connection string for the current instance."""

        if self.username is None or self.password is None:
            credentials = ""
        else:
            credentials = f"{self.username}:{self.password}@"

        return f"mongodb://{credentials}{self.host}:{self.port}"

    def _connect(self):
        """Connect to MongoDB database."""

        logger.info("Connecting to MongoDB.")

        self.client = pymongo.MongoClient(self._get_conn_str())
        self.database = self.client[self.database_name]

        logger.info("Connected to MongoDB.")

    def insert(self, target_collection: str, data: Any):
        """Insert data into target collection."""

        if target_collection in self.blacklisted_collection_names:
            return

        if target_collection not in self.collections:
            self.collections[target_collection] = self.database[target_collection]

        x = self.collections[target_collection].insert_one(data)

        if not x:
            logger.error("Error inserting message.")
            return

        logger.info("Inserted message into mongodb.")


class RedisClient:
    """Client class for the Redis interface."""

    host: str
    port: int
    password: Union[str, None]
    redis_instance: redis.Redis
    p: Union[redis.client.PubSub, None]

    def __init__(self, host: str, port: str, password: str = None):
        self.host = host
        self.port = int(port)
        self.password = password

        self._connect()

    def _connect(self) -> redis.Redis:
        """Connect to Redis database"""

        logger.info("Connecting to Redis")

        self.redis_instance = redis.Redis(
            host=self.host, port=self.port, password=self.password
        )

        logger.info("Connected to Redis")

    def subscribe_all(self):
        """Subscribe to all channels and register message handler."""

        self.p = self.redis_instance.pubsub()
        self.p.psubscribe("*")

        logger.info("Subscribed redis instance to all channels.")

    def loop(self, mongodb_client: MongoDBClient):
        """Get messages as they are sent and handle them."""

        logger.info("Receiving messages.")

        if self.p is None:
            raise ValueError(
                "self.p is not configured. You must call self.subscribe_all() before self.loop()"
            )

        while True:
            message = self.p.get_message()
            if message:
                # pylint: disable = consider-using-f-string
                logger.info("Received message: \n%s", message)

                channel = message["channel"].decode("utf-8")

                data = message["data"]
                if isinstance(data, bytes):
                    data = data.decode("utf-8")

                mongodb_client.insert(channel, {"data": data})

            time.sleep(0.001)  # be nice to the system :)


def main():
    """Listens on all redis channels and forwards messages to mongodb."""

    mongodb_client = MongoDBClient(
        MONGODB_HOST, MONGODB_PORT, MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_DATABASE
    )

    redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
    redis_client.subscribe_all()
    redis_client.loop(mongodb_client)


if __name__ == "__main__":
    main()
