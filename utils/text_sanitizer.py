import re


def extract_plain_text(text: str) -> str:
    return re.sub(r"<f>.*?</f>|</?[^>]+>", "", text.strip())
