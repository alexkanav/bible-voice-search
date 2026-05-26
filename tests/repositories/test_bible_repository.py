import sqlite3

import pytest

from repositories.bible_repository import BibleRepository


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test_bible.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE books (
            book_number INTEGER PRIMARY KEY,
            long_name TEXT
        )
        """)

    cursor.execute("""
        CREATE TABLE verses (
            book_number INTEGER,
            chapter INTEGER,
            verse INTEGER,
            text TEXT
        )
        """)

    cursor.execute("""
        INSERT INTO books (book_number, long_name)
        VALUES (1, 'Буття')
        """)

    cursor.executemany(
        """
        INSERT INTO verses (
            book_number,
            chapter,
            verse,
            text
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (1, 1, 1, "<FI>На початку створив Бог небо та землю.<Fi>"),
            (1, 1, 2, "<f>ⓑ</f>Земля ж була порожньою і безжиттєвою; безодню <i>вкривала</i> темрява"),
            (1, 1, 3, "Дух Божий ширяв над поверхнею води"),
        ],
    )

    conn.commit()
    conn.close()

    return str(db_path)


@pytest.fixture
def repository(test_db):
    return BibleRepository(test_db, 2)


@pytest.mark.parametrize(
    ("additional_verses", "verses"),
    [
        (0, [(1, "На початку створив Бог небо та землю.")]),
        (1, [
                (1, "На початку створив Бог небо та землю."),
                (2, "Земля ж була порожньою і безжиттєвою; безодню вкривала темрява"),
            ],
        ),
        (3, [
                (1, "На початку створив Бог небо та землю."),
                (2, "Земля ж була порожньою і безжиттєвою; безодню вкривала темрява"),
            ],
        ),
    ],
)
def test_get_verses__verse_range__returns_verses(repository, additional_verses, verses):
    result = repository.get_verses(
        book=1,
        chapter=1,
        start_verse=1,
        additional_verses=additional_verses,
    )

    assert result.book_name == "Буття"

    assert result.verses == verses


def test_get_verses__unknown_book__returns_error_message(
    repository,
):
    result = repository.get_verses(
        book=999,
        chapter=1,
        start_verse=1,
    )

    assert result.error == "Невідома Книга, Вірш не знайдено."


def test_get_verses__missing_verse__returns_not_found_message(
    repository,
):
    result = repository.get_verses(
        book=1,
        chapter=1,
        start_verse=99,
    )

    assert result.error == "Буття, Вірш не знайдено."


def test_get_verses__default_verse_end__uses_verse_start(
    repository,
):
    result = repository.get_verses(
        book=1,
        chapter=1,
        start_verse=1,
    )

    assert result.book_name == "Буття"

    assert result.verses == [(1, "На початку створив Бог небо та землю.")]
