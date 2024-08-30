#!/usr/bin/env python3
"""
Contains hash_password function that encrypts a password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password with a salt using bcrypt."""
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
