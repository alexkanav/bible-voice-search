from unittest.mock import MagicMock

import pytest

from models.bible_query_result import BibleQueryResult
from models.bible_reference import BibleReference
from models.service_result import ServiceResult
from services.bible_service import BibleService


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def parser():
    return MagicMock()


@pytest.fixture
def service(repository, parser):
    return BibleService(
        repository=repository,
        parser=parser,
    )


def test_process_reference__valid_reference__returns_success_result(
    service,
    repository,
    parser,
):
    parser.return_value = BibleReference(
        book=43,
        chapter=3,
        start_verse=16,
        additional_verses=0,
    )

    repository.get_verses.return_value = BibleQueryResult(
        book_name="John",
        verses=[(16, "For God so loved the world")],
    )

    result = service.process_reference("John 3:16")

    assert result == ServiceResult(
        book_name="John",
        chapter=3,
        start_verse=16,
        verses=[(16, "For God so loved the world")],
    )
    service.parser.assert_called_once_with("John 3:16")

    service.repository.get_verses.assert_called_once_with(43, 3, 16, 0)


def test_process_reference__invalid_input_reference__returns_error(
    service,
    parser,
    repository,
):
    parser.return_value = None

    result = service.process_reference("invalid input")

    assert result == ServiceResult(
        input_text="invalid input", error="Не вдалося розпізнати запит."
    )

    repository.get_verses.assert_not_called()


def test_process_reference__verse_not_found__returns_error(
    service,
    repository,
    parser,
):
    parser.return_value = BibleReference(
        book=43,
        chapter=3,
        start_verse=16,
        additional_verses=0,
    )

    repository.get_verses.return_value = BibleQueryResult(
        error="Вірш не знайдено.",
    )

    result = service.process_reference("буття 1:999")

    assert result == ServiceResult(
        input_text="43, 3, 16",
        error="Вірш не знайдено.",
    )
