FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 \
    libxkbcommon0 libxcomposite1 libxrandr2 libxdamage1 libxfixes3 \
    libasound2 libdrm2 libxext6 libxshmfence1 libgbm1 \
    wget curl git ca-certificates fonts-liberation && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install --with-deps chromium

COPY . .
ENV PORT=8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
