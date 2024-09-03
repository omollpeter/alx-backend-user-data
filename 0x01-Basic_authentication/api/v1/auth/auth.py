#!/usr/bin/env python3
"""
This module contains Auth class
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manages API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False (modified later)
        """
        if not path:
            return True
        if not excluded_paths:
            return True
        if not path.endswith("/"):
            path += "/"

        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns none (modified later)
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None
        """
        return None
