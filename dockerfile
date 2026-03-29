FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8001

RUN mkdir -p temp_uploads


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
