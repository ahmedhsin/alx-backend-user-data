#!/usr/bin/env python3
"""filter logger alxxxx"""
import re


def filter_datum(f: list[str], r: str, m: str, s: str) -> str:
    """filter_datum that returns the log m obfuscated"""
    for f_ in f:
        f__regex = r'{}=(.*?){}'.format(f_, s)
        m = re.sub(f__regex, f'{f_}={r}{s}', m)
    return m
