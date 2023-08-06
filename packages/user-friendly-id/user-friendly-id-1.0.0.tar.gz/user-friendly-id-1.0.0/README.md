# User-friendly ID

Collection of functions to randomly and securely generate commonly-used types of IDs.

## Installation
Install from PyPI:

`pip install user-friendly-id`

## Features
- Generate any length of random string, either cryptographically secure (slower) or not (faster)
- Generate IDs without without common confusables / homoglyphs (e.g lowercase "l" vs uppercase "i")
- Lowers chances of a curse word randomly appearing in IDs using same logic as Hashids library.

## How to use?

```
from ufid import (
    generate_random_string,
    generate_random_lowercase_string,
    generate_random_digit_string,
    generate_base64_random_string,
    generate_base47_random_string,
    generate_user_friendly_id,
)

# Generate securely a random string of 10 characters of
# any lowercase/uppercase alphabet + digits
generate_random_string(length=10, secure=True)


# Generate a random string of 10 characters within a set of predefined chars
generate_random_string(length=10, allowed_chars='01')


# Shortcut of the above to only allow lowercase alphabet
generate_random_lowercase_string(length=10)


# Again, shortcut to get only digits
generate_random_digit_string(length=10)


# Generate youtube-like base64 random string
generate_base64_random_string(length=10)


# Generate a random string without common confusables / homoglyphs.
# To maximize number of combination allowed_chars is not settable.
# This gives a base47 string hence the name of the function

generate_base47_random_string(length=10)


# Generate a 'true' user-friendly ID. Opiniated to a secure settings, and default of
# 6 chars for about 10 billion combinations. Also excludes without confusables / homoglyphs
# but also adds an algorithm inspired by the popular Hashids library to lower chances of
# generating curse words

generate_user_friendly_id()
generate_user_friendly_id(length=10)
```

## Tests
TODO
