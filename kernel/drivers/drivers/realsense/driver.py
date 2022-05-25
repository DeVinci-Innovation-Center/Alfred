from threading import Thread

from libalfred.utils import config_logger
from redis import Redis

from realsense import command_getter
from realsense import config as cfg
from realsense import data_producer


def main():
    config_logger(f"drivers.{cfg.DRIVER_NAME}")

    redis_instance = Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    getter = command_getter.CommandGetter(
        redis_instance, channel="device-command-realsense",
    )
    producer = data_producer.DataProducer(
        redis_instance, channel="device-data-realsense",
    )

    getter_thread = Thread(target=getter.loop)
    producer_thread = Thread(target=producer.loop)

    getter_thread.start()
    producer_thread.start()
