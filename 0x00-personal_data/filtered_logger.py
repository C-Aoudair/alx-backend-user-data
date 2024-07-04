#!/usr/bin/env python3
""" Contains filter_datum function"""

import re


def filter_datum(fields, redaction, message, seperator):
    """
    Returns the log message obfuscated.
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
                    all fields in the log line (message)
    Return: log message obfuscated
    """
    for field in fields:
        # Create a regex pattern for the current field
        pattern = re.compile(rf"{field}=[^{seperator}]*")
        # Replace the field value with the redaction
        message = pattern.sub(f"{field}={redaction}", message)

    return message
