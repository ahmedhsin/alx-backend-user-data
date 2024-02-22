#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")  # noqa: E251
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def find_user_by(self, **kwargs) -> User:
        """Finds user by valid argument """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user

        except InvalidRequestError as e:
            raise e

    def add_user(self, email: str, hashed_password: str) -> User:
        """create user method"""
        session = self._session
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        return new_user

    def update_user(self, user_id: str, **kwargs:  Dict[str, str]) -> None:
        """update the user based on user_id"""
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            user.key = val
        self._session.commit()
