#!/usr/bin/env python3
""" Module of Index views
"""
import re
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """a class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require Auth"""
        if path is not None and excluded_paths is not None:
            for ex in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if ex[-1] == '*':
                    pattern = '{}.*'.format(ex[0:-1])
                elif ex[-1] == '/':
                    pattern = '{}/*'.format(ex[0:-1])
                else:
                    pattern = '{}.*'.format(ex)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization"""
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
    
    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        SESSION_NAME = os.getenv('SESSION_NAME')
        my_session_id = request.cookies.get(SESSION_NAME)
        return my_session_id
