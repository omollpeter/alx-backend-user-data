#!/usr/bin/env python3
"""
Contains class that handles session expiry
"""


from api.v1.auth.session_auth import SessionAuth
import os


duration = os.getenv("SESSION_DURATION")

class SessionExpAuth(SessionAuth):
    """
    Handles session expiry
    """

    def __init__(self):
        """
        Initializes instance attributes
        """
        if duration:
            session_duration = int(duration)
        else:
            session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
