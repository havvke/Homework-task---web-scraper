FROM python:3.11-slim

COPY requirements.txt /app/
COPY src /app/src/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "src.orchestrator"]
