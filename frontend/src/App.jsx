import { useState, useEffect, useRef } from "react";
import axios from "axios";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
    }, [messages]);   

  const askQuestion = async () => {
    if (loading || !question.trim()) return;

    const currentQuestion = question;

    setQuestion("");

    setLoading(true);

    const userMessage = {
      role: "user",
      content: currentQuestion,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
      {
        role: "assistant",
        content: "Thinking...",
      },
    ]);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          session_id: "user123",
          question: currentQuestion,
        }
      );

      const assistantMessage = {
        role: "assistant",
        content: response.data.answer,
      };

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = assistantMessage;
        return updated;
      });
    } catch (error) {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "assistant",
          content: "Something went wrong.",
        };
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
  <div className="h-screen bg-slate-900 text-white flex">

    {/* Sidebar */}
    <div className="w-72 bg-slate-950 border-r border-slate-800 p-6">

      <h1 className="text-2xl font-bold">
        🇺🇸 VisaPilot
      </h1>

      <p className="text-slate-400 mt-2 text-sm">
        AI Immigration Assistant
      </p>

      <div className="mt-10 space-y-4">

        <div className="bg-slate-800 rounded-xl p-4">
          Ask questions about
          <br />
          • OPT
          <br />
          • STEM OPT
          <br />
          • H-1B
          <br />
          • CPT
          <br />
          • USCIS
        </div>

      </div>

    </div>

    {/* Chat */}

    <div className="flex-1 flex flex-col">

      <div className="flex-1 overflow-y-auto p-10">

        {messages.map((message, index) => (

          <div
            key={index}
            className={`flex mb-6 ${
              message.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >

            <div
              className={`max-w-3xl px-5 py-4 rounded-2xl ${
                message.role === "user"
                  ? "bg-blue-600"
                  : "bg-slate-800"
              }`}
            >
              {message.content}
            </div>

          </div>

        ))}

        <div ref={chatEndRef}></div>

      </div>

      <div className="border-t border-slate-800 p-6">

        <div className="flex gap-4">

          <input
            className="flex-1 rounded-xl bg-slate-800 px-5 py-4 outline-none"
            placeholder="Ask anything about U.S. immigration..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                askQuestion();
              }
            }}
          />

          <button
            disabled={loading}
            onClick={askQuestion}
            className="bg-blue-600 hover:bg-blue-700 px-8 rounded-xl disabled:bg-slate-700"
          >
            {loading ? "Thinking..." : "Send"}
          </button>

        </div>

      </div>

    </div>

  </div>
  );
}

export default App;