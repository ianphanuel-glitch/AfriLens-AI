# 🚀 Quick Deployment Guide

## Option 1: Docker (Fastest - Recommended)

**Prerequisites:** Docker Desktop installed

```bash
# Windows
deploy.bat

# Linux/Mac
chmod +x deploy.sh
./deploy.sh

# Or manually:
docker-compose up -d
```

**Access:**
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Option 2: Railway + Vercel (Cloud - Free Tier)

### Backend (Railway)

1. Go to https://railway.app
2. New Project > Deploy from GitHub
3. Select your repo
4. Railway auto-detects Python
5. Add environment variable: `PORT` (auto-set)

**Get your Railway URL:** `https://your-app.railway.app`

### Frontend (Vercel)

1. Go to https://vercel.com
2. New Project > Import from GitHub
3. Select your repo
4. Root Directory: `frontend`
5. Build Command: `npm run build`
6. Output Directory: `dist`
7. Add Environment Variable:
   - `VITE_API_URL` = Your Railway URL

**Done!** Your site is live.

---

## Option 3: Render (All-in-One)

1. Go to https://render.com
2. New > Web Service (Backend)
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
3. New > Static Site (Frontend)
   - Build: `cd frontend && npm install && npm run build`
   - Publish: `frontend/dist`
   - Add env: `VITE_API_URL` = Backend URL

---

## Manual Local Deployment

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run build
# Serve dist/ folder with any static server
```

---

## Environment Variables

Create `.env` file:
```bash
PORT=8000
CORS_ORIGINS=http://localhost:5173
```

Frontend: Create `frontend/.env.production`:
```bash
VITE_API_URL=https://your-backend-url.com
```

---

**Full guide:** See `DEPLOY.md` for detailed instructions.
