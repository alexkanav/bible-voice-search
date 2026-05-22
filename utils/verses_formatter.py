def format_verses(
    verses_list: list[tuple[int, str]], sep: str = ":  ", line_sep: str = "\n\n"
) -> str:
    """
    Formats a list of numbered verses into a string.

    Args:
        verses_list: iterable of tuples (number, content)
        sep: separator between number and content
        line_sep: separator between lines

    Returns:
        str: formatted text
    """
    formatted_verses = (f"{number}{sep}{content}" for number, content in verses_list)
    return line_sep.join(formatted_verses)
