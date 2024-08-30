#!/usr/bin/env python3
"""
This module contains filter_datum function
"""


from typing import List
import re
import logging

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes instance attributes"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters value in the incoming log records"""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


# def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
#     """Returns log message obfuscated"""
#     for field in fields:
#         message = re.sub(rf"{re.escape(field)}=.*?{re.escape(separator)}", f"{re.escape(field)}={redaction}{re.escape(separator)}", message)
#     return message

def filter_datum(fields, redaction, message, separator):
    """Returns obfuscated message"""
    pattern = r'({})=[^{}]*'.format('|'.join(re.escape(field) for field in fields), re.escape(separator))
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}", message)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
