"""
FastAPI endpoints for AfriLens AI.
Implements all required API routes with trust scores and flags.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from typing import List, Dict, Any
import json
import csv
import io
from pathlib import Path
from datetime import datetime

from .database import get_db_connection, init_database, upgrade_database
from .models import ReceiptResponse, StatsResponse
from .ocr_engine import ocr_engine
from .rules_engine import rules_engine
from .validator import validator
from .utils import ensure_upload_dir


# Initialize FastAPI app
app = FastAPI(
    title="AfriLens AI API",
    description="Vision Intelligence for African SMEs",
    version="1.0.0"
)

# CORS middleware for frontend
# In production, set CORS_ORIGINS environment variable
import os
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        init_database()
        upgrade_database()
    except Exception as e:
        print(f"Warning: Database initialization issue: {e}")


@app.post("/upload")
async def upload_receipt(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload and process a receipt image.
    Returns structured data with trust score and flags.
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file
        upload_dir = ensure_upload_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = Path(file.filename).suffix or '.jpg'
        saved_path = upload_dir / f"{timestamp}_{file.filename}"
        
        with open(saved_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process receipt through pipeline
        # Step 1: OCR
        raw_text, ocr_confidence, ocr_lines = ocr_engine.extract_with_confidence(str(saved_path))
        ocr_line_texts = [line['text'] for line in ocr_lines]
        
        # Step 2: Rules engine
        receipt_data = rules_engine.extract(ocr_line_texts, raw_text)
        receipt_data.ocr_confidence = ocr_confidence
        
        # Step 3: Validator
        validation = validator.validate(receipt_data)
        
        # Step 4: Save to database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO receipts (
                    filename, image_path, vendor_name, transaction_date,
                    total_amount, currency, trust_score, flags,
                    raw_ocr_text, extracted_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                file.filename,
                str(saved_path),
                receipt_data.vendor_name,
                receipt_data.transaction_date,
                receipt_data.total_amount,
                receipt_data.currency,
                validation.trust_score,
                json.dumps(validation.flags),
                raw_text,
                json.dumps(receipt_data.to_dict())
            ))
            
            receipt_id = cursor.lastrowid
            
            # Save line items
            for item in receipt_data.line_items:
                cursor.execute("""
                    INSERT INTO line_items (
                        receipt_id, description, quantity, unit_price,
                        total_price, line_number
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    receipt_id,
                    item.description,
                    item.quantity,
                    item.unit_price,
                    item.total_price,
                    item.line_number
                ))
        
        # Return response
        return {
            "data": receipt_data.to_dict(),
            "trust_score": validation.trust_score,
            "flags": validation.flags,
            "id": receipt_id,
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.get("/receipts")
async def get_receipts() -> Dict[str, Any]:
    """
    Get all receipts with trust scores and flags.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, filename, vendor_name, transaction_date,
                       total_amount, currency, trust_score, flags,
                       extracted_data, created_at
                FROM receipts
                ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            
            receipts = []
            for row in rows:
                flags = json.loads(row['flags']) if row['flags'] else []
                data = json.loads(row['extracted_data']) if row['extracted_data'] else {}
                
                receipts.append({
                    "id": row['id'],
                    "filename": row['filename'],
                    "data": data,
                    "trust_score": row['trust_score'],
                    "flags": flags,
                    "created_at": row['created_at']
                })
            
            return {
                "data": receipts,
                "count": len(receipts)
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch receipts: {str(e)}")


@app.get("/stats")
async def get_stats() -> Dict[str, Any]:
    """
    Get statistics about receipts.
    Returns total receipts, spending, trust scores, etc.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Total receipts
            cursor.execute("SELECT COUNT(*) as count FROM receipts")
            total_receipts = cursor.fetchone()['count']
            
            # Total spent
            cursor.execute("""
                SELECT SUM(total_amount) as total, currency
                FROM receipts
                WHERE total_amount IS NOT NULL
                GROUP BY currency
                ORDER BY total DESC
                LIMIT 1
            """)
            total_row = cursor.fetchone()
            total_spent = total_row['total'] if total_row and total_row['total'] else 0.0
            currency = total_row['currency'] if total_row and total_row['currency'] else 'KES'
            
            # Average trust score
            cursor.execute("SELECT AVG(trust_score) as avg_score FROM receipts")
            avg_score_row = cursor.fetchone()
            avg_trust_score = round(avg_score_row['avg_score'], 2) if avg_score_row and avg_score_row['avg_score'] else 0.0
            
            # Receipts today
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM receipts
                WHERE DATE(created_at) = DATE('now')
            """)
            receipts_today = cursor.fetchone()['count']
            
            # Top vendors
            cursor.execute("""
                SELECT vendor_name, COUNT(*) as count, SUM(total_amount) as total
                FROM receipts
                WHERE vendor_name IS NOT NULL
                GROUP BY vendor_name
                ORDER BY count DESC, total DESC
                LIMIT 5
            """)
            
            top_vendors = []
            for row in cursor.fetchall():
                top_vendors.append({
                    "name": row['vendor_name'],
                    "receipt_count": row['count'],
                    "total_spent": row['total'] if row['total'] else 0.0
                })
            
            return {
                "data": {
                    "total_receipts": total_receipts,
                    "total_spent": round(total_spent, 2),
                    "currency": currency,
                    "average_trust_score": avg_trust_score,
                    "receipts_today": receipts_today,
                    "top_vendors": top_vendors
                },
                "trust_score": 100,  # Stats endpoint is always trusted
                "flags": []
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


@app.get("/export/csv")
async def export_csv():
    """
    Export all receipts as CSV.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, filename, vendor_name, transaction_date,
                       total_amount, currency, trust_score, flags, created_at
                FROM receipts
                ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            
            # Create CSV in memory
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Header
            writer.writerow([
                'ID', 'Filename', 'Vendor', 'Date', 'Total', 'Currency',
                'Trust Score', 'Flags', 'Created At'
            ])
            
            # Data rows
            for row in rows:
                flags_str = ', '.join(json.loads(row['flags'])) if row['flags'] else ''
                writer.writerow([
                    row['id'],
                    row['filename'],
                    row['vendor_name'] or '',
                    row['transaction_date'] or '',
                    row['total_amount'] or '',
                    row['currency'] or 'KES',
                    row['trust_score'],
                    flags_str,
                    row['created_at']
                ])
            
            output.seek(0)
            
            return StreamingResponse(
                io.BytesIO(output.getvalue().encode('utf-8')),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=afrilens_receipts.csv"}
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@app.get("/export/excel")
async def export_excel():
    """
    Export all receipts as Excel (CSV format for simplicity).
    For full Excel support, would need openpyxl or xlsxwriter.
    """
    # For hackathon, we'll return CSV with .xlsx extension
    # In production, would use openpyxl for true Excel format
    return await export_csv()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AfriLens AI"}
