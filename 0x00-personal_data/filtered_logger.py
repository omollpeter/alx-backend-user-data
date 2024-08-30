#!/usr/bin/env python3
"""
This module contains filter_datum function
"""


from typing import List
import re
import logging
import os
import mysql.connector
from mysql.connector import connection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
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


def get_db() -> connection.MySQLConnection:
    """Returns a MySQLConnection object to the database."""
    # Retrieve database credentials from environment variables
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Establish a connection to the database
    db_connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    
    return db_connection

def main():
    """Main function that logs information about users."""
    db_connection = get_db()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        message = "; ".join([f"{key}={value}" for key, value in row.items()])
        message += ";"
        logger.info(message)

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
