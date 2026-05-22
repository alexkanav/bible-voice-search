import queue
import tkinter as tk
from collections.abc import Callable
from tkinter import font as tkfont

from config import AppConfig
from services.bible_service import BibleService
from utils.verses_formatter import format_verses


class BibleApp:
    def __init__(
        self,
        output_queue: queue.Queue[str],
        service: BibleService,
        text_layout: Callable[[str, AppConfig], tuple[str, tkfont.Font]],
        config: AppConfig,
    ) -> None:
        self.output_queue = output_queue
        self.service = service
        self.text_layout = text_layout
        self.config = config

        self.root = tk.Tk()
        self.root.title(self.config.title)
        self.root.geometry(self.config.geometry)
        self.root.configure(bg=self.config.theme["bg"])

        self.main_label = tk.Label(
            self.root,
            text="",
            justify="left",
            bg=self.config.theme["bg"],
            fg=self.config.theme["fg"],
            anchor="center",
            wraplength=self.config.label_width,
        )
        self.main_label.pack(side="top", pady=(self.config.label_margin, 0))

        self.footer_label = tk.Label(
            self.root,
            text="",
            justify="left",
            bg=self.config.theme["bg"],
            fg=self.config.theme["fg"],
            font=self.config.footer_font,
            wraplength=self.config.label_width,
        )
        self.footer_label.pack(side="bottom", pady=(0, self.config.label_margin))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def poll_queue(self) -> None:
        try:
            while True:
                text = self.output_queue.get_nowait().rstrip()

                result = self.service.process_reference(text)

                if result.error:
                    self.main_label.config(
                        text=result.error,
                        fg=self.config.error_fg,
                        font=self.config.error_font,
                    )
                    self.footer_label.config(text=result.input_text)
                    continue

                text = format_verses(result.verses)

                wrapped_text, font = self.text_layout(
                    text,
                    self.config,
                )

                self.main_label.config(
                    text=wrapped_text, fg=self.config.theme["fg"], font=font
                )

                self.footer_label.config(
                    text=f"{result.book_name} - "
                    f"{result.chapter}: "
                    f"{result.start_verse}"
                )

        except queue.Empty:
            pass

        self.root.after(
            int(self.config.queue_timeout * 1000),
            self.poll_queue,
        )

    def run(self) -> None:
        self.poll_queue()
        self.root.mainloop()

    def on_close(self) -> None:
        print("Exiting application...")
        self.root.destroy()
