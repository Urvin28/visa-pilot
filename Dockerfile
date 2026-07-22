FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl zstd

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD sh -c "\
ollama serve & \
sleep 5 && \
ollama list | grep llama3.2:3b || ollama pull llama3.2:3b && \
python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000"