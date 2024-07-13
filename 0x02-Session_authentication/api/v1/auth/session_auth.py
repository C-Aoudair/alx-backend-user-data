#!/usr/bin/env python3
""" Contains the SessionAuth class that inherits from Auth"""

from api.v1.auth.auth import Auth
from os import getenv
import uuid


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
            Args:
                user_id: string
            Returns:
                Session ID: string
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
            Args:
                session_id: string
            Returns:
                User ID: string
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

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
