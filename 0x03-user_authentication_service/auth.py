#!/usr/bin/env python3
"""define a _hash_password method that takes in a password
string arguments and returns bytes"""

import bcrypt
from db import DB


def _hash_password(password: str) -> str:
    """Hashing and salting input password"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
