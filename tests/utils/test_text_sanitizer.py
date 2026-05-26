import pytest

from utils.text_sanitizer import extract_plain_text


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        ("Hello world", "Hello world"),
        ("  Hello world  ", "Hello world"),
        ("<f>ignored</f>Hello", "Hello"),
        ("Hello<f>ignored</f>", "Hello"),
        ("<b>Hello</b>", "Hello"),
        ("Hello <i>world</i>", "Hello world"),
        ("<f>remove</f><b>Hi</b>", "Hi"),
        ("<f>remove</f><i>text</i><b>ok</b>", "textok"),
    ],
)
def test_extract_plain_text__formatted_text__returns_clean_text(
    input_text,
    expected,
):
    result = extract_plain_text(input_text)

    assert result == expected


def test_extract_plain_text__empty_string__returns_empty_string():
    assert extract_plain_text("") == ""


def test_extract_plain_text__only_tags__returns_empty_string():
    assert extract_plain_text("<f>test</f><b></b>") == ""
