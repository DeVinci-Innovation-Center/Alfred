from redis import Redis

from threading import Thread

from gripper_sensor import config as cfg
from gripper_sensor import command_getter, data_producer

from gripper_sensor import sensor


def main():
    print(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)
    redis_instance = Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    fsr=sensor.FSR(port=cfg.FSR_SERIAL_PORT,baudrate=cfg.FSR_BAUDRATE)

    getter = command_getter.CommandGetter(
        redis_instance,
        channel="device-command-gripper",
        sensor=fsr
    )
    producer = data_producer.DataProducer(
        redis_instance,
        channel="device-data-gripper",
        sensor=fsr
    )

    getter_thread = Thread(target=getter.loop)
    producer_thread = Thread(target=producer.loop)

    getter_thread.start()
    producer_thread.start()
