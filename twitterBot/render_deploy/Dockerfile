FROM python:3.9-slim

# Install fortune and required system packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    fortune-mod \
    fortunes \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Create log directory with proper permissions
RUN mkdir -p /app/logs && \
    chmod 777 /app/logs

# Verify fortune installation
RUN /usr/games/fortune -v

# Expose port
EXPOSE 10000

# Run the application using gunicorn with thread support
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--threads", "2", "--timeout", "120", "main:app"] 