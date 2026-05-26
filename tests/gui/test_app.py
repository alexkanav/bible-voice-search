import queue
import tkinter.font as tkfont
from unittest.mock import MagicMock

import pytest

from config import AppConfig
from gui.app import BibleApp
from models.service_result import ServiceResult


@pytest.fixture
def config():
    return AppConfig(
        label_width=300,
        label_height=100,
        min_font_size=10,
        max_font_size=30,
        main_font_family="Arial",
    )


@pytest.fixture
def mocks():
    return {
        "queue": queue.Queue(),
        "listener": MagicMock(),
        "service": MagicMock(),
        "text_layout": MagicMock(),
    }


@pytest.fixture
def app(config, mocks, tk_root):
    return BibleApp(
        output_queue=mocks["queue"],
        service=mocks["service"],
        text_layout=mocks["text_layout"],
        config=config,
    )


def test_init__valid_data__sets_theme_and_title(
    app,
    config,
):
    assert app.root.title() == config.title

    assert app.main_label.cget("bg") == config.theme["bg"]
    assert app.main_label.cget("fg") == config.theme["fg"]

    assert app.footer_label.cget("bg") == config.theme["bg"]

    assert app.footer_label.cget("fg") == config.theme["fg"]


def test_poll_queue__valid_reference__updates_labels(
    app,
    mocks,
    config,
):
    mocks["queue"].put("книга десять вірш три шістнадцять")

    mocks["service"].process_reference.return_value = ServiceResult(
        input_text="книга десять вірш три шістнадцять",
        book_name="John",
        chapter=3,
        start_verse=16,
        verses=[(3, "For God so loved the world")],
        error=None,
    )

    font = tkfont.Font(size=20)

    mocks["text_layout"].return_value = (
        "Wrapped text",
        font,
    )

    app.poll_queue()

    assert app.main_label.cget("text") == "Wrapped text"

    assert app.footer_label.cget("text") == "John - 3: 16"

    mocks["service"].process_reference.assert_called_once_with(
        "книга десять вірш три шістнадцять"
    )

    mocks["text_layout"].assert_called_once_with(
        "3:  For God so loved the world",
        config,
    )


def test_poll_queue__invalid_reference__shows_error_message(
    app,
    mocks,
):
    mocks["queue"].put("invalid reference")

    mocks["service"].process_reference.return_value = ServiceResult(
        error="Reference not found",
        input_text="invalid reference",
    )

    app.poll_queue()

    assert app.main_label.cget("text") == "Reference not found"

    assert app.footer_label.cget("text") == "invalid reference"


def test_poll_queue__empty_queue__does_not_raise(app):
    app.poll_queue()


def test_on_close__called__destroys_root(app):
    app.root.destroy = MagicMock()

    app.on_close()

    app.root.destroy.assert_called_once()
