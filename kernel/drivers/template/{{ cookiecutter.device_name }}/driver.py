from threading import Thread

from redis import Redis
from {{cookiecutter.device_name}} import command_getter
from {{cookiecutter.device_name}} import config as cfg
from {{cookiecutter.device_name}} import data_producer


def main():
    print(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)
    redis_instance = Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    getter = command_getter.CommandGetter(
        redis_instance,
        channel="device-command-{{ cookiecutter.device_name }}",
    )
    producer = data_producer.DataProducer(
        redis_instance,
        channel="device-data-{{ cookiecutter.device_name }}",
    )

    getter_thread = Thread(target=getter.loop)
    producer_thread = Thread(target=producer.loop)

    getter_thread.start()
    producer_thread.start()
