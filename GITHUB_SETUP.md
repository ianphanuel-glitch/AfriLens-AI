# 🚀 GitHub Deployment Guide

## Step 1: Initialize Git Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AfriLens AI - Vision Intelligence for African SMEs"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `afrilens-ai` (or your preferred name)
3. Description: "Vision Intelligence for African SMEs - OCR receipt processing with trust scoring"
4. Choose: Public or Private
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

## Step 3: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/afrilens-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Set Up GitHub Actions (Optional)

GitHub Actions workflows are already configured:

### Available Workflows:

1. **Test** (`test.yml`)
   - Runs on every push/PR
   - Tests backend and frontend
   - Ensures code quality

2. **Docker Build** (`docker-build.yml`)
   - Builds Docker images
   - Validates Docker configuration

3. **Deploy Backend** (`deploy-backend.yml`)
   - Deploys to Railway
   - Requires: `RAILWAY_TOKEN` secret

4. **Deploy Frontend** (`deploy-frontend.yml`)
   - Deploys to Vercel
   - Requires: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` secrets

### Enable GitHub Actions:

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Workflows will run automatically on push

## Step 5: Set Up Secrets (For Auto-Deployment)

### For Railway (Backend):

1. Get Railway token:
   - Go to https://railway.app
   - Account Settings > Tokens
   - Create new token

2. Add to GitHub:
   - Repository > Settings > Secrets and variables > Actions
   - New repository secret
   - Name: `RAILWAY_TOKEN`
   - Value: Your Railway token

### For Vercel (Frontend):

1. Get Vercel tokens:
   - Go to https://vercel.com/account/tokens
   - Create new token
   - Get Org ID and Project ID from Vercel dashboard

2. Add to GitHub:
   - `VERCEL_TOKEN` - Your Vercel token
   - `VERCEL_ORG_ID` - Your organization ID
   - `VERCEL_PROJECT_ID` - Your project ID
   - `VITE_API_URL` - Your backend URL (e.g., https://your-backend.railway.app)

## Step 6: GitHub Pages (Alternative - Static Frontend)

If you want to use GitHub Pages for frontend:

1. Go to Repository > Settings > Pages
2. Source: GitHub Actions
3. Create `.github/workflows/deploy-pages.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
    paths:
      - 'frontend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: |
          cd frontend
          npm install
          npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/dist
```

## 📋 Repository Structure

Your GitHub repository will have:

```
afrilens-ai/
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── docker-build.yml
│       ├── deploy-backend.yml
│       └── deploy-frontend.yml
├── backend/
├── frontend/
├── examples/
├── Dockerfile
├── docker-compose.yml
├── README.md
├── DEPLOY.md
└── ... (all other files)
```

## 🔒 Security Notes

- ✅ `.gitignore` already excludes sensitive files
- ✅ Database files excluded
- ✅ Upload directories excluded
- ✅ Environment files excluded

## 🎯 Quick Commands

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Your commit message"

# Push
git push origin main

# Create new branch
git checkout -b feature/your-feature

# Push branch
git push origin feature/your-feature
```

## 📚 Next Steps After GitHub Setup

1. **Enable GitHub Actions** - Automatic testing
2. **Set up secrets** - For auto-deployment
3. **Add collaborators** - If working in team
4. **Create releases** - Tag versions
5. **Set up branch protection** - Protect main branch

## 🆘 Troubleshooting

### Authentication Issues
```bash
# Use GitHub CLI
gh auth login

# Or use personal access token
git remote set-url origin https://YOUR_TOKEN@github.com/USERNAME/afrilens-ai.git
```

### Large Files
```bash
# If you have large files, use Git LFS
git lfs install
git lfs track "*.db"
git add .gitattributes
```

---

**Your code is now on GitHub!** 🎉

Share your repository URL and start collaborating!
