#!/usr/bin/env python3
"""
This module contains Auth class
"""


from flask import request
from typing import List, TypeVar
import os


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

        for p in excluded_paths:
            if p.endswith("*"):
                if path.startswith(p[:-1]):
                    return False
            if p == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns value of the header request Authorization, None
        otherwise
        """
        if not request:
            return None

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns cookie value from request
        """
        if not request:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        return request.cookies.get(cookie_name)
