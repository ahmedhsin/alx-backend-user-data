#!/usr/bin/env python3
"""basic auth file for authenticate"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """basic auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> str:
        """extract_base64_authorization_header"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split('Basic ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """decode_base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        decoded = None
        try:
            decoded = base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None
        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """extract_user_credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        s = decoded_base64_authorization_header.split(':')
        email = s[0]
        password = ':'.join(s[1:])
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """user_object_from_credentials"""
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) != str or type(user_pwd) != str:
            return None
        user = User.search({'email': user_email})
        user = user[0] if len(user) > 0 else None
        if user is None:
            return None
        if not User.is_valid_password(user, user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """complete the puzzle get current_user"""
        auth_header = self.authorization_header(request)
        extract_auth_token = self.extract_base64_authorization_header(
            auth_header)
        decode_auth_token = self.decode_base64_authorization_header(
            extract_auth_token)
        user_credit = self.extract_user_credentials(
            decode_auth_token)
        get_user = self.user_object_from_credentials(
            user_credit[0], user_credit[1])
        return get_user
