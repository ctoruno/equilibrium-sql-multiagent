# Multi-stage build for optimization
FROM python:3.13-slim AS builder
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install --system --no-cache -r pyproject.toml

# Production stage
FROM python:3.13-slim
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set working directory
WORKDIR /app

# Copy application code
COPY esma/ ./esma/

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Cloud Run uses PORT environment variable
ENV PORT=8080
EXPOSE 8080

# Run with uvicorn optimized for Cloud Run
CMD exec uvicorn esma.api.app:app --host 0.0.0.0 --port ${PORT} --workers 1