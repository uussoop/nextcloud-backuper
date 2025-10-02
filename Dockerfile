# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    p7zip-full \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./

# Create volume mount point for data to backup
VOLUME ["/data"]

# Create volume mount point for forbidden file
VOLUME ["/config"]

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BACKUP_BASE_DIR=/data
ENV FORBIDDEN_DIRS_FILE=/config/forbidden

# Run the application
CMD ["python", "main.py"]

