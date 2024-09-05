#!/usr/bin/env python3
"""
Contains class for implementing session based authentication
"""


from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    Implements session based authentication
    """

    user_id_by_session_id =  {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates session id for user id
        """
        if not user_id:
            return None
        if type(user_id) is not str:
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
