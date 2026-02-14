# Activity 6.1-6.4: Deployment - Docker Configuration
# Citizen AI Platform Docker Image

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY app.py .
COPY .env.example .env

# Activity 1.3: Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Activity 6.3: Run application
CMD ["python", "app.py"]
