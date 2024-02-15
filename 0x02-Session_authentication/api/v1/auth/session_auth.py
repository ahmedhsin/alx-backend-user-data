#!/usr/bin/env python3
"""session auth file for authenticate"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
from uuid import uuid4

class SessionAuth(Auth):
    """session auth class"""
    user_id_by_session_id = {}
    def create_session(self, user_id: str = None) -> str:
        """create a user session"""
        if user_id is None:
            return None
        if type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrive the user id based on sesison id"""
        if session_id is None:
            return None
        if type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """return current user"""
        cookie = self.session_cookie()
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)
    