from app.models.session import Session


class SessionManager:

    def __init__(self):
        self.sessions = {}

    def get(self, session_id):

        if session_id not in self.sessions:
            self.sessions[session_id] = Session()

        return self.sessions[session_id]