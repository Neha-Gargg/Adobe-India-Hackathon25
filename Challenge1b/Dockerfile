FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential libmupdf-dev libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "extract_headings.py"]
