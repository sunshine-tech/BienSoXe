def split_to_triples(string: str):
    """Split a string to many substrings of 3-character.

    For example, split "abcdef" to "abc", "def".
    """
    return tuple(string[i: i + 3] for i in range(0, len(string), 3))
