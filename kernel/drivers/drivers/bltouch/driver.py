from threading import Thread

from redis import Redis

from bltouch import command_getter
from bltouch import config as cfg
from bltouch import data_producer, sensor


def main():
    print(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)
    redis_instance = Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    blt = sensor.BLTouch(port=cfg.BLTOUCH_SERIAL_PORT, baudrate=cfg.BLTOUCH_BAUDRATE)

    getter = command_getter.CommandGetter(
        redis_instance, channel="device-command-bltouch", sensor=blt
    )
    producer = data_producer.DataProducer(
        redis_instance, channel="device-data-bltouch", sensor=blt
    )

    getter_thread = Thread(target=getter.loop)
    producer_thread = Thread(target=producer.loop)

    getter_thread.start()
    producer_thread.start()
