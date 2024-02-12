#!/usr/bin/env python3
"""This class is the template for all authentication system you will implement.

"""
from flask import request
from typing import List, TypeVar


class Auth():
    """class for auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """func to check if auth or not"""
        if path is not None:
            if path[-1] != '/':
                path += '/'
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path is None or path not in excluded_paths:
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
