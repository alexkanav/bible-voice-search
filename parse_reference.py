import re
import logging

from string_to_number import ukrainian_to_number, TENS


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
            r'\b(?:вір(?:і|и|иш|ш|ша|ші|шів)?|більш(?:е|і)?|бірж(?:а|і|и)?)\b',
            text, flags=re.IGNORECASE
        )
        book_text = re.sub(r'\bкниг[аио]?\b', '', split_text[0], flags=re.IGNORECASE).strip()
        book = ukrainian_to_number(book_text)
        chapter_verse_txt = split_text[1].strip()

        if "сто" in chapter_verse_txt:
            chapter_verse_list = chapter_verse_txt.split("сто")
            chapter = ukrainian_to_number(chapter_verse_list[0])
            verse = ukrainian_to_number(chapter_verse_list[1]) + 100
            return book, chapter, verse

        chapter_verse_list = chapter_verse_txt.split()
        if len(chapter_verse_list) == 2:
            chapter = ukrainian_to_number(chapter_verse_list[0])
            verse = ukrainian_to_number(chapter_verse_list[1])
        elif len(chapter_verse_list) == 4:
            chapter = ukrainian_to_number(chapter_verse_list[0]) + ukrainian_to_number(chapter_verse_list[1])
            verse = ukrainian_to_number(chapter_verse_list[2]) + ukrainian_to_number(chapter_verse_list[3])
        elif len(chapter_verse_list) == 3:
            if chapter_verse_list[0] in TENS:
                chapter = ukrainian_to_number(chapter_verse_list[0]) + ukrainian_to_number(chapter_verse_list[1])
                verse = ukrainian_to_number(chapter_verse_list[2])
            else:
                chapter = ukrainian_to_number(chapter_verse_list[0])
                verse = ukrainian_to_number(chapter_verse_list[1]) + ukrainian_to_number(chapter_verse_list[2])

    except Exception as e:
        logger.exception("❌ Failed to parse Bible reference from text")

    return book, chapter, verse

