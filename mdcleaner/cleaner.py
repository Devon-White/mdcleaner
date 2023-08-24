# cleaner.py

import chardet
from unidecode import unidecode


def detect_encoding(file_path):
    """Detects the encoding of a given file."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def clean_md(file_path):
    """
    Converts the content of a .md file to a cleaned ASCII format.
    :param file_path: Path to the .md file
    :return: Cleaned ASCII string
    """
    encoding = detect_encoding(file_path)

    with open(file_path, "r", encoding=encoding) as file:
        content = file.read()

    # Transliterate non-ASCII characters using unidecode
    return unidecode(content)
