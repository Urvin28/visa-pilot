from app.retrieval.retriever import Retriever
from app.llm.client import LLMClient
from app.llm.prompts import PromptBuilder
from app.llm.extractor import UserInfoExtractor
from app.memory.session_manager import SessionManager


class RAGService:

    def __init__(self):

        self.session_manager = SessionManager()
        self.info_extractor = UserInfoExtractor()

        self.retriever = Retriever()
        self.llm = LLMClient()

    def ask(self, session_id, question):

        # -------------------------
        # Load/Create Session
        # -------------------------
        session = self.session_manager.get(session_id)

        # -------------------------
        # Extract user information
        # -------------------------
        user_info = self.info_extractor.extract(question)

        if user_info:
            session.profile.update(user_info)

        # -------------------------
        # Retrieve documents
        # -------------------------
        chunks = self.retriever.search(question)

        context = "\n\n".join(chunks)

        # -------------------------
        # Build prompt
        # -------------------------
        prompt = PromptBuilder.build(
            context=context,
            question=question,
            profile=session.profile,
            history=session.history
        )

        # -------------------------
        # Generate answer
        # -------------------------
        answer = self.llm.generate(
            system_prompt="You are an expert U.S. immigration assistant.",
            user_prompt=prompt
        )

        # -------------------------
        # Save conversation
        # -------------------------
        session.history.append({
            "role": "user",
            "content": question
        })

        session.history.append({
            "role": "assistant",
            "content": answer
        })

        # Keep only last 10 messages
        session.history = session.history[-10:]

        return answer


if __name__ == "__main__":

    rag = RAGService()

    print(
        rag.ask(
            "user123",
            "I am an F-1 student at Stevens Institute of Technology graduating in May 2027."
        )
    )

    print("-" * 80)

    print(
        rag.ask(
            "user123",
            "When should I apply for OPT?"
        )
    )