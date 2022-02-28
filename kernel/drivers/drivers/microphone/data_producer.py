"""Gets data from a device, treats them, and sends them to Redis."""

import pickle
import threading
import time
from typing import Any

from redis import Redis

from microphone.azure_speech import AzureSpeech
from microphone.microphone_callback import SounddeviceCallback


class DataProducer:
    """Produces sensor data over Redis."""

    redis_instance: Redis
    channel: str

    def __init__(
        self,
        redis_instance: Redis,
        channel: str,
        audio_stream: SounddeviceCallback,
        azure_instance: AzureSpeech,
    ):
        self.redis_instance = redis_instance
        self.channel = channel
        self.audio_stream = audio_stream
        self.azure_instance = azure_instance

        self.last_update = time.time()

        self.recog_thread = threading.Thread(
            target=self.azure_instance.start_recog_continuous, daemon=True
        )
        self.recog_thread.start()

    def get_data(self):
        """Get data from device."""

        mic_data = self.audio_stream.read_frame(check_ready=True)
        speech_data = self.azure_instance.read_result(check_ready=True)

        return mic_data, speech_data

    def produce_data(self, data: Any):
        """Produce data to Redis."""

        mic_data, speech_data = data

        if mic_data is not None:
            self.redis_instance.publish(
                channel=f"{self.channel}-mic", message=pickle.dumps(mic_data)
            )

        if speech_data is not None:
            print(speech_data)
            self.redis_instance.publish(
                channel=f"{self.channel}-speech", message=speech_data
            )

    def loop(self):
        """Get and produce data indefinitely."""

        while True:
            data = self.get_data()
            self.produce_data(data)
            time.sleep(0.001)
