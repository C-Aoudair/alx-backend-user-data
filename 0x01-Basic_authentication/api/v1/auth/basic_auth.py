#!/usr/bin/env python3
""" Contains BasicAuth class"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """
        Extracts the Base64 part of the Authorization header.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the header if valid, otherwise None.
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """
        Decodes a Base64 authorization header.

        Args:
            base64_authorization_header (str): The Base64 encoded header.

        Returns:
            str: The decoded UTF-8 string if valid, otherwise None.
        """
        if (
            base64_authorization_header is None or
            not isinstance(base64_authorization_header, str)
        ):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Extracts user email and password from decoded Base64
        authorization header.

        Args:
            decoded_base64_authorization_header (str):
            Decoded Base64 string.

        Returns:
            (str, str): User email and password if valid,
            otherwise (None, None).
        """
        if (decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str)):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)
