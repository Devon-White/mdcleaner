from mdcleaner import clean_md

global_test = "Global Test here"


def greet():
    new_test = "Local Test here"
    print(clean_md('test.md', formatted=True))


greet()
