# Market IQ Application Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements_full.txt .
RUN pip install --no-cache-dir -r requirements_full.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Copy application code
COPY src/ ./src/

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=src.main
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

