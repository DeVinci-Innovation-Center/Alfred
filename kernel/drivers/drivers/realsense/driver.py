from threading import Thread

from redis import Redis

from libalfred.utils import config_logger
from realsense import command_getter
from realsense import config as cfg
from realsense import data_producer
from realsense import realsense_manager as rsm


def main():
    config_logger(f"drivers.{cfg.DRIVER_NAME}")

    redis_instance = Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    rs_manager = rsm.RealsenseManager()

    getter = command_getter.CommandGetter(
        redis_instance, "device-command-realsense", rs_manager
    )
    producer = data_producer.DataProducer(
        redis_instance, "device-data-realsense", rs_manager
    )

    getter_thread = Thread(target=getter.loop)
    producer_thread = Thread(target=producer.loop)

    getter_thread.start()
    producer_thread.start()
