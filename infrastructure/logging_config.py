import logging


def setup_logging(log_file: str, level=logging.INFO) -> None:
    logging.basicConfig(
        filename=log_file,
        level=level,
        filemode="a",
        format="%(asctime)s %(levelname)s: %(message)s",
    )
