#!/usr/bin/env python3
"""Session Authentication"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}  # Attribut de classe

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user with id user_id  """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
