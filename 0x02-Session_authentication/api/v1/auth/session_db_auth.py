#!/usr/bin/env python3
""" contains the SessionDBAuth class """

from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timezone
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """
    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id and saves it to the database
            Args:
                user_id: string
            Returns:
                Session ID: string or None
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID from UserSession based on a Session ID
            Args:
                session_id: string
            Returns:
                User ID: string or None
        """
        if session_id is None:
            return None

        try:
            user_session = UserSession.search({'session_id': session_id})[0]
        except Exception:
            return None

        if self.session_duration <= 0:
            return user_session.user_id

        if user_session.created_at is None:
            return None

        duration = datetime.now(timezone.utc) - user_session.created_at
        if duration.seconds > self.session_duration:
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """ Deletes the UserSession based on the Session ID
            Args:
                request: request object
            Returns:
                True if session was deleted, False otherwise
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        try:
            user_session = UserSession.search({'session_id': session_id})[0]
        except Exception:
            return False

        user_session.remove()
        return True
