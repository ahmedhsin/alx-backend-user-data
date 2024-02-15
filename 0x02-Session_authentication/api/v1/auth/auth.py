#!/usr/bin/env python3
"""This class is the template for all authentication system you will implement.

"""
from flask import request
from typing import List, TypeVar
import re
from os import getenv


class Auth():
    """class for auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """func to check if auth or not"""
        if path is not None:
            if path[-1] != '/':
                path += '/'
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path is None:
            return True
        found = False
        for p in excluded_paths:
            if re.search(p, path):
                found = True
                break
        if not found:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """auth header get the token"""
        if request is None:
            return None
        auth = request.headers.get('Authorization')
        if auth is None:
            return None
        return auth

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user if exists"""
        return None

    def session_cookie(self, request=None):
        """return the cookie extackted from request"""
        if request is None:
            return None
        _my_session_id = getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)