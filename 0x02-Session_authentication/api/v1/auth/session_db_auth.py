#!/usr/bin/env python3
"""
Implements authentication system that persistently stores sessions
"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import userSession


class SessionDBAuth(SessionExpAuth):
    """
    New authentication system
    """

    def create_session(self, user_id=None):
        """
        Creates and stores new instance of user session and returns
        session ID
        """
        if not user_id:
            return None
        return super().create_session(user_id)()
        
    def destroy_session(self, request=None):
        return super().destroy_session(request)()
