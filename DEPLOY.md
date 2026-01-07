# AfriLens AI - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Docker (Recommended for Local/Server)

**Prerequisites:**
- Docker and Docker Compose installed

**Deploy:**
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Option 2: Railway (Backend) + Vercel (Frontend)

#### Backend on Railway

1. **Create Railway Account:**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy Backend:**
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Initialize project
   railway init
   
   # Deploy
   railway up
   ```

3. **Set Environment Variables:**
   - In Railway dashboard, add:
     - `PORT` (auto-set by Railway)
     - `PYTHON_VERSION=3.11`

4. **Get Backend URL:**
   - Copy the Railway URL (e.g., `https://afrilens-backend.railway.app`)

#### Frontend on Vercel

1. **Create Vercel Account:**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Deploy Frontend:**
   ```bash
   # Install Vercel CLI
   npm i -g vercel
   
   # Login
   vercel login
   
   # Deploy
   cd frontend
   vercel
   ```

3. **Set Environment Variable:**
   - In Vercel dashboard, add:
     - `VITE_API_URL` = Your Railway backend URL

4. **Update vercel.json:**
   - Edit `vercel.json` and replace `your-backend-url.railway.app` with your actual Railway URL

---

### Option 3: Render (Full Stack)

1. **Create Render Account:**
   - Go to https://render.com
   - Sign up with GitHub

2. **Deploy Backend:**
   - New > Web Service
   - Connect GitHub repo
   - Settings:
     - Build Command: `pip install -r backend/requirements.txt`
     - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
     - Environment: Python 3
   - Deploy

3. **Deploy Frontend:**
   - New > Static Site
   - Connect GitHub repo
   - Settings:
     - Build Command: `cd frontend && npm install && npm run build`
     - Publish Directory: `frontend/dist`
   - Add Environment Variable:
     - `VITE_API_URL` = Your backend Render URL

---

### Option 4: Heroku (Full Stack)

1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy Backend:**
   ```bash
   # Login
   heroku login
   
   # Create app
   heroku create afrilens-backend
   
   # Set buildpack
   heroku buildpacks:set heroku/python
   
   # Deploy
   git push heroku main
   ```

3. **Deploy Frontend:**
   ```bash
   # Create app
   heroku create afrilens-frontend
   
   # Set buildpack
   heroku buildpacks:set heroku/nodejs
   
   # Deploy
   cd frontend
   git push heroku main
   ```

---

## 🔧 Environment Variables

### Backend
```bash
PORT=8000
PYTHON_VERSION=3.11
DATABASE_PATH=./afrilens.db
UPLOAD_DIR=./uploads
```

### Frontend
```bash
VITE_API_URL=https://your-backend-url.com
```

---

## 📦 Production Build

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
# Output in frontend/dist/
```

---

## 🐳 Docker Deployment

### Build Images
```bash
# Backend
docker build -t afrilens-backend .

# Frontend
docker build -f Dockerfile.frontend -t afrilens-frontend .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

---

## ⚠️ Important Notes

1. **Tesseract OCR:**
   - Must be installed on the server
   - For Docker: Included in Dockerfile
   - For cloud: May need custom buildpack or system package

2. **Database:**
   - SQLite works for small deployments
   - For production scale, consider PostgreSQL
   - Update `backend/database.py` for PostgreSQL

3. **File Storage:**
   - Uploads stored locally in `uploads/` folder
   - For production, use cloud storage (S3, Cloudinary, etc.)

4. **CORS:**
   - Update `backend/api.py` CORS origins for production domain

5. **Environment:**
   - Never commit `.env` files
   - Use platform environment variables

---

## 🔍 Post-Deployment Checklist

- [ ] Backend health check: `https://your-backend.com/health`
- [ ] Frontend loads correctly
- [ ] API calls work from frontend
- [ ] File uploads work
- [ ] Database persists (check file storage)
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] SSL/HTTPS enabled

---

## 🆘 Troubleshooting

### Backend won't start
- Check Tesseract is installed
- Verify Python version (3.11+)
- Check port availability

### Frontend can't connect to backend
- Verify `VITE_API_URL` is set
- Check CORS settings
- Verify backend is running

### OCR not working
- Ensure Tesseract is installed on server
- Check Tesseract path in code
- Verify image uploads are working

---

## 📚 Platform-Specific Guides

- **Railway:** https://docs.railway.app
- **Vercel:** https://vercel.com/docs
- **Render:** https://render.com/docs
- **Heroku:** https://devcenter.heroku.com

---

**Need help?** Check the main README.md or open an issue.
