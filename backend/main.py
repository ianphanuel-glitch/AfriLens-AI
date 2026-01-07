"""
Main entry point for AfriLens AI backend.
Run with: uvicorn backend.main:app --reload
"""
from .api import app

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
