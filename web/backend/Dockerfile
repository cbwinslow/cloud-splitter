FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        ffmpeg \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# First install core dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi==0.95.2 \
    uvicorn[standard]==0.21.1 \
    python-multipart==0.0.6 \
    pydantic==1.10.7 \
    SQLAlchemy==1.4.50 \
    psycopg2-binary==2.9.9 \
    alembic==1.11.3 \
    databases[postgresql]==0.8.0

# Then install audio processing dependencies
RUN pip install --no-cache-dir numpy==1.23.5 \
    scipy==1.10.1 \
    librosa==0.9.2 \
    soundfile==0.12.1 \
    audioread==3.0.1

# Finally install remaining dependencies
RUN pip install --no-cache-dir python-magic==0.4.27 \
    aiofiles==23.2.1 \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    python-dotenv==1.0.0 \
    bcrypt==4.0.1 \
    websockets==11.0.3 \
    python-socketio==5.8.0 \
    requests==2.31.0 \
    pydub==0.25.1

# Create a non-root user
RUN useradd -m -u 1000 appuser

FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Install runtime system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create upload directory
RUN mkdir -p uploads

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy project files
COPY . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
