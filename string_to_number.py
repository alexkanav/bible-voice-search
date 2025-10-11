import logging


logger = logging.getLogger(__name__)


ONES = {
    "нуль": 0, "один": 1, "два": 2, "три": 3, "чотири": 4, "п'ять": 5,
    "шість": 6, "сім": 7, "вісім": 8, "дев'ять": 9
}

TEENS = {
    "десять": 10, "одинадцять": 11, "дванадцять": 12, "тринадцять": 13,
    "чотирнадцять": 14, "п'ятнадцять": 15, "шістнадцять": 16,
    "сімнадцять": 17, "вісімнадцять": 18, "дев'ятнадцять": 19
}

TENS = {
    "двадцять": 20, "тридцять": 30, "сорок": 40, "п'ятдесят": 50, "пятдесят": 50,
    "шістдесят": 60, "сімдесят": 70, "вісімдесят": 80, "дев'яносто": 90
}


def ukrainian_to_number(text: str) -> int:
    """
    Converts a Ukrainian number phrase (up to 99) into an integer.

    Args:
        text (str): Ukrainian number string.

    Returns:
        int: Numeric value of the input string. Returns 0 if no valid words found.
    """
    words = text.strip().lower().split()

    number = 0

    for word in words:
        if word in TEENS:
            number += TEENS[word]
        elif word in TENS:
            number += TENS[word]
        elif word in ONES:
            number += ONES[word]
        else:
            logger.error(f"Unknown number: {word}")

    return number

