"""
OCR Engine for AfriLens AI.
Uses Tesseract OCR with confidence scoring and line-by-line processing.
"""
import pytesseract
from typing import List, Dict, Tuple, Any
import numpy as np
from .utils import preprocess_image, clean_text


class OCREngine:
    """Handles OCR processing with confidence scoring."""
    
    def __init__(self):
        """Initialize OCR engine."""
        # Configure Tesseract for better accuracy
        self.config = '--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,/-:() '
    
    def extract_text(self, image_path: str) -> str:
        """
        Extract raw text from image.
        Returns cleaned text string.
        """
        try:
            # Preprocess image
            processed_img = preprocess_image(image_path)
            
            # Run OCR
            text = pytesseract.image_to_string(processed_img, config=self.config)
            
            return clean_text(text)
        except Exception as e:
            raise ValueError(f"OCR extraction failed: {str(e)}")
    
    def extract_with_confidence(self, image_path: str) -> Tuple[str, float, List[Dict[str, Any]]]:
        """
        Extract text with confidence scores per line.
        Returns: (full_text, average_confidence, line_data)
        """
        try:
            # Preprocess image
            processed_img = preprocess_image(image_path)
            
            # Get detailed OCR data
            ocr_data = pytesseract.image_to_data(
                processed_img, 
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and confidence per line
            lines = []
            current_line = []
            current_y = None
            line_confidences = []
            
            n_boxes = len(ocr_data['text'])
            for i in range(n_boxes):
                text = ocr_data['text'][i].strip()
                conf = int(ocr_data['conf'][i])
                
                if text and conf > 0:  # Valid text
                    y_pos = ocr_data['top'][i]
                    
                    # Group words on same line (within 5 pixels)
                    if current_y is None or abs(y_pos - current_y) < 5:
                        current_line.append(text)
                        line_confidences.append(conf)
                        current_y = y_pos
                    else:
                        # New line detected
                        if current_line:
                            line_text = ' '.join(current_line)
                            avg_conf = sum(line_confidences) / len(line_confidences) if line_confidences else 0
                            lines.append({
                                'text': line_text,
                                'confidence': round(avg_conf, 2),
                                'line_number': len(lines) + 1
                            })
                        
                        current_line = [text]
                        line_confidences = [conf]
                        current_y = y_pos
            
            # Add last line
            if current_line:
                line_text = ' '.join(current_line)
                avg_conf = sum(line_confidences) / len(line_confidences) if line_confidences else 0
                lines.append({
                    'text': line_text,
                    'confidence': round(avg_conf, 2),
                    'line_number': len(lines) + 1
                })
            
            # Calculate average confidence
            all_confs = [line['confidence'] for line in lines]
            avg_confidence = sum(all_confs) / len(all_confs) if all_confs else 0
            
            # Full text
            full_text = '\n'.join([line['text'] for line in lines])
            
            return clean_text(full_text), round(avg_confidence, 2), lines
            
        except Exception as e:
            raise ValueError(f"OCR extraction with confidence failed: {str(e)}")
    
    def extract_lines(self, image_path: str) -> List[str]:
        """
        Extract text as list of lines.
        Returns list of cleaned line strings.
        """
        text, _, lines = self.extract_with_confidence(image_path)
        return [line['text'] for line in lines]


# Global instance
ocr_engine = OCREngine()
