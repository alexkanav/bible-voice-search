import sqlite3
import re

from config import DB_PATH


def load_book_content(book: int, chapter: int, verse_start: int, verse_end: int = None) -> tuple[str, str]:
    """
    Fetches the text of a specific Bible verse or a range of verses from a SQLite database.

    Args:
        book (int): The numerical ID of the book (e.g. 1 for Genesis).
        chapter (int): The chapter number within the book.
        verse_start (int): The starting verse number.
        verse_end (int, optional): The ending verse number. If not provided, only `verse_start` is used.

    Returns:
        tuple[str, str]: A tuple containing:
            - The full name of the book (str).
            - The formatted verse text (str).
              If the book or verses are not found, returns an appropriate fallback message.
    """
    verse_end = verse_end or verse_start
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Fetch book name
        cursor.execute("SELECT long_name FROM books WHERE book_number = ?", (book,))
        row = cursor.fetchone()
        if not row:
            return "Невідома Книга", "Вірш не знайдено."
        (book_name,) = row

        # Fetch verse(s)
        cursor.execute("""
            SELECT verse, text
            FROM verses
            WHERE book_number = ? AND chapter = ? AND verse BETWEEN ? AND ?
        """, (book, chapter, verse_start, verse_end))

        verses = [
            f"{v[0]}: {re.sub(r'</?[^>]+>', '', v[1])}"
            for v in cursor.fetchall()
        ]

        if not verses:
            return book_name, "Вірш не знайдено."

        return book_name, "\n\n".join(verses)

