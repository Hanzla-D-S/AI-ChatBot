#!/bin/bash

# Start FastAPI backend in background on port 8000
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to be ready
sleep 5

# Start Streamlit on port 7860 (Hugging Face default)
streamlit run frontend/app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false