#!/usr/bin/env python3
"""Basic Auth"""
import re
import base64
import binascii
from typing import TypeVar, Tuple

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """a class BasicAuth that inherits from Auth"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Returns base64"""
        if isinstance(authorization_header, str):
            pattern = r'Basic (?P<token>.+)'
            match = re.fullmatch(pattern, authorization_header.strip())
            if match is not None:
                return match.group('token')
            return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Returns Base64 decode"""
        if isinstance(base64_authorization_header, str):
            try:
                decoded = base64.b64decode(
                    base64_authorization_header,
                    validate=True
                )
                return decoded.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """returns the user email and password from the Base64 decoded value"""
        if isinstance(decoded_base64_authorization_header, str):
            pattern = r'(?P<user>[^:]+):(?P<password>[^:]+)'
            match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip()
            )
            if match is not None:
                user = match.group('user')
                password = match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request:"""
        auth_header = self.authorization_header(request)
        encoded_token = self.extract_base64_authorization_header(auth_header)
        decoded_token = self.decode_base64_authorization_header(encoded_token)
        email, password = self.extract_user_credentials(decoded_token)
        return self.user_object_from_credentials(email, password)
