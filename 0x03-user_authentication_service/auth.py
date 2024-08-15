#!/usr/bin/env python3
"""
hash_password function
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
from typing import (
    TypeVar,
    Union
)

U = TypeVar(User)


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt and return the salted hash in bytes"""
    password_bytes = password.encode('utf-8')

    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user in the database"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")
