#!/usr/bin/env python3
""" Module of Session Expiring Authentication
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth

class SessionExpAuth(SessionAuth):
    """ Session Expiring Authentication class
    """

    def __init__(self):
        """ Initialize the SessionExpAuth class
        """
        super().__init__()
        self.session_duration = 0
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a Session ID and store its creation time
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get the user ID associated with a session ID
        """
        if session_id is None:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if session is None:
            return None
        if self.session_duration <= 0:
            return session.get('user_id')
        created_at = session.get('created_at')
        if created_at is None:
            return None
        if datetime.now() > created_at + timedelta(seconds=self.session_duration):
            return None
        return session.get('user_id')
