import tkinter as tk
import threading
import queue
import logging

from listen_speech import recognize_speech_stream
from parse_reference import extract_reference_numbers
from get_book_from_db import load_book_content
from config import LOG_FILE_PATH


# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s\n'
)


def main():
    """
    Launches the Bible voice assistant application.

    This function initializes the GUI window using Tkinter, starts a background thread
    for continuous speech recognition using Vosk, and displays recognized Bible references
    and their corresponding verse text from the database.

    Key components:
        - Starts `recognize_speech_stream` in a separate daemon thread
        - Uses a queue to receive recognized speech text
        - Parses recognized text to extract Bible reference (book, chapter, verse)
        - Fetches the verse text from a SQLite database
        - Displays results in a Tkinter GUI

    The GUI polls the speech recognition queue every 100ms and updates accordingly.
    """
    output_queue = queue.Queue()

    # Start listening in background thread
    threading.Thread(target=recognize_speech_stream, args=(output_queue,), daemon=True, name="SpeechListener").start()

    # Setup tkinter window
    root = tk.Tk()
    root.title("Біблія (переклад Турконяка 2020)")
    root.geometry("500x400")
    root.configure(bg='#2e2e2e')

    output_label = tk.Label(root, text="", wraplength=450, justify="left",
                            bg="#2e2e2e", fg="#ffffff", font=("Courier New", 12, "italic"))
    output_label.pack(pady=20)
    output_label_bottom = tk.Label(root, text="", wraplength=350, justify="left",
                                   bg="#2e2e2e", fg="#bbbbbb", font=("Helvetica", 8))
    output_label_bottom.pack(pady=20)

    # Function to poll the queue and update the label
    def poll_queue():
        try:
            while True:
                received_text = output_queue.get_nowait().rstrip()
                print(f"Ви шукаєте: {received_text}")

                book, chapter, verse = extract_reference_numbers(received_text)
                if not all((book, chapter, verse)):
                    output_label.config(text="Не вдалося розпізнати запит.")
                    output_label_bottom.config(text=received_text)
                    continue

                book_name, output_text = load_book_content(book, chapter, verse)
                output_label.config(text=output_text)
                output_label_bottom.config(text=f"{book_name.title()} - {chapter}: {verse}")

        except queue.Empty:
            pass
        root.after(100, poll_queue)  # Check again in 100ms

    def on_close():
        print("👋 Exiting application...")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    poll_queue()
    root.mainloop()


if __name__ == '__main__':
    main()
