#!/usr/bin/env python3
""" Contains filter_datum function"""

import mysql.connector
import logging
import re
import os

from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def main() -> None:
    """ obtain a database connection using get_db
        and retrieve all rows in the users table
        and display each row under a filtered format
    """
    db_connector = get_db()
    cursor = db_connector.cursor()
    cursor.execute('SELECT * FROM users;')

    logger = get_logger()

    headers = [field[0] for field in cursor.description]

    for row in cursor:
        message = ""
        for item in zip(headers, row):
            message += f"{item[0]}={item[1]}; "
        logger.info(message)

    cursor.close()
    db_connector.close()


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database"""
    db_connect = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect


def get_logger() -> logging.Logger:
    """ Returns a loggin.Logger object with user_data as a name"""
    logger = logging.Logger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.addHandler(handler)

    return logger


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """Returns the log message obfuscated."""
    for field in fields:
        message = re.sub(
                rf"\b{field}=[^{separator}]*\b",
                f"{field}={redaction}",
                message
            )
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constucture"""
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Override the format method fo the parent class"""
        log_message = super().format(record)
        obfuscated_message = filter_datum(
            self.fields, self.REDACTION, log_message, self.SEPARATOR
        )
        return obfuscated_message


if __name__ == '__main__':
    main()
