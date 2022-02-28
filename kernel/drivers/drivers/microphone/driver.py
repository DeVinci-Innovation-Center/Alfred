from threading import Thread

from redis import Redis

from microphone import azure_speech, command_getter
from microphone import config as cfg
from microphone import data_producer, microphone_callback


def main():
    print(cfg.MICROPHONE_ID)
    redis_instance = Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    audio_stream = microphone_callback.SounddeviceCallback(cfg.MICROPHONE_ID)
    azure_sp = azure_speech.AzureSpeech(callback=audio_stream)

    getter = command_getter.CommandGetter(
        redis_instance, "device-command-microphone", audio_stream, azure_sp
    )
    producer = data_producer.DataProducer(
        redis_instance, "device-data-microphone", audio_stream, azure_sp
    )

    getter_thread = Thread(target=getter.loop)
    producer_thread = Thread(target=producer.loop)

    getter_thread.start()
    producer_thread.start()
