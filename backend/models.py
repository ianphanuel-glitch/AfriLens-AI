"""
Data models for AfriLens AI.
Defines the structure of receipt data and API responses.
"""
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


@dataclass
class LineItem:
    """Represents a single line item from a receipt."""
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    line_number: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ReceiptData:
    """Structured receipt data extracted from OCR."""
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: str = "KES"
    line_items: List[LineItem] = None
    raw_text: str = ""
    ocr_confidence: float = 0.0
    
    def __post_init__(self):
        """Initialize line_items if None."""
        if self.line_items is None:
            self.line_items = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "vendor_name": self.vendor_name,
            "transaction_date": self.transaction_date,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "line_items": [item.to_dict() for item in self.line_items],
            "raw_text": self.raw_text,
            "ocr_confidence": self.ocr_confidence
        }


@dataclass
class ValidationResult:
    """Result of receipt validation."""
    trust_score: int  # 0-100
    flags: List[str]  # List of anomaly flags
    is_valid: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "trust_score": self.trust_score,
            "flags": self.flags,
            "is_valid": self.is_valid
        }


@dataclass
class ReceiptResponse:
    """Complete API response for a receipt."""
    id: int
    filename: str
    data: ReceiptData
    trust_score: int
    flags: List[str]
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "id": self.id,
            "filename": self.filename,
            "data": self.data.to_dict(),
            "trust_score": self.trust_score,
            "flags": self.flags,
            "created_at": self.created_at
        }


@dataclass
class StatsResponse:
    """Statistics response."""
    total_receipts: int
    total_spent: float
    currency: str
    average_trust_score: float
    receipts_today: int
    top_vendors: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_receipts": self.total_receipts,
            "total_spent": self.total_spent,
            "currency": self.currency,
            "average_trust_score": self.average_trust_score,
            "receipts_today": self.receipts_today,
            "top_vendors": self.top_vendors
        }
