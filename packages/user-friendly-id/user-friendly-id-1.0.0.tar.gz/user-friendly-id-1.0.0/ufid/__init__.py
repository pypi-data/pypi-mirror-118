"""
User-friendly ID library
----------------------------

Collection of functions to randomly and securely generate commonly-used types of IDs.

:copyright: (c) 2021 by Remy Charlot
:license: BSD 3-clause. See LICENSE for more details
"""

__title__ = 'ufid'
__version__ = '1.0.0'
__author__ = 'Remy Charlot'
__license__ = 'BSD 3-clause'
__copyright__ = 'Copyright 2021'

import secrets
import re
import random
import string


def generate_random_string(length: int, allowed_chars: str = (
        string.digits + string.ascii_letters), secure: bool = False):
    if secure:
        # Same behavior as django.utils.crypto's get_random_string
        return ''.join(secrets.choice(allowed_chars) for i in range(length))
    else:
        # Using cryptographically unsecure source of randomness for better performance
        return ''.join(random.sample(allowed_chars, length))


def generate_random_lowercase_string(length: int, secure: bool = False) -> str:
    """
    Generates random string from all ascii lowercase chars and digits
    """
    allowed_chars = string.ascii_lowercase + string.digits
    return generate_random_string(
        length=length,
        allowed_chars=allowed_chars,
        secure=secure
    )


def generate_random_digit_string(length: int, secure: bool = False) -> str:
    """
    Generates random string from all digits
    """
    allowed_chars = string.digits
    return generate_random_string(
        length=length,
        allowed_chars=allowed_chars,
        secure=secure
    )


def generate_base64_random_string(length: int, secure: bool = False) -> str:
    """
    Generates Youtube-like base64 random strings
    """
    allowed_chars = string.digits + string.ascii_letters + '-_'
    return generate_random_string(
        length=length,
        allowed_chars=allowed_chars,
        secure=secure
    )


def generate_base47_random_string(length: int, secure: bool = False) -> str:
    """
    Generates Alphanumeric (lower+upper) without common confusables / homoglyphs
    """
    chars = string.digits + string.ascii_letters
    confusables_pattern = '[l1IO0S58BZ2qgnv]'
    allowed_chars = re.sub(confusables_pattern, '', chars)
    return generate_random_string(
        length=length,
        allowed_chars=allowed_chars,
        secure=secure
    )


def generate_user_friendly_id(length: int = 6) -> str:
    """
    Generates 6 chars base47 string without two consecutive
    'curse word inducing' chars (taken from hashids library)
    Around 10 billion combinations at 6 chars.
    """
    while True:
        ufid = generate_base47_random_string(length=length, secure=True)
        curse_inducing_chars = 'cfhistuCFHISTU'  # Note that I and S are already absent from this base 47
        ufid_separated = re.split('|'.join(list(curse_inducing_chars)), ufid)
        if '' not in ufid_separated:
            return ufid
