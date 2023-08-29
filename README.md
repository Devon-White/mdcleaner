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

### Using the Formatted Option
Imagine you have an MD file named `sample.md` with the following content:
```markdown
This is a test: {my_variable}
```
In your script, you can replace the `{my_variable}` placeholder with the value of a variable defined in your script:

```python
from mdcleaner import clean_md

my_variable = "Hello, World!"

# Read and format the content of "sample.md"
cleaned_content = clean_md("sample.md", formatted=True)
print(cleaned_content) # This will print: "This is a test: Hello, World!"
```
By setting the `formatted` option to `True`, any placeholders inside `{}` in your MD file will be replaced by the corresponding variables in your script.
If a placeholder doesn't have a corresponding variable in your script, a warning will be logged, and the placeholder will be retained in the output.

## Contributing
If you find any bugs or want to propose a new feature, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE.txt file for details.