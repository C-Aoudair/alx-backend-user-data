#!/usr/bin/env python3
""" Contains Auth class"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class for authentication porpuses"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required.
        For now, this method returns False.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the value of the Authorization header from the request.
        For now, this method returns None.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user.
        For now, this method returns None.
        """
        return None
