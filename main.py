import queue
import logging

from speech_listener import SpeechListener
from gui import BibleApp
from config import LOG_FILE_PATH

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s\n'
)


def main():
    output_queue = queue.Queue()
    listener = SpeechListener(output_queue)
    listener.start()  # starts background speech recognition
    app = BibleApp(output_queue, listener)
    app.run()


if __name__ == "__main__":
    main()
