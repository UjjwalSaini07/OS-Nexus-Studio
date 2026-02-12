FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY client/ ./client/

COPY server/ ./server/

RUN g++ -std=c++11 -o /app/server/main_system /app/server/main_system.cpp -lws2_32

RUN pip install --no-cache-dir tk

EXPOSE 9090 8080

CMD ["python", "/app/client/mainClient.py"]
