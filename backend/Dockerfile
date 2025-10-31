FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Use PORT environment variable for Railway
ENV PORT=8000

# Default command (Railway will override with PORT env var)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

