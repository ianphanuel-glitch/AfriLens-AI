# AfriLens AI - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Install Tesseract OCR

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### Step 2: Backend

```bash
cd backend
pip install -r requirements.txt
python -m backend.database
uvicorn backend.main:app --reload
```

✅ Backend running on `http://localhost:8000`

### Step 3: Frontend

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend running on `http://localhost:5173`

### Step 4: Test It!

1. Open `http://localhost:5173`
2. Upload a receipt image
3. Watch the AI extract data!

## 📋 What You Get

- ✅ Full-stack application
- ✅ OCR + extraction pipeline
- ✅ Trust scoring (0-100)
- ✅ Anomaly flagging
- ✅ Business insights
- ✅ CSV/Excel export
- ✅ Mobile-friendly UI

## 🎯 Demo Flow

1. Upload receipt → See "AI Thinking..."
2. View extracted data with trust score
3. Check insights banner
4. Export to Excel

**Full demo script:** See `DEMO.md`

## 📚 Documentation

- `README.md` - Full documentation
- `DEMO.md` - 2-minute demo script
- `PITCH.md` - Pitch deck
- `SETUP.md` - Detailed setup guide

## 🐛 Troubleshooting

**Tesseract not found?**
- Ensure it's installed and in PATH
- Windows: Check installation path

**Port in use?**
- Change ports in config files

**Import errors?**
- Run: `pip install -r backend/requirements.txt`
- Run: `npm install` in frontend/

---

**Ready to demo?** Follow `DEMO.md` for the perfect 2-minute presentation!
