import sqlite3

from models.bible_query_result import BibleQueryResult
from utils.text_sanitizer import extract_plain_text


class BibleRepository:
    def __init__(self, db_path: str, max_verses: int) -> None:
        self.db_path = db_path
        self.max_verses = max_verses

    def get_verses(
        self,
        book: int,
        chapter: int,
        start_verse: int,
        additional_verses: int = 0,
    ) -> BibleQueryResult:
        end_verse = start_verse + min(additional_verses, self.max_verses - 1)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT long_name FROM books WHERE book_number = ?",
                (book,),
            )

            row = cursor.fetchone()

            if not row:
                return BibleQueryResult(
                    error="Невідома Книга, Вірш не знайдено.",
                )

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
                (book, chapter, start_verse, end_verse),
            )

            rows = cursor.fetchall()

            verses = [(verse, extract_plain_text(text)) for verse, text in rows]
            if not verses:
                return BibleQueryResult(
                    error=f"{book_name}, Вірш не знайдено.",
                )

            return BibleQueryResult(
                book_name=book_name,
                verses=verses,
            )
