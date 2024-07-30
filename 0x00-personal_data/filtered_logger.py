#!/usr/bin/env python3
"""
Returns an obfuscated log message
"""
import re

def filter_datum(fields, redaction, message, separator):
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: m.group().split('=')[0] + '=' + redaction, message)

