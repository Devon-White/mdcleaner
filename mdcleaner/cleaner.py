import chardet
from unidecode import unidecode
from typing import Optional
import inspect


def detect_encoding(file_path: str) -> str:
    """Detects the encoding of a given file."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def clean_md(file_path: str, formatted: Optional[bool] = None) -> str:
    """
    Converts the content of a .md file to a cleaned ASCII format.
    If as_fstring is True, the contents inside {} are replaced with their respective values in the calling context.
    :param file_path: Path to the .md file
    :param formatted: If True, replaces the content inside {} with their respective values from the calling context.
    :return: Cleaned ASCII string
    """
    encoding = detect_encoding(file_path)

    with open(file_path, "r", encoding=encoding) as file:
        content = file.read()

    cleaned_content = unidecode(content)

    if formatted:
        # Get the calling frame
        frame = inspect.currentframe().f_back
        # Get both local and global variables from the calling context
        all_vars = {**frame.f_globals, **frame.f_locals}
        try:
            return cleaned_content.format(**all_vars)
        except KeyError as e:
            raise ValueError(f"Variable {e} not found in the scope. Make sure it's defined before calling clean_md."
                             f" Additionally, you can set the formatted option to false, or leave it as default.")

    return cleaned_content
