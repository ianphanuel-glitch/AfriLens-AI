@echo off
REM Deployment script for AfriLens AI (Windows)

echo.
echo ========================================
echo AfriLens AI Deployment Script
echo ========================================
echo.

REM Check if Docker is available
where docker >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Docker found
    echo.
    echo Building Docker images...
    docker-compose build
    echo.
    echo Starting services...
    docker-compose up -d
    echo.
    echo [SUCCESS] Deployment complete!
    echo.
    echo Services:
    echo   - Frontend: http://localhost
    echo   - Backend: http://localhost:8000
    echo   - API Docs: http://localhost:8000/docs
    echo.
    echo View logs: docker-compose logs -f
    echo Stop: docker-compose down
) else (
    echo [ERROR] Docker not found. Please install Docker first.
    echo.
    echo Alternative: Deploy to cloud platform (see DEPLOY.md)
    exit /b 1
)
