#!/usr/bin/env python3
"""
Contains a class that implements Basic Authentication
"""


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Implements Basic Authentication
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Returns the Base64 part of the authorization header for
        basic authentication
        """
        if not authorization_header:
            return
        if type(authorization_header) is not str:
            return None
        auth_header = authorization_header.split(" ")
        if auth_header[0] != "Basic":
            return None
        return auth_header[-1]
