import json
import queue
from vosk import Model, KaldiRecognizer
import sounddevice as sd

from config import DEVICE_INDEX, MODEL_PATH


def recognize_speech_stream(output_queue):
    """
    Continuously listen to the microphone, recognize speech with Vosk,
    and put recognized text into output_queue.
    """
    def callback(indata, frames, time, status):
        if status:
            print("⚠️", status)
        audio_queue.put(bytes(indata))

    audio_queue = queue.Queue()
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, device=DEVICE_INDEX, callback=callback):
            print("🎙️ Слухаю, говоріть у форматі: КНИГА х ВІРШ х х")

            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        output_queue.put(text)
                else:
                    partial = json.loads(recognizer.PartialResult())
                    print("...partial:", partial["partial"])

    except Exception as e:
        print(f"🎧 Audio stream error: {e}")

