from mdcleaner import clean_md

global_test = "Global Test here"


def greet():
    new_test = "Local Test here"
    context = {'new_test': new_test, 'global_test': global_test}
    print(clean_md(file_path='test.md', contexts=context, encoding_detection_bytes=500, manual_encoding='utf-888'))


greet()