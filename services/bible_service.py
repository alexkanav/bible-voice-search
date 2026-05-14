from collections.abc import Callable

from repositories.bible_repository import BibleRepository


class BibleService:
    def __init__(
        self, repository: BibleRepository, parser: Callable[[str], tuple[int, int, int]]
    ):
        self.repository = repository
        self.parser = parser

    def process_reference(self, text: str) -> dict[str, str | bool | int]:
        book, chapter, verse = self.parser(text)

        if not all((book, chapter, verse)):
            return {
                "success": False,
                "message": "Не вдалося розпізнати запит.",
                "input": text,
            }

        book_name, verse_text = self.repository.get_verses(
            book,
            chapter,
            verse,
        )

        return {
            "success": True,
            "book_name": book_name,
            "chapter": chapter,
            "verse": verse,
            "text": verse_text,
        }
