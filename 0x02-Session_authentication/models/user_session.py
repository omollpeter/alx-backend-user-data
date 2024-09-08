#!/usr/bin/env python3
"""
Contains a class that assists in storing session IDs
"""


from models.base import Base


class userSession(Base):
    """
    Persistent user sessions
    """
    def __init__(self, *args: list, **kwargs: dict):
        """Initializes attributes for user session instances"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
