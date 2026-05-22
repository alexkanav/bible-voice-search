from collections.abc import Callable

from models.bible_reference import BibleReference
from models.service_result import ServiceResult
from repositories.bible_repository import BibleRepository


class BibleService:
    def __init__(
        self,
        repository: BibleRepository,
        parser: Callable[[str], BibleReference | None],
    ) -> None:
        self.repository = repository
        self.parser = parser

    def process_reference(self, text: str) -> ServiceResult:
        reference = self.parser(text)
        if reference is None:
            return ServiceResult(
                input_text=text,
                error="Не вдалося розпізнати запит.",
            )

        result = self.repository.get_verses(
            reference.book,
            reference.chapter,
            reference.start_verse,
            reference.additional_verses,
        )
        if result.error:
            return ServiceResult(
                input_text=f"{reference.book}, {reference.chapter}, {reference.start_verse}",
                error=result.error,
            )

        return ServiceResult(
            book_name=result.book_name,
            chapter=reference.chapter,
            start_verse=reference.start_verse,
            verses=result.verses,
        )
