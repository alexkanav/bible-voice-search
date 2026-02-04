import threading
import json
import queue
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import logging

from config import DEVICE_INDEX, MODEL_PATH, QUEUE_TIMEOUT

logger = logging.getLogger(__name__)


class SpeechListener(threading.Thread):
    def __init__(self, output_queue):
        super().__init__(daemon=True)
        self.output_queue = output_queue
        self.stop_event = threading.Event()

    def run(self):
        recognize_speech_stream(self.output_queue, self.stop_event)

    def stop(self):
        self.stop_event.set()


def recognize_speech_stream(output_queue, stop_event):
    """
    Continuously listen to the microphone, recognize speech with Vosk,
    and put recognized text into output_queue.
    """

    def callback(indata, frames, time_info, status):
        if status:
            logger.warning("Audio status: %s", status)

        try:
            audio_queue.put_nowait(bytes(indata))
        except queue.Full:
            pass

    audio_queue = queue.Queue(maxsize=10)
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, device=DEVICE_INDEX, callback=callback):
            print("🎙️ Слухаю, говоріть у форматі: КНИГА ... ВІРШ ... ...")

            while not stop_event.is_set():
                try:
                    data = audio_queue.get(timeout=QUEUE_TIMEOUT)
                except queue.Empty:
                    continue
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        output_queue.put(text)
                else:
                    partial = json.loads(recognizer.PartialResult())
                    print("...partial:", partial["partial"])

    except Exception as e:
        logger.exception("Audio stream error")
