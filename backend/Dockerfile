# Use official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    UPLOAD_DIR=/app/uploads

# Install system dependencies
# gcc and g++ are required to compile tree-sitter parsers
# git is required for cloning git repositories (/api/analyze-git)
# curl is used for container healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up user for Hugging Face Spaces compatibility (uid 1000)
RUN useradd -m -u 1000 user

WORKDIR /app

# Copy dependency definition and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

# Ensure uploads directory exists and configure permissions
RUN mkdir -p /app/uploads && \
    chown -R user:user /app && \
    chmod -R 777 /app/uploads

# Expose backend API port (8000 default, dynamically overridable by $PORT e.g. on Render)
EXPOSE 8000

USER user

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/api/health || exit 1

# Start FastAPI with Uvicorn
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}"]
