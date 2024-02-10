#!/usr/bin/env python3
"""filter logger"""
import re


def filter_datum(fields: list[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """filter_datum that returns the log message obfuscated"""
    for field in fields:
        field_regex = r'{}=(.*?){}'.format(field, separator)
        message = re.sub(field_regex, f'{field}={redaction}{separator}',
                         message)
    return message
