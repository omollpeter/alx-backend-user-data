#!/usr/bin/env python3
"""
Contains a class that implements Basic Authentication
"""


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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
            decoded_str = decoded_data.decode("utf-8")
        except Exception:
            return None
        return decoded_str

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Returns user email and password from base64 decoded value
        """
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email_pass = decoded_base64_authorization_header.split(":")
        email = email_pass.pop(0)

        password = ":".join(email_pass)
        return email, password

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password
        """
        if not (user_email or isinstance(user_email, str)):
            return None

        if not (user_pwd or isinstance(user_pwd, str)):
            return None

        user_list = User.search({'email': user_email})
        if not user_list:
            return None

        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user from the authorization header
        """
        if not request:
            return None
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        encoded = self.extract_base64_authorization_header(auth_header)
        if not encoded:
            return None
        decoded = self.decode_base64_authorization_header(encoded)
        if not decoded:
            return None
        user_cred = self.extract_user_credentials(decoded)
        if not user_cred:
            return None
        user_object = self.user_object_from_credentials(
            user_cred[0], user_cred[1]
        )
        return user_object
