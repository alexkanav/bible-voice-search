import logging
import queue

from config import AppConfig
from gui.app import BibleApp
from gui.text_layout import fit_text_to_box
from infrastructure.logging_config import setup_logging
from parsers.reference_parser import extract_reference_numbers
from repositories.bible_repository import BibleRepository
from services.bible_service import BibleService
from services.speech_listener import SpeechListener

config = AppConfig()

setup_logging(config.log_file_path, logging.ERROR)


def main():
    output_queue = queue.Queue()

    repository = BibleRepository(config.db_path)

    bible_service = BibleService(
        repository=repository,
        parser=extract_reference_numbers,
    )

    listener = SpeechListener(
        output_queue=output_queue,
        config=config,
    )
    listener.start()

    app = BibleApp(
        output_queue=output_queue,
        listener=listener,
        service=bible_service,
        text_layout=fit_text_to_box,
        config=config,
    )

    try:
        app.run()
    finally:
        listener.stop()
        listener.join()


if __name__ == "__main__":
    main()
