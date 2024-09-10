#!/usr/bin/env python3
"""
DB Module
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Saves user to a database and returns the user
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Returns the first user based on given arguments
        """
        attributes = [
            "email", "id", "hashed_password", "session_d", "reset_token"
        ]
        for key in kwargs.keys():
            if key not in attributes:
                raise InvalidRequestError()
            if key == "email":
                user = self._session.query(User).filter(
                    User.email == kwargs["email"]
                ).first()
            elif key == "id":
                user = self._session.query(User).filter(
                    User.id == kwargs["id"]
                ).first()
            elif key == "hashed_password":
                user = self._session.query(User).filter(
                    User.hashed_password == kwargs["hashed_password"]
                ).first()
            elif key == "session_id":
                user = self._session.query(User).filter(
                    User.session_id == kwargs["session_id"]
                ).first()
            elif key == "reset_token":
                user = self._session.query(User).filter(
                    User.reset_token == kwargs["reset_token"]
                ).first()
            if user:
                return user
        raise NoResultFound()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user in the database
        """
        user = self.find_user_by(id=user_id)
        if not user:
            return None

        attributes = ["email", "hashed_password", "session_d", "reset_token"]
        for key, value in kwargs.items():
            if key not in attributes:
                raise ValueError()
            if key == "email":
                user.email = value
            elif key == "hashed_password":
                user.hashed_password = value
            elif key == "session_id":
                user.session_id = value
            elif key == "reset_token":
                user.reset_token = value
        self._session.commit()
