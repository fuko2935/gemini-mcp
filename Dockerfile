FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY gemini_mcp_server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY gemini_mcp_server/ ./gemini_mcp_server/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "gemini_mcp_server.mcp_server:app", "--host", "0.0.0.0", "--port", "8000"]
