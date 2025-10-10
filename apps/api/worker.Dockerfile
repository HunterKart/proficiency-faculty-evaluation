FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libffi-dev \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libgdk-pixbuf-2.0-0 \
      libcairo2 \
      libjpeg-dev \
      zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
      transformers==4.44.2 \
      torch==2.8.0 \
      keybert==0.8.4 \
      google-generativeai==0.6.0 \
      scikit-learn==1.5.2

COPY src ./src

CMD ["rq", "worker", "default"]
