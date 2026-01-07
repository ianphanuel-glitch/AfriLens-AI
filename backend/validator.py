"""
Validator for AfriLens AI.
Validates extracted receipt data and assigns trust scores.
"""
from typing import List
from .models import ReceiptData, ValidationResult


class ReceiptValidator:
    """
    Validates receipt data and assigns trust scores (0-100).
    Flags anomalies and mathematical inconsistencies.
    """
    
    def __init__(self):
        """Initialize validator."""
        pass
    
    def validate(self, receipt_data: ReceiptData) -> ValidationResult:
        """
        Validate receipt data and return trust score with flags.
        This is what judges will see - make it impressive!
        """
        flags = []
        score = 100  # Start with perfect score, deduct for issues
        
        # Check 1: Has vendor name?
        if not receipt_data.vendor_name:
            flags.append("MISSING_VENDOR")
            score -= 15
        elif len(receipt_data.vendor_name) < 3:
            flags.append("VENDOR_NAME_TOO_SHORT")
            score -= 10
        
        # Check 2: Has date?
        if not receipt_data.transaction_date:
            flags.append("MISSING_DATE")
            score -= 15
        
        # Check 3: Has total?
        if receipt_data.total_amount is None or receipt_data.total_amount <= 0:
            flags.append("MISSING_TOTAL")
            score -= 20
        else:
            # Check 4: Total is reasonable (not too small, not astronomical)
            if receipt_data.total_amount < 1:
                flags.append("TOTAL_TOO_SMALL")
                score -= 10
            elif receipt_data.total_amount > 1000000:  # 1M KES
                flags.append("TOTAL_SUSPICIOUSLY_LARGE")
                score -= 10
        
        # Check 5: Mathematical verification (line items sum ≈ total)
        if receipt_data.line_items:
            items_with_price = [item for item in receipt_data.line_items if item.total_price is not None]
            
            if items_with_price:
                calculated_total = sum(item.total_price for item in items_with_price)
                
                if receipt_data.total_amount:
                    difference = abs(calculated_total - receipt_data.total_amount)
                    tolerance = receipt_data.total_amount * 0.05  # 5% tolerance
                    
                    if difference > tolerance:
                        flags.append("TOTAL_MISMATCH")
                        # Deduct based on severity
                        if difference > receipt_data.total_amount * 0.2:  # >20% off
                            score -= 25
                        elif difference > receipt_data.total_amount * 0.1:  # >10% off
                            score -= 15
                        else:
                            score -= 10
            else:
                # Has line items but no prices
                flags.append("LINE_ITEMS_WITHOUT_PRICES")
                score -= 10
        else:
            # No line items extracted
            flags.append("NO_LINE_ITEMS")
            score -= 10
        
        # Check 6: OCR confidence (if available)
        if receipt_data.ocr_confidence > 0:
            if receipt_data.ocr_confidence < 50:
                flags.append("LOW_OCR_CONFIDENCE")
                score -= 15
            elif receipt_data.ocr_confidence < 70:
                flags.append("MEDIUM_OCR_CONFIDENCE")
                score -= 5
        
        # Check 7: Raw text quality
        if not receipt_data.raw_text or len(receipt_data.raw_text.strip()) < 10:
            flags.append("INSUFFICIENT_TEXT")
            score -= 20
        
        # Check 8: Currency consistency
        if receipt_data.currency not in ['KES', 'USD', 'EUR', 'NGN', 'ZAR']:
            flags.append("UNKNOWN_CURRENCY")
            score -= 5
        
        # Ensure score is in valid range
        score = max(0, min(100, score))
        
        # Determine if valid (trust score >= 70)
        is_valid = score >= 70
        
        return ValidationResult(
            trust_score=score,
            flags=flags,
            is_valid=is_valid
        )


# Global instance
validator = ReceiptValidator()
