from dataclasses import dataclass


@dataclass(frozen=True)
class BibleQueryResult:
    book_name: str | None = None
    verses: list[tuple[int, str]] | None = None
    error: str | None = None

