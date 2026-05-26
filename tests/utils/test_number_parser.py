import pytest

from utils.number_parser import ukrainian_to_number


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("нуль", 0),
        ("один", 1),
        ("п'ять", 5),
        ("десять", 10),
        ("шістнадцять", 16),
        ("двадцять", 20),
        ("тридцять", 30),
        ("сорок", 40),
        ("двадцять один", 21),
        ("тридцять п'ять", 35),
        ("дев'яносто дев'ять", 99),
        ("пятдесят два", 52),
    ],
)
def test_ukrainian_to_number__valid_numbers__returns_number(
    text,
    expected,
):
    result = ukrainian_to_number(text)

    assert result == expected


def test_ukrainian_to_number__uppercase_input__returns_number():
    result = ukrainian_to_number("ДВАДЦЯТЬ ОДИН")

    assert result == 21


def test_ukrainian_to_number__extra_spaces__returns_number():
    result = ukrainian_to_number("  двадцять    три  ")

    assert result == 23


def test_ukrainian_to_number__one_unknown_word__raises_value_error():
    with pytest.raises(ValueError, match="Unknown number: apple"):
        ukrainian_to_number("apple")


def test_ukrainian_to_number__two_unknown_words__raises_value_error():
    with pytest.raises(ValueError, match="Invalid number phrase: три apple"):
        ukrainian_to_number("три apple")


def test_ukrainian_to_number__unsupported_words__raises_value_error():
    with pytest.raises(
        ValueError, match=r"Unsupported number format \(0–99 only\): сто двадцять три"
    ):
        ukrainian_to_number("сто двадцять три")
