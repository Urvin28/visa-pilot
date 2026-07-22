import json


class UserProfile:

    def __init__(self):
        self.users = {}

    def update(self, session_id, data):

        if session_id not in self.users:
            self.users[session_id] = {}

        self.users[session_id].update(data)

    def get(self, session_id):

        return self.users.get(session_id, {})