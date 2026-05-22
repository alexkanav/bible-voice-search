import logging
import re

from models.bible_reference import BibleReference
from utils.number_parser import ukrainian_to_number, TENS, ONES

logger = logging.getLogger(__name__)

BOOK_PATTERNS = (
    r"книг[аио]?",
    r"книжка",
)

VERSE_PATTERNS = (
    r"вір(?:і|и|иш|ш|ша|ші|шів|шем)?",
    r"більш(?:е|і)?",
    r"бірж(?:а|і|и)?",
)


def extract_reference_numbers(text: str) -> BibleReference | None:
    try:
        book_text, chapter_verse_text = _split_reference_parts(text)

        if chapter_verse_text is None:
            return None

        book = _parse_book(book_text)

        parsed_reference = _parse_chapter_verses(chapter_verse_text)
        if parsed_reference is None:
            return None

        chapter, start_verse, additional_verses = parsed_reference

        return BibleReference(
            book=book,
            chapter=chapter,
            start_verse=start_verse,
            additional_verses=additional_verses,
        )

    except ValueError:
        logger.exception("Failed to parse Bible reference from text: %r", text)
        return None


def _split_reference_parts(text: str) -> tuple[str, str | None]:
    pattern = rf"\b(?:{'|'.join(VERSE_PATTERNS)})\b"
    split_text = re.split(pattern, text, flags=re.IGNORECASE)

    if len(split_text) < 2:
        return text, None

    return split_text[0].strip(), split_text[1].strip()


def _parse_book(text: str) -> int:
    pattern = rf"\b{'|'.join(BOOK_PATTERNS)}\b"
    cleaned = re.sub(
        pattern,
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    return ukrainian_to_number(cleaned)


def _parse_chapter_verses(text: str) -> tuple[int, int, int] | None:
    verses = re.split(r"\bдалі\b", text, flags=re.IGNORECASE)
    additional = verses[1] if len(verses) >= 2 else None
    try:
        additional_verses = ukrainian_to_number(additional) if additional else 0
    except ValueError:
        additional_verses = 0

    parts = re.split(r"\bсто\b", verses[0], flags=re.IGNORECASE)
    if len(parts) == 2:
        first, second = parts
        return (
            ukrainian_to_number(first),
            ukrainian_to_number(second) + 100 if second else 100,
            additional_verses,
        )

    words = verses[0].split()

    match len(words):
        case 2:
            first, second = words

        case 3:
            if words[0] in TENS and words[1] in ONES:
                first = " ".join(words[:2])
                second = words[2]
            else:
                first = words[0]
                second = " ".join(words[1:])

        case 4:
            first = " ".join(words[:2])
            second = " ".join(words[2:])

        case _:
            return None

    return (
        ukrainian_to_number(first),
        ukrainian_to_number(second),
        additional_verses,
    )
