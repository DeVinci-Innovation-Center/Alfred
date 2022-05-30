import time
from typing import List, Optional

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import speech_py_impl as impl
from azure.cognitiveservices.speech.languageconfig import SourceLanguageConfig

from microphone import config as cfg


class OwnAutoDetectSourceLanguageConfig(
    speechsdk.languageconfig.AutoDetectSourceLanguageConfig
):
    """
    Superclass of AutoDetectSourceLanguageConfig to disable VSCode's
    Pylance `Code is unreachable` error.

    Represents auto detection source language configuration, allowing open
    range, specifying the potential source languages and corresponding
    customized endpoint

    The configuration can be initialized in different ways:

    - from open range: pass nothing, for source language auto detection in
    synthesis.
    - from languages: pass a list of potential source languages, for source
    language auto detection in recognition.
    - from sourceLanguageConfigs: pass a list of source language
    configurations, for source language auto detection in recognition.

    :param languages: The list of potential source languages. The language is
    specified in BCP-47 format
    :param sourceLanguageConfigs: The list of source language configurations
    """

    def __init__(
        self,
        languages: List[str] = None,
        sourceLanguageConfigs: List[SourceLanguageConfig] = None,
    ) -> None:
        if languages is not None and sourceLanguageConfigs is not None:
            raise ValueError(
                """languages and sourceLanguageConfigs cannot be both specified
                to create AutoDetectSourceLanguageConfig"""
            )
        self._impl = self._get_impl(
            impl.AutoDetectSourceLanguageConfig,
            languages,
            sourceLanguageConfigs,
        )


class AzureSpeech:
    def __init__(self, stream):

        stream_format = speechsdk.audio.AudioStreamFormat()

        speech_config = speechsdk.SpeechConfig(
            subscription=cfg.AZURE_KEY, region=cfg.AZURE_REGION
        )

        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        auto_lang = OwnAutoDetectSourceLanguageConfig(languages=cfg.AZURE_LANG)

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

    def save_result(self, result: str):
        self.result = result
        self.result_ready = True

    def read_result(self, check_ready=False) -> Optional[str]:
        """Returns last recognition result. If check_ready is True, returns None if
        the last results was already read."""

        if check_ready and not self.result_ready:
            return None

        self.result_ready = False
        return self.result

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
        print("RECOGNIZED {}".format(event.result.text))
        self.save_result(event.result.text)

    def stop_callback(self):
        self.speech_recognizer.stop_continuous_recognition()
        self.done = True
