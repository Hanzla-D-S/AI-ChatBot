FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Build vector store at image build time
# RUN python backend/ingest.py

# Expose Hugging Face default port
EXPOSE 7860

# Start script
CMD ["bash", "start.sh"]