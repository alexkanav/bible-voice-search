import sqlite3

from utils.text_sanitizer import extract_plain_text


class BibleRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_verses(
        self,
        book: int,
        chapter: int,
        verse_start: int,
        verse_end: int | None = None,
    ) -> tuple[str, str]:
        if verse_end is None:
            verse_end = verse_start

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT long_name FROM books WHERE book_number = ?",
                (book,),
            )

            row = cursor.fetchone()

            if not row:
                return "Невідома Книга", "Вірш не знайдено."

            (book_name,) = row

            cursor.execute(
                """
                SELECT verse, text
                FROM verses
                WHERE book_number = ?
                AND chapter = ?
                AND verse BETWEEN ? AND ?
                ORDER BY verse
                """,
                (book, chapter, verse_start, verse_end),
            )

            rows = cursor.fetchall()

            verses = [f"{verse}: {extract_plain_text(text)}" for verse, text in rows]
            if not verses:
                return book_name, "Вірш не знайдено."

            return book_name, "\n\n".join(verses)
