import tkinter.font as tkfont

import pytest

from config import AppConfig
from gui.text_layout import fit_text_to_box


@pytest.fixture
def config():
    return AppConfig(
        label_width=300,
        label_height=100,
        min_font_size=10,
        max_font_size=30,
        main_font_family="Arial",
    )


def test_fit_text_to_box__short_text__uses_max_font_size(config, tk_root):
    text = "John 3:16"

    wrapped_text, font = fit_text_to_box(text, config)

    assert wrapped_text == text
    assert isinstance(font, tkfont.Font)
    assert font.cget("size") == config.max_font_size


def test_fit_text_to_box__long_text__wraps_text_and_scales_font(config, tk_root):
    text = "For God so loved the world that He gave " "His only begotten Son"

    wrapped_text, font = fit_text_to_box(text, config)

    assert "\n" in wrapped_text
    assert isinstance(font, tkfont.Font)
    assert config.min_font_size <= font.cget("size") <= config.max_font_size


def test_fit_text_to_box__box_too_small__uses_fallback_font(tk_root):
    config = AppConfig(
        label_width=1,
        label_height=1,
        min_font_size=8,
        max_font_size=20,
        main_font_family="Arial",
    )

    text = "Hello"

    wrapped_text, font = fit_text_to_box(text, config)

    assert wrapped_text == "H\ne\nl\nl\no"
    assert font.cget("size") == config.min_font_size


def test_fit_text_to_box__invalid_font_family__returns_valid_font(
    tk_root,
):
    config = AppConfig(
        label_width=300,
        label_height=100,
        min_font_size=10,
        max_font_size=20,
        main_font_family="NonexistentFont",
    )

    text = "Test text"

    wrapped_text, font = fit_text_to_box(text, config)

    assert isinstance(font, tkfont.Font)
    assert wrapped_text == text
