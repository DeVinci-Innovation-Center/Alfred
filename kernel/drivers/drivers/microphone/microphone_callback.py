import traceback
from typing import Optional, Union

import azure.cognitiveservices.speech as speechsdk
import numpy as np
import sounddevice as sd


class SounddeviceCallback(speechsdk.audio.PullAudioInputStreamCallback):
    """Callback for using Sounddevice audio capture with Azure Speech.
    """

    stream: sd.InputStream
    frame: np.ndarray
    frame_ready: bool

    def __init__(self, device: Union[str, int] = None):
        super().__init__()

        self.stream = sd.InputStream(
            device=device,
            dtype="int16",
            channels=1,
            samplerate=16_000,
            blocksize=1,
        )

        self.frame = None
        self.frame_ready = False

        self.stream.start()

    def save_frame(self, frame: np.ndarray):
        self.frame = frame.copy()
        self.frame_ready = True

    def read_frame(self, check_ready=False) -> Optional[np.ndarray]:
        """Returns last audio frame. If check_ready is True, returns None if
        the last frame was already read."""

        if check_ready and not self.frame_ready:
            return None

        self.frame_ready = False
        return self.frame

    def start(self):
        self.stream.start()

    def read(self, buffer: memoryview) -> int:
        try:
            size = buffer.nbytes

            frame: np.ndarray = self.stream.read(
                size // self.stream.samplesize
            )[0]
            frame = frame.flatten()
            self.save_frame(frame)

            new_buffer = frame.data.cast("B")
            buffer[: len(new_buffer)] = new_buffer

            return len(new_buffer)

        except Exception:
            traceback.print_exc()
            raise

    def close(self) -> None:
        print("closing file")
        try:
            self.stream.close()
        except Exception:
            traceback.print_exc()
            raise
