#!/bin/bash
# Run AfriLens AI Backend

echo "Starting AfriLens AI Backend..."
echo "Make sure Tesseract OCR is installed!"

cd backend
python -m backend.database
cd ..

uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
