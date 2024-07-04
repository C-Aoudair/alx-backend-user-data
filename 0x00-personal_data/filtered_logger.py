#!/usr/bin/env python3
""" Contains filter_datum function"""

import re

from typing import List


def filter_datum(fields: List[str], redaction: str,
                message: str, seperator: str):
    """Returns the log message obfuscated."""
    for field in fields:
        message = re.sub(rf"{field}=[^{seperator}]*",
                        f"{field}={redaction}", message)
    return message
