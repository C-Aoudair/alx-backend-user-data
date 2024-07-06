#!/usr/bin/env python3
""" Contains hash_password fucntion"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes and return hashed password"""

    bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(bytes, salt)
