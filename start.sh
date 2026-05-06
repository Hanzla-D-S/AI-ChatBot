#!/bin/bash

echo "🚀 Building vector store..."
python backend/ingest.py

echo "🚀 Starting FastAPI backend..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

echo "⏳ Waiting for backend..."
sleep 5

echo "🚀 Starting Streamlit..."
streamlit run frontend/app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false