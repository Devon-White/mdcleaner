
# MDCleaner

A utility to clean and convert MD files to ASCII.

## Installation

You can install MDCleaner via pip:

```bash
pip install mdcleaner
```

## Usage

After installation, you can use the package in your Python scripts:

```python
from mdcleaner import clean_md

cleaned_content = clean_md("path_to_md_file.md")
print(cleaned_content)
```

## Features

- **Encoding Detection**: The utility can automatically detect the file's encoding to ensure compatibility with various text files.
- **ASCII Conversion**: Converts non-ASCII characters to their closest ASCII representation using the `unidecode` library.
- **Template Replacements**: Provides an easy way to replace placeholders within the MD files with specific content.
- **Graceful Error Handling**: Provides warnings for unmatched templates, ensuring placeholders without corresponding replacements are retained as-is. Additionally, handles improperly formatted templates and gives clear warnings.

### Using templates in your Markdown file

Imagine you have an MD file named `sample.md` with the following content:

```markdown
This is a test: {my_variable}
```

In your script, you can replace the `{my_variable}` placeholder with a specific value:

```python
from mdcleaner import clean_md

replacements = {'my_variable': 'Hello, World!'}
cleaned_content = clean_md("sample.md", contexts=replacements)
print(cleaned_content)  # This will print: "This is a test: Hello, World!"
```

By passing the `contexts` parameter with a dictionary, any placeholders inside `{}` in your MD file will be replaced by the corresponding values.

### Encoding Detection

MDCleaner reads a certain number of bytes from the file to determine its encoding:

- By default, it reads the first 1024 bytes.
- You can specify a different number of bytes using the `encoding_detection_bytes` parameter.
- If you set `encoding_detection_bytes` to 'auto', the entire file will be read to determine its encoding.
- If no encoding is specified, the default option used is `utf-8`.

Example:

```python
clean_md("sample.md", encoding_detection_bytes=500)
```

### Manual Encoding

If you're certain about the encoding of your file, you can specify it directly using the `encoding` parameter, which bypasses the automatic detection process:

```python
clean_md("sample.md", encoding="utf-8")
```

## Contributing

If you find any bugs or want to propose a new feature, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE.txt file for details.
