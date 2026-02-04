import tkinter as tk
from tkinter import font as tkfont
import textwrap
import queue

from config import WIDTH, HEIGHT, FONT_FAMILY, FONT_COLOR, BG_COLOR, FONT_SMALL
from parse_reference import extract_reference_numbers
from get_book_from_db import load_book_content


class BibleApp:
    def __init__(self, output_queue, listener):
        self.queue = output_queue
        self.listener = listener
        self.root = tk.Tk()
        self.root.title("Біблія (переклад Турконяка 2020)")
        self.root.geometry(f"{WIDTH + 20}x{HEIGHT + 80}")
        self.root.configure(bg=BG_COLOR)

        self.output_label = tk.Label(self.root, text="", justify="left", bg=BG_COLOR, fg=FONT_COLOR, anchor="center",
                                     wraplength=WIDTH)
        self.output_label.pack(pady=20)
        self.output_label_bottom = tk.Label(self.root, text="", justify="left", bg=BG_COLOR, fg=FONT_COLOR,
                                            font=FONT_SMALL, wraplength=WIDTH)
        self.output_label_bottom.pack(pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.poll_queue()

    def poll_queue(self):
        try:
            while True:
                received_text = self.queue.get_nowait().rstrip()
                print(f"Ви шукаєте: {received_text}")

                book, chapter, verse = extract_reference_numbers(received_text)
                if not all((book, chapter, verse)):
                    self.output_label.config(text="Не вдалося розпізнати запит.")
                    self.output_label_bottom.config(text=received_text)
                    continue

                book_name, output_text = load_book_content(book, chapter, verse)
                self.fit_wrapped_text_to_label(self.output_label, output_text)
                self.output_label_bottom.config(text=f"{book_name.title()} - {chapter}: {verse}")

        except queue.Empty:
            pass

        self.root.after(100, self.poll_queue)

    def on_close(self):
        print("Exiting application...")
        self.listener.stop()
        self.listener.join()  # waits for the thread to finish
        self.root.destroy()

    @staticmethod
    def fit_wrapped_text_to_label(label, text: str):
        """Dynamically fits the verse text to a Tkinter Label using font sizing and word wrapping."""
        max_font_size = 100
        min_font_size = 5

        for size in range(max_font_size, min_font_size - 1, -1):
            try:
                fnt = tkfont.Font(family=FONT_FAMILY, size=size)
            except tk.TclError:
                fnt = tkfont.Font(size=size)  # Default system font
            char_width = fnt.measure("M")  # Rough width of one character
            line_height = fnt.metrics("linespace")

            chars_per_line = max(WIDTH // char_width, 1)
            lines_fit = max(HEIGHT // line_height, 1)

            # Wrap text
            wrapped = textwrap.fill(text, width=chars_per_line)

            # Count lines
            actual_lines = wrapped.count('\n') + 1
            if actual_lines <= lines_fit:
                label.config(text=wrapped, font=fnt)
                break

    def run(self):
        self.root.mainloop()
