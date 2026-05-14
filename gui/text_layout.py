import textwrap
import tkinter as tk
from tkinter import font as tkfont

from config import AppConfig


def fit_text_to_box(
    text: str,
    config: AppConfig,
) -> tuple[str, tkfont.Font]:
    """
    Calculates wrapped text and the largest fitting font.
    """
    for size in range(config.max_font_size, config.min_font_size - 1, -1):

        try:
            font = tkfont.Font(family=config.main_font_family, size=size)
        except tk.TclError:
            font = tkfont.Font(size=size)

        char_width = max(font.measure("M"), 1)
        line_height = max(font.metrics("linespace"), 1)

        chars_per_line = max(config.label_width // char_width, 1)
        lines_fit = max(config.label_height // line_height, 1)

        wrapped_text = textwrap.fill(
            text,
            width=chars_per_line,
        )

        actual_lines = wrapped_text.count("\n") + 1

        if actual_lines <= lines_fit:
            return wrapped_text, font

    wrapped_text = textwrap.fill(text, width=1)

    fallback_font = tkfont.Font(size=config.min_font_size)

    return wrapped_text, fallback_font
