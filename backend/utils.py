"""
Utility functions for AfriLens AI.
Image processing, text normalization, and helper functions.
"""
import re
from pathlib import Path
from typing import Optional, Tuple
import cv2
import numpy as np
from PIL import Image


def ensure_upload_dir() -> Path:
    """Ensure upload directory exists and return its path."""
    upload_dir = Path(__file__).parent.parent / "uploads"
    upload_dir.mkdir(exist_ok=True)
    return upload_dir


def normalize_price_string(text: str) -> Optional[float]:
    """
    Normalize price strings to float.
    Handles African receipt formats: "1,200.50", "1200/=", "KES 500", etc.
    """
    if not text:
        return None
    
    # Remove currency symbols and text
    text = re.sub(r'[A-Z]{3}\s*', '', text, flags=re.IGNORECASE)  # Remove "KES", "USD", etc.
    text = text.replace('KES', '').replace('USD', '').replace('EUR', '')
    text = text.replace('/=', '').replace('=', '').replace('-', '')
    text = text.strip()
    
    # Remove common words
    text = re.sub(r'\b(cash|total|amount|paid|balance)\b', '', text, flags=re.IGNORECASE)
    text = text.strip()
    
    # Remove all non-digit characters except decimal point and comma
    text = re.sub(r'[^\d.,]', '', text)
    
    if not text:
        return None
    
    # Handle comma as thousand separator (e.g., "1,200.50")
    if ',' in text and '.' in text:
        # Assume comma is thousands, dot is decimal
        text = text.replace(',', '')
    elif ',' in text:
        # Could be decimal separator in some locales, but we'll assume thousands
        if text.count(',') == 1 and len(text.split(',')[1]) <= 2:
            text = text.replace(',', '.')
        else:
            text = text.replace(',', '')
    
    try:
        return float(text)
    except ValueError:
        return None


def extract_date(text: str) -> Optional[str]:
    """
    Extract date from text in various formats.
    Returns ISO format date string (YYYY-MM-DD) or None.
    """
    if not text:
        return None
    
    # Common date patterns in African receipts
    # Check YYYY-MM-DD first (4 digits at start)
    yyyy_pattern = r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})'  # YYYY/MM/DD or YYYY-MM-DD
    match = re.search(yyyy_pattern, text)
    if match:
        try:
            year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
            if 1 <= month <= 12 and 1 <= day <= 31:
                return f"{year:04d}-{month:02d}-{day:02d}"
        except (ValueError, IndexError):
            pass
    
    # Text month format: DD Mon YYYY
    text_month_pattern = r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{2,4})'
    months = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    match = re.search(text_month_pattern, text, re.IGNORECASE)
    if match:
        try:
            day = int(match.group(1))
            month = months[match.group(2).lower()[:3]]
            year = int(match.group(3))
            if year < 100:
                year += 2000
            return f"{year:04d}-{month:02d}-{day:02d}"
        except (ValueError, IndexError, KeyError):
            pass
    
    # DD/MM/YYYY or DD-MM-YYYY (common in Africa)
    ddmmyyyy_pattern = r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'
    match = re.search(ddmmyyyy_pattern, text)
    if match:
        try:
            parts = [int(g) for g in match.groups()]
            # If first part > 31, might be YYYY-MM-DD (already handled above, but double-check)
            if parts[0] > 31:
                year, month, day = parts[0], parts[1], parts[2]
            else:
                # Assume DD-MM-YYYY (common in Africa)
                day, month, year = parts[0], parts[1], parts[2]
                if year < 100:
                    year += 2000
            
            if 1 <= month <= 12 and 1 <= day <= 31:
                return f"{year:04d}-{month:02d}-{day:02d}"
        except (ValueError, IndexError):
            pass
    
    return None


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocess image for OCR: resize, grayscale, threshold, deskew.
    Returns processed image as numpy array.
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
    
    # Resize if too large (max 2000px on longest side)
    height, width = img.shape[:2]
    max_dim = 2000
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    # Convert to grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    # Apply adaptive thresholding for better OCR
    # Use adaptive threshold to handle varying lighting
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Optional: deskew (simple rotation correction)
    # This is a simplified version - full deskew would use Hough transform
    try:
        coords = np.column_stack(np.where(thresh > 0))
        if len(coords) > 0:
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
            
            # Only correct if angle is significant
            if abs(angle) > 0.5:
                (h, w) = thresh.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                thresh = cv2.warpAffine(thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    except Exception:
        # If deskew fails, continue with original
        pass
    
    return thresh


def clean_text(text: str) -> str:
    """Clean OCR text: remove extra whitespace, normalize."""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    return text.strip()


def detect_currency(text: str) -> str:
    """
    Detect currency from text.
    Defaults to KES for African SME context.
    """
    text_upper = text.upper()
    
    if 'KES' in text_upper or 'KENYA' in text_upper or 'SHILLING' in text_upper:
        return 'KES'
    elif 'USD' in text_upper or 'DOLLAR' in text_upper:
        return 'USD'
    elif 'EUR' in text_upper or 'EURO' in text_upper:
        return 'EUR'
    elif 'NGN' in text_upper or 'NAIRA' in text_upper:
        return 'NGN'
    elif 'ZAR' in text_upper or 'RAND' in text_upper:
        return 'ZAR'
    else:
        return 'KES'  # Default for African SME context
