import queue
import tkinter as tk
from collections.abc import Callable
from tkinter import font as tkfont

from config import AppConfig
from services.bible_service import BibleService
from services.speech_listener import SpeechListener


class BibleApp:
    def __init__(
        self,
        output_queue: queue.Queue,
        listener: SpeechListener,
        service: BibleService,
        text_layout: Callable[[str, AppConfig], tuple[str, tkfont.Font]],
        config: AppConfig,
    ):
        self.output_queue = output_queue
        self.listener = listener
        self.service = service
        self.text_layout = text_layout
        self.config = config

        self.root = tk.Tk()
        self.root.title(config.title)
        self.root.geometry(config.geometry)
        self.root.configure(bg=config.theme["bg"])

        self.output_label = tk.Label(
            self.root,
            text="",
            justify="left",
            bg=config.theme["bg"],
            fg=config.theme["fg"],
            anchor="center",
            wraplength=config.label_width,
        )
        self.output_label.pack(side="top", pady=(self.config.label_margin, 0))

        self.output_label_bottom = tk.Label(
            self.root,
            text="",
            justify="left",
            bg=config.theme["bg"],
            fg=config.theme["fg"],
            font=config.reference_font,
            wraplength=config.label_width,
        )
        self.output_label_bottom.pack(side="bottom", pady=(0, self.config.label_margin))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def poll_queue(self) -> None:
        try:
            while True:
                text = self.output_queue.get_nowait().rstrip()

                result = self.service.process_reference(text)

                if not result["success"]:
                    self.output_label.config(text=result["message"])
                    self.output_label_bottom.config(text=text)
                    continue

                wrapped_text, font = self.text_layout(
                    result["text"],
                    self.config,
                )

                self.output_label.config(text=wrapped_text, font=font)

                self.output_label_bottom.config(
                    text=f"{result['book_name']} - "
                    f"{result['chapter']}: "
                    f"{result['verse']}"
                )

        except queue.Empty:
            pass

        self.root.after(100, self.poll_queue)

    def run(self):
        self.poll_queue()
        self.root.mainloop()

    def on_close(self):
        print("Exiting application...")
        self.root.destroy()
