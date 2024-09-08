#!/usr/bin/env python3
"""
Contains class that handles session expiry
"""


from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


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
            self.session_duration = int(duration)
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session
        """
        if not user_id:
            return None
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        super().user_id_by_session_id["session_id"] = {
            "user_id": user_id,
            "created_at": datetime.now() 
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user id fro the current session
        """
        if not session_id:
            return None

        session_dict = self.user_id_by_session_id.get("session_id")
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")
        created_at = session_dict.get("created_at")
        if not created_at:
            return None

        total_duration_req = created_at + timedelta(
            minutes=self.session_duration
        )

        if (datetime.now() - total_duration_req) < timedelta(0):
            return None
        return session_dict.get("user_id")
