#!/usr/bin/env python3
""" Contains filter_datum function"""

import re


def filter_datum(fields, redaction, message, seperator):
    """Returns the log message obfuscated."""
    for field in fields:
        message = re.sub(rf"{field}=[^{seperator}]*", f"{field}={redaction}", message)
    return message
