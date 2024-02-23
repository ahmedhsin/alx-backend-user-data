#!/usr/bin/env python3
"""Auth class file"""

from db import DB, NoResultFound
from user import Base, User
import bcrypt
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """hash function using bcrypt"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """generate a uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """func to register user"""
        user = None
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """check if the credits is valid"""
        try:
            user = self._db.find_user_by(email=email)
            hash_password = user.hashed_password
            return bcrypt.checkpw(password.encode('utf8'), hash_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """create a session id and attatch to the user """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """get user form session"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy_session remove session from db"""
        if user_id is None:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """get_reset_password_token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset)
        return reset

    def update_password(self, reset_token: str, password: str) -> None:
        """update_password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except Exception:
            raise ValueError
