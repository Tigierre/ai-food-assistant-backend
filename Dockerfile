FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Set default environment variables
ENV HOST=0.0.0.0
ENV LANGGRAPH_HOST=0.0.0.0
ENV LANGGRAPH_PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8080}/ || exit 1

# Start command with explicit port configuration
CMD ["sh", "-c", "python main.py --host ${HOST:-0.0.0.0} --port ${PORT:-8080}"]
