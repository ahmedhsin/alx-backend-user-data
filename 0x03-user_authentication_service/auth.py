#!/usr/bin/env python3
from db import DB
"""Auth class file"""

from user import Base, User
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash function using bcrypt"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """func to register user"""
        session = self._db._session
        user = session.query(User).filter(User.email == email).first()
        if user:
            raise ValueError(f"User {email} already exists")
        user = User(email=email, hashed_password=_hash_password(password))
        session.add(user)
        session.commit()
        return user
