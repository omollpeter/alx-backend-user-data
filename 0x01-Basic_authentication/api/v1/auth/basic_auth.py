#!/usr/bin/env python3
"""
Contains a class that implements Basic Authentication
"""


from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes a base64 encoded authorization header value
        """
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_data = base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        return decoded_data.decode("utf-8")

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> tuple[str, str]:
        """
        Returns user email and password from base64 decoded value
        """
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(":")
        return email, password
