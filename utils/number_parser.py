ONES = {
    "нуль": 0,
    "один": 1,
    "два": 2,
    "три": 3,
    "чотири": 4,
    "п'ять": 5,
    "шість": 6,
    "сім": 7,
    "вісім": 8,
    "дев'ять": 9,
}

TEENS = {
    "десять": 10,
    "одинадцять": 11,
    "дванадцять": 12,
    "тринадцять": 13,
    "чотирнадцять": 14,
    "п'ятнадцять": 15,
    "шістнадцять": 16,
    "сімнадцять": 17,
    "вісімнадцять": 18,
    "дев'ятнадцять": 19,
}

TENS = {
    "двадцять": 20,
    "тридцять": 30,
    "сорок": 40,
    "п'ятдесят": 50,
    "пятдесят": 50,
    "шістдесят": 60,
    "сімдесят": 70,
    "вісімдесят": 80,
    "дев'яносто": 90,
}

NUMBER_WORDS = ONES | TEENS | TENS


def ukrainian_to_number(text: str) -> int:
    """
    Converts a Ukrainian number phrase (0–99) into an integer.

    Args:
        text (str): Ukrainian number phrase.

    Returns:
        int: Numeric value of the input phrase.

    Raises:
        ValueError: If the phrase is invalid or unsupported.
    """
    words = text.strip().lower().replace("’", "'").replace("`", "'").split()

    if len(words) == 1:
        number = NUMBER_WORDS.get(words[0])

        if number is None:
            raise ValueError(f"Unknown number: {words[0]}")

        return number

    if len(words) == 2:
        tens = TENS.get(words[0])
        ones = ONES.get(words[1])

        if tens is None or ones is None:
            raise ValueError(f"Invalid number phrase: {text}")

        return tens + ones

    raise ValueError(f"Unsupported number format (0–99 only): {text}")
