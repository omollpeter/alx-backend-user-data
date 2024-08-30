#!/usr/bin/env python3
"""
This module contains filter_datum function
"""


from typing import List
import re


# def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
#     """Returns log message obfuscated"""
#     for field in fields:
#         message = re.sub(rf"{re.escape(field)}=.*?{re.escape(separator)}", f"{re.escape(field)}={redaction}{re.escape(separator)}", message)
#     return message

def filter_datum(fields, redaction, message, separator):
    """Returns obfuscated message"""
    pattern = r'({})=[^{}]*'.format('|'.join(re.escape(field) for field in fields), re.escape(separator))
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}", message)
