# Use an official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

EXPOSE 8080

# Command to run app
CMD ["sh", "-c", "gunicorn", "-b", "0.0.0.0:8080", "app:server"]
