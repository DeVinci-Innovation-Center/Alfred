import json
import time

from redis.client import PubSub

from src.utils.global_instances import rc


def send_command(command: str = "activate"):
    redis_command = {"function": "activate-bltouch", "data": repr(command)}
    # print(redis_command)

    res = rc.redis_instance.publish("device-command-bltouch", json.dumps(redis_command))
    # print(res)


def receive_data(pubusb: PubSub) -> str:
    return pubusb.get_message()["data"]


def main():
    # res= rc.redis_instance.pubsub()
    # res.subscribe("device-data-bltouch")
    time.sleep(1)
    send_command()
