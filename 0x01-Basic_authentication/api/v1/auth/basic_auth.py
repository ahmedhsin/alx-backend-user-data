#!/usr/bin/env python3
"""basic auth file for authenticate"""

from api.v1.auth.auth import Auth
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
        return s[0], s[1]
