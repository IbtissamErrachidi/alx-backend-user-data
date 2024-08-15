import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt and return the salted hash in bytes"""
    password_bytes = password.encode('utf-8')

    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password
