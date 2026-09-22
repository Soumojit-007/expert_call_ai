FROM python:3.12-slim

# Prevent Python from creating .pyc files
# and ensure logs appear immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY app ./app

# Create directory for ChromaDB persistence
RUN mkdir -p /app/vectorstore

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]