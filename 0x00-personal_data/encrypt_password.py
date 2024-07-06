#!/usr/bin/env python3
""" Contains hash_password and is_valid fucntions"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes and return hashed password"""

    bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(bytes, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate a password and return True if it is valid"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
