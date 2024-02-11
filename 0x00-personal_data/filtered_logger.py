#!/usr/bin/env python3
"""filter logger alxxxx"""
from typing import List
import re


def filter_datum(f: list[str], r: str, m: str, s: str) -> str:
    """filter_datum that returns the log m obfuscated"""
    for f_ in f:
        m = re.sub(r'{}=(.*?){}'.format(f_, s), f'{f_}={r}{s}', m)
    return m
