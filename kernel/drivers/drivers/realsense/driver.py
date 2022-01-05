from redis import Redis

from threading import Thread

from realsense import config as cfg
from realsense import command_getter, data_producer


def main():
    print(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)
    redis_instance = Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    getter = command_getter.CommandGetter(
        redis_instance,
        channel="device-command-realsense",
    )
    producer = data_producer.DataProducer(
        redis_instance,
        channel="device-data-realsense",
    )

    getter_thread = Thread(target=getter.loop)
    producer_thread = Thread(target=producer.loop)

    getter_thread.start()
    producer_thread.start()
