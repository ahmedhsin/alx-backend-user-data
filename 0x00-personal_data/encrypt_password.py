#!/usr/bin/env python3
"""password encrypt"""

import bcrypt


def hash_password(password: str) -> bytes:
    """return hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str):
    """check if function is valid or not"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
