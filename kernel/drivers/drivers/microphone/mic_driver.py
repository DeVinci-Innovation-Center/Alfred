import threading
import time
from typing import Optional

import azure.cognitiveservices.speech as speechsdk
import numpy as np
import sounddevice as sd

from microphone import azure_speech
from microphone import config as cfg

_lock = threading.Lock()


class MicDriver:
    mic_stream: sd.InputStream
    azure_stream: speechsdk.audio.PushAudioInputStream
    speech_recognizer: speechsdk.SpeechRecognizer

    def __init__(self):
        self.mic_stream = sd.InputStream(
            device=cfg.MICROPHONE_ID,
            dtype="int16",
            channels=1,
            samplerate=16_000,
            blocksize=1,
        )

        stream_format = speechsdk.audio.AudioStreamFormat()
        self.azure_stream = speechsdk.audio.PushAudioInputStream(stream_format)

        speech_config = speechsdk.SpeechConfig(
            subscription=cfg.AZURE_KEY, region=cfg.AZURE_REGION
        )

        audio_config = speechsdk.audio.AudioConfig(stream=self.azure_stream)

        auto_lang = azure_speech.OwnAutoDetectSourceLanguageConfig(
            languages=cfg.AZURE_LANG
        )

        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config,
            audio_config,
            auto_detect_source_language_config=auto_lang,
        )
        self.done = False

        self.speech_recognizer.recognized.connect(self.recognized_callback)
        self.speech_recognizer.session_started.connect(
            lambda evt: print("SESSION STARTED: {}".format(evt))
        )
        self.speech_recognizer.session_stopped.connect(
            lambda evt: print("SESSION STOPPED {}".format(evt))
        )
        self.speech_recognizer.canceled.connect(
            lambda evt: print("CANCELED {}".format(evt))
        )

        self.speech_recognizer.session_stopped.connect(self.stop_callback)
        self.speech_recognizer.canceled.connect(self.stop_callback)

        self.result_ready = False
        self.result = ""

        self.frame_ready = False
        self.frame = np.zeros((1,))

        self.recog_thread = threading.Thread(target=self.start_recog_continuous)
        self.capture_thread = threading.Thread(target=self.capture_mic_continuous)

    def save_frame(self, frame: np.ndarray):
        with _lock:
            self.frame = frame.copy()
            self.frame_ready = True

    def read_frame(self, check_ready=False) -> Optional[np.ndarray]:
        """Returns last audio frame. If check_ready is True, returns None if
        the last frame was already read."""
        with _lock:
            if check_ready and not self.frame_ready:
                return None

            self.frame_ready = False
            return self.frame

    def save_result(self, result: str):
        with _lock:
            self.result = result
            self.result_ready = True

    def read_result(self, check_ready=False) -> Optional[str]:
        """Returns last recognition result. If check_ready is True, returns None if
        the last results was already read."""
        with _lock:
            if check_ready and not self.result_ready:
                return None

            self.result_ready = False
            return self.result

    def capture_mic_continuous(self):
        n_bytes = 3200
        samplesize = self.mic_stream.samplesize

        self.mic_stream.start()

        try:
            while True:
                frame: np.ndarray = self.mic_stream.read(n_bytes // samplesize)[0]
                frame = frame.flatten()
                self.save_frame(frame)
                new_buffer = frame.data.cast("B")

                self.azure_stream.write(new_buffer)
                time.sleep(0.01)
        finally:
            # stop recognition and clean up
            self.mic_stream.close()
            self.azure_stream.close()
            self.speech_recognizer.stop_continuous_recognition()

    def start_recog_continuous(self):
        self.speech_recognizer.start_continuous_recognition()
        while not self.done:
            time.sleep(0.5)

        self.speech_recognizer.stop_continuous_recognition()

    def recognize_once(self):
        print("start talking")
        result = self.speech_recognizer.recognize_once()

        # Check the result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

    def recognized_callback(self, event):
        recognized = event.result.text
        if recognized != "":
            print(f"RECOGNIZED: {recognized}")
            self.save_result(recognized)

    def stop_callback(self):
        self.speech_recognizer.stop_continuous_recognition()
        self.done = True
