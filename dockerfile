# Use an official, highly optimized Python slim runtime
FROM python:3.11-slim

# Prevent Python from writing .pyc files to disk and ensure logs print instantly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container virtual environment
WORKDIR /workspace

# Copy requirements first to leverage Docker's caching layers optimally
COPY requirements.txt .

# Install dependencies cleanly without saving cache data to minimize image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application files into the working directory
COPY ./app ./app

# Expose port 8000 for local network traffic mapping
EXPOSE 8000

# Fire up the Uvicorn web engine pointing to your main FastAPI application block
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]

