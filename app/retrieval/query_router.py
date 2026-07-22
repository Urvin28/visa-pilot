class QueryRouter:

    SMALL_TALK = {
        "ok",
        "okay",
        "thanks",
        "thank you",
        "gotcha",
        "cool",
        "great",
        "nice",
        "awesome",
        "yep",
        "yes",
        "no",
        "understood",
        "sounds good"
    }

    def route(self, question: str):

        q = question.lower().strip()

        if q in self.SMALL_TALK:
            return "small_talk"

        return "rag"