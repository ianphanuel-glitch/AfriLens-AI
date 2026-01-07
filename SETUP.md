# AfriLens AI - Setup Guide

## Quick Start

### 1. Install Prerequisites

**Tesseract OCR:**
- **Windows**: Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Add to PATH during installation
  - Or set `TESSDATA_PREFIX` environment variable
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

**Python 3.11+:**
- Download from [python.org](https://www.python.org/downloads/)
- Verify: `python --version`

**Node.js 18+:**
- Download from [nodejs.org](https://nodejs.org/)
- Verify: `node --version`

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m backend.database

# Run server
uvicorn backend.main:app --reload
```

Backend will run on `http://localhost:8000`

**Or use the script:**
- Windows: `run_backend.bat`
- Linux/Mac: `./run_backend.sh`

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend will run on `http://localhost:5173`

**Or use the script:**
- Windows: `run_frontend.bat`
- Linux/Mac: `./run_frontend.sh`

### 4. Verify Installation

1. Open `http://localhost:5173` in browser
2. You should see the AfriLens AI dashboard
3. Try uploading a receipt image

## Troubleshooting

### Tesseract Not Found

**Error:** `TesseractNotFoundError`

**Solution:**
- Ensure Tesseract is installed
- Add to PATH or set environment variable:
  - Windows: Add Tesseract bin folder to PATH
  - Or set: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
- Change port in `backend/main.py` or `frontend/vite.config.js`
- Or kill process using the port

### Database Errors

**Error:** `Database locked` or similar

**Solution:**
- Delete `afrilens.db` and reinitialize
- Run: `python -m backend.database`

### Import Errors

**Error:** `ModuleNotFoundError`

**Solution:**
- Ensure you're in the project root
- Install requirements: `pip install -r backend/requirements.txt`
- Check Python path includes project root

## Development

### Backend Development

```bash
# Run with auto-reload
uvicorn backend.main:app --reload

# Run on different port
uvicorn backend.main:app --reload --port 8001
```

### Frontend Development

```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Production Deployment

### Backend

1. Use production ASGI server:
   ```bash
   pip install gunicorn
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. Set environment variables:
   - `DATABASE_PATH` (optional)
   - `UPLOAD_DIR` (optional)

### Frontend

1. Build:
   ```bash
   cd frontend
   npm run build
   ```

2. Serve `dist/` folder with nginx or similar

## Next Steps

- Add sample receipts to `examples/sample_receipts/`
- Review `DEMO.md` for demo script
- Review `PITCH.md` for pitch deck
- Read `README.md` for full documentation
