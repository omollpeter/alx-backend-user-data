#!/usr/bin/env python3
"""
Contains a function that hashes passwords
"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    Returns salted hash of the input password
    """
    pwd_bytes = password.encode("utf-8")

    hashed_pwd = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid():
    """
    Generates and return a new UUID
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a given password for successful login
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Finds user, creates and return a session_id for the user
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db._session.commit()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Returns a user corresponding to a session id
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Updates a corresponding user's session id to None
        """
        self._db.update_user(user_id, session_id=None)
        return None
