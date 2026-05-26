import pytest

from parsers.reference_parser import extract_reference_numbers
from models.bible_reference import BibleReference


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "книга п'ять вірш три дев'ять",
            (5, 3, 9, 0),
        ),
        (
            "книга п'ять вірш три шістнадцять далі два",
            (5, 3, 16, 2),
        ),
        (
            "книга п'ять вірш три шістнадцять далі xyz",
            (5, 3, 16, 0),
        ),
        (
            "книга п'ять вірш одинадцять шістнадцять далі вісім",
            (5, 11, 16, 8),
        ),
        (
            "книга два вірш двадцять один",
            (2, 20, 1, 0),
        ),
        (
            "книга двадцять вірш двадцять один чотири",
            (20, 21, 4, 0),
        ),
        (
            "книга п'ятнадцять вірш двадцять один чотири",
            (15, 21, 4, 0),
        ),
        (
            "книга сорок три вірш двадцять двадцять",
            (43, 20, 20, 0),
        ),
        (
            "книга сорок три вірш тридцять двадцять два",
            (43, 30, 22, 0),
        ),
        (
            "книга сорок три вірш тридцять три двадцять два",
            (43, 33, 22, 0),
        ),
        (
            "книга чотири вірш двадцять сто",
            (4, 20, 100, 0),
        ),
        (
            "книга один вірш три сто п'ять",
            (1, 3, 105, 0),
        ),
        (
            "книга один вірш три сто сімдесят п'ять",
            (1, 3, 175, 0),
        ),
    ],
)
def test_extract_reference_numbers__valid_inputs__returns_numbers(
    text,
    expected,
):
    result = extract_reference_numbers(text)

    assert result == BibleReference(*expected)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "книга abc",
        "книга один",
        "вірш xyz",
        "вірш один",
        "книга abc вірш xyz",
        "книга один три шістнадцять",
        "книга один вірш три три три",
    ],
)
def test_extract_reference_numbers__invalid_inputs__returns_none(text):
    result = extract_reference_numbers(text)

    assert result is None
