# AfriLens AI – Vision Intelligence for African SMEs

> **Take a photo. AfriLens thinks. You get clean numbers.**

AfriLens AI transforms photos of African SME receipts into trusted financial intelligence using computer vision, rule-based reasoning, and context-aware validation.

## 🎯 The Problem

African SMEs struggle with manual receipt management:
- **Time-consuming**: Hours spent manually entering receipt data
- **Error-prone**: Human errors in transcription
- **No insights**: Receipts sit in folders, unused
- **Poor quality**: Handwritten, faded, or damaged receipts are hard to process

## ✨ The Solution

AfriLens AI uses advanced OCR and intelligent extraction to:
1. **Extract** structured data from receipt images
2. **Validate** data quality with trust scores (0-100)
3. **Flag** anomalies and inconsistencies
4. **Provide** actionable insights for business decisions

## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │  React + Vite + Tailwind CSS
│  (React)    │  Mobile-first, judge-friendly UX
└──────┬──────┘
       │ HTTP/REST
┌──────▼──────┐
│   Backend   │  FastAPI + Python 3.11
│  (FastAPI)  │  Modular AI pipeline
└──────┬──────┘
       │
┌──────▼─────────────────────────────────────┐
│         AI Processing Pipeline             │
├────────────────────────────────────────────┤
│ 1. Image Preprocessing                     │
│    - Resize, grayscale, threshold, deskew │
├────────────────────────────────────────────┤
│ 2. OCR Engine (Tesseract)                 │
│    - Text extraction with confidence       │
│    - Line-by-line processing               │
├────────────────────────────────────────────┤
│ 3. Rules Engine (CORE INTELLIGENCE)        │
│    - Vendor detection                      │
│    - Date parsing (multiple formats)       │
│    - Line-item extraction                  │
│    - Price normalization                   │
│    - Total detection                       │
├────────────────────────────────────────────┤
│ 4. Validator                               │
│    - Mathematical verification             │
│    - Trust score calculation (0-100)        │
│    - Anomaly flagging                     │
└──────┬─────────────────────────────────────┘
       │
┌──────▼──────┐
│  SQLite DB  │  Auto-upgradeable schema
└─────────────┘
```

## 🧠 Trust Score Explained

Every receipt gets a **Trust Score (0-100)** based on:

- ✅ **Vendor name detected** (+15 points)
- ✅ **Date extracted** (+15 points)
- ✅ **Total amount found** (+20 points)
- ✅ **Line items match total** (+25 points)
- ✅ **High OCR confidence** (+15 points)
- ✅ **Sufficient text quality** (+20 points)

**Flags** indicate specific issues:
- `MISSING_VENDOR` - Couldn't identify vendor
- `MISSING_DATE` - Date not found
- `TOTAL_MISMATCH` - Line items don't sum to total
- `LOW_OCR_CONFIDENCE` - Poor image quality
- And more...

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Tesseract OCR installed

**Install Tesseract:**
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Initialize database
python -m backend.database

# Run server
uvicorn backend.main:app --reload
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## 📁 Project Structure

```
afrilens-ai/
├── backend/
│   ├── main.py           # Entry point
│   ├── api.py            # FastAPI endpoints
│   ├── ocr_engine.py     # OCR processing
│   ├── rules_engine.py   # Data extraction rules
│   ├── validator.py      # Trust scoring
│   ├── models.py         # Data models
│   ├── database.py       # SQLite management
│   ├── utils.py          # Helpers
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/Dashboard.jsx
│   │   ├── components/
│   │   │   ├── UploadCard.jsx
│   │   │   ├── ReceiptTable.jsx
│   │   │   ├── InsightBanner.jsx
│   │   │   └── StatsCard.jsx
│   │   └── services/api.js
│   └── package.json
│
├── examples/sample_receipts/  # Test images
├── README.md
├── DEMO.md
└── PITCH.md
```

## 🌍 African SME Intelligence

AfriLens AI is built with African SME context in mind:

- **Currency defaults**: KES (Kenyan Shillings)
- **Common patterns**: MPESA, CASH, TOTAL, VAT
- **Price formats**: Handles "1,200.50", "1200/=", "KES 500"
- **Date formats**: DD/MM/YYYY, DD-MM-YYYY, text dates
- **Vendor detection**: Recognizes common African business types

## 📊 API Endpoints

### `POST /upload`
Upload a receipt image. Returns structured data with trust score.

**Response:**
```json
{
  "data": {
    "vendor_name": "Nakumatt Supermarket",
    "transaction_date": "2024-01-15",
    "total_amount": 3200.50,
    "currency": "KES",
    "line_items": [...]
  },
  "trust_score": 87,
  "flags": ["TOTAL_MISMATCH"]
}
```

### `GET /receipts`
Get all processed receipts.

### `GET /stats`
Get statistics: total receipts, spending, trust scores, top vendors.

### `GET /export/csv`
Export all receipts as CSV.

### `GET /export/excel`
Export all receipts as Excel.

## 🎨 Features

- ✅ **Drag & drop upload** - Easy receipt submission
- ✅ **Real-time processing** - See "AI Thinking..." state
- ✅ **Trust score badges** - Color-coded quality indicators
- ✅ **Anomaly flags** - Clear issue identification
- ✅ **Insight banner** - "You spent 3,200 KES today at local vendors"
- ✅ **Export options** - CSV and Excel downloads
- ✅ **Mobile-friendly** - Works on phones and tablets

## 🏆 Before & After

**Before:**
- 📸 Photo of receipt in phone gallery
- 📝 Manual data entry into spreadsheet
- ⏱️ 5-10 minutes per receipt
- ❌ Human errors

**After:**
- 📸 Upload photo to AfriLens
- 🤖 AI extracts data in seconds
- ✅ Trust score shows confidence
- 📊 Instant insights and exports

## 🧪 Testing

Place sample receipt images in `examples/sample_receipts/` and upload through the UI.

## 📝 License

MIT License - Built for hackathon demonstration.

## 🙏 Acknowledgments

Built with:
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Built with ❤️ for African SMEs**
