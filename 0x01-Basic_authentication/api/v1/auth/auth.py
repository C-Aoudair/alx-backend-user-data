#!/usr/bin/env python3
""" Contains Auth class"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class for authentication porpuses"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False"""
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
