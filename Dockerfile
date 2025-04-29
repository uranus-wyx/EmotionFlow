# Use an official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Upgrade pip (可選但推薦)
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

ENV PORT 8080

# Command to run app
CMD exec gunicorn --bind :$PORT app:app
