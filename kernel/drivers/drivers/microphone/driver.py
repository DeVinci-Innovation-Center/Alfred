from threading import Thread

from redis import Redis

from mps import command_getter
from mps import config as cfg
from mps import data_producer
from mps import mic_driver as microphone


def main():
    redis_instance = Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)
    mic_driver = microphone.MicDriver()

    getter = command_getter.CommandGetter(
        redis_instance, "device-command-microphone", mic_driver
    )
    producer = data_producer.DataProducer(
        redis_instance, "device-data-microphone", mic_driver
    )

    getter_thread = Thread(target=getter.loop)
    producer_thread = Thread(target=producer.loop)

    getter_thread.start()
    producer_thread.start()
