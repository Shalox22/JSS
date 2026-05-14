# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model file
COPY model/poultry_disease_cnn.h5 .

# Copy the API code
COPY api.py .

# Expose port 8000
EXPOSE 8000

# Run the FastAPI app with uvicorn and use Render's PORT if set
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]