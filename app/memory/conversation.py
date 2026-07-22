class ConversationMemory:

    def __init__(self):
        self.sessions = {}

    def add(self, session_id, role, content):

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({
            "role": role,
            "content": content
        })

        # Keep only last 10 messages
        self.sessions[session_id] = self.sessions[session_id][-10:]

    def get(self, session_id):

        return self.sessions.get(session_id, [])

    def clear(self, session_id):

        if session_id in self.sessions:
            del self.sessions[session_id]