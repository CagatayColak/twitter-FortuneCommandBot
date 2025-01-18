FROM python:3.9-slim

# Install fortune and required system packages
RUN apt-get update && \
    apt-get install -y fortune fortune-mod && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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

# Run the application
CMD ["python", "main.py"] 