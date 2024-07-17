#!/usr/bin/env python3
""" Auth module"""

import bcrypt

from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hashs the password and return the bytes form"""
    if not isinstance(password, str):
        raise ValueError("password should be a string")
    bytes = password.encode('utf-8')

    return bcrypt.hashpw(bytes, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register returns a user with email and password"""

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
