#!/usr/bin/env python3
"""
Contains a function that hashes passwords
"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Returns salted hash of the input password
    """
    pwd_bytes = password.encode("utf-8")

    hashed_pwd = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed_pwd


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """
        Initializes instance attributes
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Saves and returns a new user to the database if not exists
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")

        except NoResultFound:
            return self._db.add_user(
                email=email,
                hashed_password=_hash_password(password)
            )
