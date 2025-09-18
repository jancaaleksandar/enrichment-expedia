# Use Python 3.13 as base image
FROM python:3.13-rc-slim

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7890 \
    HOST=0.0.0.0

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the API port
EXPOSE 7890

# Run uvicorn directly (production-friendly, no reload)
ENTRYPOINT ["uvicorn", "entrypoint:app", "--host", "0.0.0.0", "--port", "7890"]
