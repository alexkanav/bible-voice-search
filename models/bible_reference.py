from dataclasses import dataclass


@dataclass(frozen=True)
class BibleReference:
    book: int
    chapter: int
    start_verse: int
    additional_verses: int
