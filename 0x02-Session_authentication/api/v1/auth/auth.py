#!/usr/bin/env python3
""" Contains Auth class"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Auth class for authentication porpuses"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a certain path.
       """
        if not path or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if (excluded_path.endswith('*')
                    and path.startswith(excluded_path[:-1])):
                return False

        normalized_path = path if path.endswith('/') else f"{path}/"
        return normalized_path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Returns the value of the Authorization header from the request.
        """
        if not request:
            return None

        return request.headers.get("Authorization")

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request
            Args:
                request: request object
            Returns:
                Cookie value: string
        """
        if request is None:
            return None

        return request.cookies.get(getenv("SESSION_NAME"))

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user.
        This method must be overridden in a child class.
        """
        return None
