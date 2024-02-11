#!/usr/bin/env python3
"""filter logger """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str,
                 separator: str) -> str:
    """filter_datum that returns the log message obfuscated"""
    for field in fields:
        message = re.sub(r'{}=(.*?){}'.format(field, separator),
                         f'{field}={redaction}{separator}',
                         message)
    return message
