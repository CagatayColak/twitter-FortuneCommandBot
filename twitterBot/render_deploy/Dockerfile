FROM python:3.9-slim

# Install fortune
RUN apt-get update && \
    apt-get install -y fortune-mod && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY main.py .

# Run the application
CMD ["python", "main.py"] 