#!/usr/bin/env python3
""" Contains filter_datum function"""

import logging
import re

from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """Returns the log message obfuscated."""
    for field in fields:
        message = re.sub(
                rf"{field}=[^{seperator}]*",
                f"{field}={redaction}",
                message
            )
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        obfuscated_message = filter_datum(
            self.fields, self.REDACTION, log_message, self.SEPARATOR
        )
        return obfuscated_message
