#!/usr/bin/env python3
""" Contains SessionExpAuth class"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime
from os import getenv


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class
    """
    def __init__(self):
        """ Constructor
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
            Args:
                user_id: string
            Returns:
                Session ID: string
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
            Args:
                session_id: string
            Returns:
                User ID: string or None
        """
        if session_id is None:
            return None

        session_dict = super().user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        if "created_at" not in session_dict:
            return None

        created_at = session_dict.get("created_at")
        if (datetime.now() - created_at).seconds > self.session_duration:
            return None

        return session_dict.get("user_id")
