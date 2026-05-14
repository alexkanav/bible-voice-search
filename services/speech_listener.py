import json
import logging
import queue
import threading

import sounddevice as sd
from vosk import KaldiRecognizer, Model

from config import AppConfig

logger = logging.getLogger(__name__)


class SpeechListener(threading.Thread):
    def __init__(
        self,
        output_queue: queue.Queue,
        config: AppConfig,
    ):
        super().__init__(daemon=True)

        self.config = config
        self.output_queue = output_queue

        self.stop_event = threading.Event()

        self.audio_queue = queue.Queue(maxsize=10)

        self.model = Model(config.vosk_model_path)
        self.recognizer = KaldiRecognizer(
            self.model,
            16000,
        )

    def audio_callback(
        self,
        indata,
        frames,
        time_info,
        status,
    ) -> None:
        if status:
            logger.warning(
                "Audio status: %s",
                status,
            )

        try:
            self.audio_queue.put_nowait(bytes(indata))
        except queue.Full:
            logger.warning("Audio queue full, dropping chunk")

    def recognize_speech(self) -> None:
        while not self.stop_event.is_set():

            try:
                data = self.audio_queue.get(timeout=self.config.queue_timeout)
            except queue.Empty:
                continue

            is_complete = self.recognizer.AcceptWaveform(data)

            if is_complete:
                result = json.loads(self.recognizer.Result())

                text = result.get("text", "")

                if text:
                    self.output_queue.put(text)

    def run(self) -> None:

        try:
            with sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype="int16",
                channels=1,
                device=self.config.device_index,
                callback=self.audio_callback,
            ):
                print("🎙️ Слухаю, говоріть у форматі: КНИГА ... ВІРШ ... ...")

                logger.info("Speech listener started")

                self.recognize_speech()

        except Exception:
            logger.exception("Audio stream error")

    def stop(self) -> None:
        self.stop_event.set()
