from redis import Redis

from threading import Thread

from {{ cookiecutter.device_name }} import config as cfg
from {{ cookiecutter.device_name }} import command_getter, data_producer


def main():
    print(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)
    redis_instance = Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    getter = command_getter.CommandGetter(
        redis_instance,
        channel="device-command-example",
    )
    producer = data_producer.DataProducer(
        redis_instance,
        channel="device-data-example",
    )

    getter_thread = Thread(target=getter.loop)
    producer_thread = Thread(target=producer.loop)

    getter_thread.start()
    producer_thread.start()
