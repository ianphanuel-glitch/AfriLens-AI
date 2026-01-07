"""
Rules Engine for AfriLens AI.
Extracts structured data from OCR text using rule-based heuristics.
This is the CORE INTELLIGENCE layer.
"""
import re
from typing import List, Optional, Dict, Any
from .models import ReceiptData, LineItem
from .utils import normalize_price_string, extract_date, detect_currency


class RulesEngine:
    """
    Rule-based extraction engine for African SME receipts.
    Implements vendor detection, date parsing, line-item extraction, and total detection.
    """
    
    # Common African SME vendor patterns
    VENDOR_KEYWORDS = [
        'shop', 'store', 'supermarket', 'market', 'mall',
        'restaurant', 'cafe', 'hotel', 'lodge',
        'pharmacy', 'chemist', 'hospital', 'clinic',
        'station', 'fuel', 'petrol', 'gas',
        'mpesa', 'safaricom', 'airtel', 'telkom'
    ]
    
    # Common payment method keywords
    PAYMENT_KEYWORDS = ['mpesa', 'cash', 'card', 'credit', 'debit', 'mobile money']
    
    # Total detection patterns
    TOTAL_PATTERNS = [
        r'total[:\s]+([\d,./=]+)',
        r'amount[:\s]+([\d,./=]+)',
        r'paid[:\s]+([\d,./=]+)',
        r'sum[:\s]+([\d,./=]+)',
        r'balance[:\s]+([\d,./=]+)',
        r'grand\s+total[:\s]+([\d,./=]+)',
    ]
    
    # Line item patterns (price at end of line)
    LINE_ITEM_PATTERN = r'^(.+?)\s+([\d,./=]+)\s*$'
    
    def __init__(self):
        """Initialize rules engine."""
        pass
    
    def extract(self, ocr_lines: List[str], raw_text: str) -> ReceiptData:
        """
        Extract structured data from OCR text.
        This is the main extraction method.
        """
        receipt = ReceiptData(raw_text=raw_text)
        
        # Detect currency
        receipt.currency = detect_currency(raw_text)
        
        # Extract vendor name (usually in first few lines)
        receipt.vendor_name = self._extract_vendor(ocr_lines)
        
        # Extract date
        receipt.transaction_date = self._extract_date(ocr_lines, raw_text)
        
        # Extract total amount
        receipt.total_amount = self._extract_total(ocr_lines, raw_text)
        
        # Extract line items
        receipt.line_items = self._extract_line_items(ocr_lines)
        
        return receipt
    
    def _extract_vendor(self, lines: List[str]) -> Optional[str]:
        """
        Extract vendor name from top lines.
        Looks for business names, shop names, etc.
        """
        # Check first 5 lines for vendor name
        candidate_lines = lines[:5]
        
        for line in candidate_lines:
            line_upper = line.upper()
            
            # Skip if line is mostly numbers or dates
            if re.match(r'^[\d\s/:-]+$', line):
                continue
            
            # Skip payment method lines
            if any(keyword in line_upper for keyword in self.PAYMENT_KEYWORDS):
                continue
            
            # Skip total/amount lines
            if re.search(r'\b(total|amount|paid|balance)\b', line_upper):
                continue
            
            # If line has reasonable length and contains letters, it might be vendor
            if len(line) > 3 and len(line) < 100 and re.search(r'[A-Za-z]', line):
                # Clean up common prefixes/suffixes
                vendor = line.strip()
                vendor = re.sub(r'^[#\*]+', '', vendor)  # Remove leading symbols
                vendor = re.sub(r'[#\*]+$', '', vendor)  # Remove trailing symbols
                vendor = vendor.strip()
                
                if vendor and len(vendor) > 2:
                    return vendor
        
        return None
    
    def _extract_date(self, lines: List[str], full_text: str) -> Optional[str]:
        """
        Extract transaction date.
        Tries multiple strategies.
        """
        # Strategy 1: Check first 10 lines
        for line in lines[:10]:
            date = extract_date(line)
            if date:
                return date
        
        # Strategy 2: Search full text
        date = extract_date(full_text)
        if date:
            return date
        
        return None
    
    def _extract_total(self, lines: List[str], full_text: str) -> Optional[float]:
        """
        Extract total amount using multiple heuristics.
        Returns the highest confidence total found.
        """
        candidates = []
        
        # Strategy 1: Look for explicit "TOTAL" patterns
        for pattern in self.TOTAL_PATTERNS:
            matches = re.finditer(pattern, full_text, re.IGNORECASE)
            for match in matches:
                price_str = match.group(1)
                price = normalize_price_string(price_str)
                if price and price > 0:
                    candidates.append((price, 10))  # High confidence
        
        # Strategy 2: Look at last few lines (totals usually at bottom)
        for line in lines[-5:]:
            line_upper = line.upper()
            
            # If line contains "total" or "amount", extract number
            if re.search(r'\b(total|amount|paid|sum)\b', line_upper):
                # Extract all numbers from line
                numbers = re.findall(r'[\d,./=]+', line)
                for num_str in numbers:
                    price = normalize_price_string(num_str)
                    if price and price > 0:
                        candidates.append((price, 8))  # Medium-high confidence
        
        # Strategy 3: Largest number in last 3 lines (heuristic)
        last_lines = ' '.join(lines[-3:])
        numbers = re.findall(r'[\d,./=]+', last_lines)
        for num_str in numbers:
            price = normalize_price_string(num_str)
            if price and price > 0:
                # Lower confidence, but still consider
                candidates.append((price, 5))
        
        if not candidates:
            return None
        
        # Return highest confidence candidate, or largest if tie
        candidates.sort(key=lambda x: (x[1], x[0]), reverse=True)
        return candidates[0][0]
    
    def _extract_line_items(self, lines: List[str]) -> List[LineItem]:
        """
        Extract line items from receipt.
        Looks for patterns like: "Item Name    100.00"
        """
        line_items = []
        
        # Skip first 3 lines (usually header/vendor) and last 3 lines (usually totals)
        candidate_lines = lines[3:-3] if len(lines) > 6 else lines[3:]
        
        for idx, line in enumerate(candidate_lines):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip lines that are clearly not items (dates, vendor info, etc.)
            if re.match(r'^[\d\s/:-]+$', line):  # Only numbers/dates
                continue
            
            if any(keyword in line.upper() for keyword in ['TOTAL', 'AMOUNT', 'PAID', 'CASH', 'MPESA']):
                continue
            
            # Try to extract: description + price
            # Pattern: text followed by number at end
            match = re.search(r'^(.+?)\s+([\d,./=]+)\s*$', line)
            if match:
                description = match.group(1).strip()
                price_str = match.group(2)
                price = normalize_price_string(price_str)
                
                if price and price > 0 and len(description) > 2:
                    # Try to extract quantity and unit price if present
                    # Pattern: "Item x2 @ 50.00 = 100.00"
                    qty_match = re.search(r'x\s*(\d+(?:\.\d+)?)', description, re.IGNORECASE)
                    unit_match = re.search(r'@\s*([\d,./=]+)', description, re.IGNORECASE)
                    
                    quantity = None
                    unit_price = None
                    
                    if qty_match:
                        try:
                            quantity = float(qty_match.group(1))
                        except ValueError:
                            pass
                    
                    if unit_match:
                        unit_price = normalize_price_string(unit_match.group(1))
                    
                    line_items.append(LineItem(
                        description=description,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=price,
                        line_number=idx + 4  # Account for skipped lines
                    ))
            else:
                # No clear price pattern, but might be item description
                # Check if line has reasonable length and contains letters
                if 5 < len(line) < 80 and re.search(r'[A-Za-z]', line):
                    # Might be item without price, or price on next line
                    # For now, create item with description only
                    line_items.append(LineItem(
                        description=line,
                        line_number=idx + 4
                    ))
        
        return line_items


# Global instance
rules_engine = RulesEngine()
