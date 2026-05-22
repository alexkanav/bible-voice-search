from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceResult:
    input_text: str | None = None
    book_name: str | None = None
    chapter: int | None = None
    start_verse: int | None = None
    verses: list[tuple[int, str]] | None = None
    error: str | None = None
