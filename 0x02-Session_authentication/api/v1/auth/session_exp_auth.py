#!/usr/bin/env python3
"""session auth  exp file for authenticate"""

from api.v1.auth.session_auth import SessionAuth, getenv
from flask import request, jsonify
from typing import TypeVar
from models.user import User
from uuid import uuid4
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """session auth expire class"""
    def __init__(self):
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overload create_session func in session auth"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return the user_id key from
        the session dictionary if
        self.session_duration is equal or under 0"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        key = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return key['user_id']
        if 'created_at' not in key:
            return None
        created_at = key['created_at'].timestamp()
        if created_at + self.session_duration < datetime.now().timestamp():
            return None
        return key['user_id']
