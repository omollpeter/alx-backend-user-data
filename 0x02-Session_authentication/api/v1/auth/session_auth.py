#!/usr/bin/env python3
"""
Contains class for implementing session based authentication
"""


from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    Implements session based authentication
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates session id for user id
        """
        if not user_id:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user id based on a session id
        """
        if not session_id:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a user instance based on cookie value
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None
        return User.get(user_id)
