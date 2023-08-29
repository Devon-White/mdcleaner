import chardet
import re
from unidecode import unidecode
from typing import Optional, Match, Dict, Set, List, Any
import inspect
import logging

# Configure the logging module
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')


def detect_encoding(file_path: str) -> str:
    """Detects the encoding of a given file."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def clean_md(file_path: str, formatted: Optional[bool] = False) -> str:
    """
    Converts the content of a .md file to a cleaned ASCII format.
    If formatted is True, the contents inside {} are replaced with their respective values in the calling context.
    Double brackets {{}} and unmatched single brackets are considered improperly formatted.
    :param file_path: Path to the .md file
    :param formatted: If True, replaces the content inside {} with their respective values from the calling context.
    :return: Cleaned ASCII string
    """

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    cleaned_content = unidecode(content)

    if formatted:
        # Get the calling frame
        frame: inspect.FrameType = inspect.currentframe().f_back
        # Get both local and global variables from the calling context
        all_vars: Dict[str, Any] = {**frame.f_globals, **frame.f_locals}

        # Identify and log improperly formatted templates, including double brackets
        misformatted_templates: Set[str] = set(re.findall(r'\{{2,}[^}]+?}}|\{[^})]+?\)', cleaned_content))
        for template in misformatted_templates:
            logging.getLogger('clean_md').warning(
                f"Improperly formatted template: '{template}'. Retaining it as-is.")
            cleaned_content = cleaned_content.replace(template, template)  # Retain as is

        # List to hold parts of misformatted templates that should be ignored
        ignore_list: List[str] = []
        for misformatted in misformatted_templates:
            if misformatted.startswith("{{") and misformatted.endswith("}}"):
                inner_part: str = "{" + misformatted[2:-2]
                ignore_list.append(inner_part)

        # Only process templates not in the ignore_list
        def replacement_callback(match: Match[str]) -> str:
            template: str = match.group(0)
            key: str = match.group(1)
            if template in ignore_list:
                return template  # Return as is
            if key not in all_vars:
                logging.getLogger('clean_md').warning(
                    f"No value found for template '{key}'. Retaining it as-is.")
                return template  # Return the original if not found or invalid
            return all_vars[key]

        # Use re.sub with callback to replace single bracket templates
        cleaned_content = re.sub(r'\{(?![{])([^})]+?)}(?!})', replacement_callback, cleaned_content)

    return cleaned_content
