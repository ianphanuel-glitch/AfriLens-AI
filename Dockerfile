# Multi-stage build for AfriLens AI
FROM python:3.11-slim as backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY afrilens.db* ./

# Expose port
EXPOSE 8000

# Initialize database
RUN python -m backend.database || true

# Run backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
