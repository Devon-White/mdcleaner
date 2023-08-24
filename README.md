# MDCleaner

A utility to clean and convert MD files to ASCII.

## Installation

You can install MDCleaner via pip:

```python
pip install mdcleaner
```

## Usage

After installation, you can use the package in your Python script:

```python
from mdcleaner import clean_md

cleaned_content = clean_md("path_to_md_file.md")
print(cleaned_content)
```

## Features
Automatically detects file encoding.
Converts non-ASCII characters to their closest ASCII representation.

## Contributing
If you find any bugs or want to propose a new feature, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE.txt file for details.