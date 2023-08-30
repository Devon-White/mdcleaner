import os
from typing import Optional, Dict, Any, Union, Iterator
import chardet
import re
import logging

from unidecode import unidecode

logger = logging.getLogger('clean_md')


class FileReadError(Exception):
    pass


class EncodingDetectionError(Exception):
    pass


# Moved regex compilation outside of function to compile only once
COMPILED_REGEX = re.compile(r'\{([^{}]+)}')


def read_in_chunks(file, chunk_size: int) -> Iterator[bytes]:
    """Generator to read a file in chunks."""
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data


def detect_encoding(file_path: str,
                    num_bytes: Optional[Union[int, str]] = 1024,
                    encoding: str = 'utf-8') -> str:
    if encoding != 'auto':
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(num_bytes)
            return encoding
        except LookupError:
            logger.warning(
                f"File {file_path} cannot be read with the provided manual encoding '{encoding}'. Proceeding with automatic detection.")
        except Exception as e:
            logger.warning(
                f"Error reading file {file_path} with encoding '{encoding}': {e}. Proceeding with automatic detection.")

    # If encoding is 'auto' or there's an error with the provided encoding, detect encoding automatically
    detector = chardet.universaldetector.UniversalDetector()
    try:
        if num_bytes == 'auto':
            num_bytes = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            for block in read_in_chunks(f, min(num_bytes, 1024)):
                detector.feed(block)
                if detector.done:
                    break
                num_bytes -= 1024
            detector.close()
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        raise FileReadError(f"File {file_path} not found.")
    except OSError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise FileReadError(f"Error reading file {file_path}. Cause: {e}")
    except Exception as e:
        logger.error(f"Error detecting encoding: {e}")
        raise EncodingDetectionError(f"Error detecting encoding for {file_path}. Cause: {e}")

    if not detector.result['encoding']:
        logger.warning("chardet failed to detect encoding. Falling back to 'utf-8'.")
        return 'utf-8'

    return detector.result['encoding']


def perform_replacements(content: str, replacements: Optional[Dict[str, Any]] = None) -> str:
    return COMPILED_REGEX.sub(lambda m: replacement_callback(m, replacements), content)


def replacement_callback(match: 're.Match', replacements: Optional[Dict[str, Any]]) -> str:
    key: str = match.group(1)
    if not replacements or key not in replacements:
        logger.warning(f"No value found for template '{key}'. Retaining it as-is.")
        return match.group(0)
    return str(replacements[key])


def clean_md(file_path: str,
             contexts: Optional[Dict[str, Any]] = None,
             encoding_detection_bytes: Optional[Union[int, str]] = 1024,
             encoding: Optional[str] = 'utf-8') -> str:
    if not os.path.exists(file_path):
        raise FileReadError(f"File {file_path} not found.")
    try:
        encoding = detect_encoding(file_path, encoding_detection_bytes, encoding)
        with open(file_path, "r", encoding=encoding) as file:
            content = file.read()

        content = unidecode(content)
        content = perform_replacements(content, contexts)
        return content
    except (FileReadError, EncodingDetectionError):
        raise
    except Exception as e:
        raise FileReadError(f"Error reading or processing file {file_path}. Cause: {e}")
