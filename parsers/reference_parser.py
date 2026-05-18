import logging
import re

from utils.number_parser import ukrainian_to_number, TENS, ONES

logger = logging.getLogger(__name__)


def extract_reference_numbers(text: str) -> tuple[int, int, int]:
    """
    Parses a Ukrainian Bible reference string and returns book, chapter, and verse as integers.

    Args:
        text (str): Input string with spoken or written reference.

    Returns:
        tuple[int, int, int]: Parsed (book_number, chapter_number, verse_number).
                              Defaults to 0s if parsing fails.
    """
    book = chapter = verse = 0
    try:
        split_text = re.split(
            r"\b(?:вір(?:і|и|иш|ш|ша|ші|шів)?|більш(?:е|і)?|бірж(?:а|і|и)?)\b",
            text,
            flags=re.IGNORECASE,
        )

        if len(split_text) < 2:
            return 0, 0, 0

        book_text = re.sub(
            r"\bкниг[аио]?\b", "", split_text[0], flags=re.IGNORECASE
        ).strip()
        book = ukrainian_to_number(book_text)

        chapter_verse_txt = split_text[1].strip()

        parts = re.split(r"\bсто\b", chapter_verse_txt, flags=re.IGNORECASE)
        if len(parts) == 2:
            chapter, verse = parts
            return book, ukrainian_to_number(chapter), ukrainian_to_number(verse) + 100 if verse else 100,

        words = chapter_verse_txt.split()

        match len(words):
            case 2:
                chapter, verse = words

            case 3:
                if words[0] in TENS and words[1] in ONES:
                    chapter = " ".join(words[:2])
                    verse = words[2]
                else:
                    chapter = words[0]
                    verse = " ".join(words[1:])

            case 4:
                chapter = " ".join(words[:2])
                verse = " ".join(words[2:])

            case _:
                return 0, 0, 0

    except ValueError:
        logger.exception("Failed to parse Bible reference from text: %r", text)

    return book, ukrainian_to_number(chapter), ukrainian_to_number(verse)
