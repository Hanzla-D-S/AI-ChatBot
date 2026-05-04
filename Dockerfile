# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]