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
- Automatically detects file encoding.
- Converts non-ASCII characters to their closest ASCII representation.
- Provides warnings for unmatched templates, ensuring placeholders without corresponding variables are retained as-is.
- Handles improperly formatted templates, like unmatched curly braces {, and gives a clear warning while returning the content as-is.

### Using templates in your Markdown file
Imagine you have an MD file named `sample.md` with the following content:
```markdown
This is a test: {my_variable}
```
In your script, you can replace the `{my_variable}` placeholder with the value of a variable defined in your script:

```python
from mdcleaner import clean_md

# Read and format the content of "sample.md"
replacements = {'user_name': 'Devon', 'role': 'admin'}
cleaned_content = clean_md("sample.md", contexts=replacements)
print(cleaned_content) # This will print: "This is a test: Hello, World!"
```
By passing `contexts` option with a `Dictionary`, any placeholders inside `{}` in your MD file will be replaced by the corresponding variables in your script.
If a placeholder doesn't have a corresponding variable in your script, a warning will be logged, and the placeholder will be retained in the output.

### Encoding Detection Bytes Param
The `encoding_detection_bytes` parameter will allow the user to define how many bytes it will read from the md file before
deciding on its encoding type. 
#### Example
```python
global_test = "Global Test here"


def greet():
    new_test = "Local Test here"
    context = {'new_test': new_test, 'global_test': global_test}
    print(clean_md(file_path='test.md', contexts=context, encoding_detection_bytes=500))


greet()
```
In the above example, `clean_md` will read the first 500 bytes before deciding its encoding type. This is helpful when
dealing with larger files that have a lot of bytes. The default for `encoding_detection_bytes` is `1024`.

Additionally, you can pass the `string` value of `auto` inside `encoding_detection_bytes` which will allot it to read the entire
file content before making a decision.

```python
global_test = "Global Test here"

def greet():
    new_test = "Local Test here"
    context = {'new_test': new_test, 'global_test': global_test}
    print(clean_md(file_path='test.md', contexts=context, encoding_detection_bytes='auto'))
```

### Manual Encoding
If you know the type of encoding of the file beforehand, you can specify the encoding type by using the `manual_encoding`
parameter. This will allow the script to bypass the encoding detection when reading the md file. If the `manual_encoding`
provided is **invalid**, we will catch the error and then retry with encoding detection.

We will assume in our Markdown file, the encoding type is `utf-8`, and pass it in `manual_encoding` like such:
```python
global_test = "Global Test here"

def greet():
    new_test = "Local Test here"
    context = {'new_test': new_test, 'global_test': global_test}
    print(clean_md(file_path='test.md', contexts=context, encoding_detection_bytes='auto', manual_encoding='utf-8'))
```

## Contributing
If you find any bugs or want to propose a new feature, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE.txt file for details.