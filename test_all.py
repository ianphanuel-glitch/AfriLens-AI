"""Comprehensive test suite for AfriLens AI."""
import sys
sys.path.insert(0, '.')

def test_imports():
    """Test all backend imports."""
    print("=" * 60)
    print("TEST 1: Backend Module Imports")
    print("=" * 60)
    try:
        from backend import api, ocr_engine, rules_engine, validator, database, models, utils
        from backend.database import init_database, get_db_connection
        from backend.models import ReceiptData, LineItem, ValidationResult
        from backend.utils import normalize_price_string, extract_date, detect_currency
        print("[OK] All backend imports successful\n")
        return True
    except Exception as e:
        print(f"[FAIL] Import error: {e}\n")
        return False

def test_utils():
    """Test utility functions."""
    print("=" * 60)
    print("TEST 2: Utility Functions")
    print("=" * 60)
    from backend.utils import normalize_price_string, extract_date, detect_currency
    
    # Test price normalization
    price_tests = [
        ("1,200.50", 1200.5),
        ("1200/=", 1200.0),
        ("KES 500", 500.0),
    ]
    
    all_passed = True
    for price_str, expected in price_tests:
        result = normalize_price_string(price_str)
        if result == expected:
            print(f"[OK] Price: '{price_str}' -> {result}")
        else:
            print(f"[FAIL] Price: '{price_str}' -> {result} (expected {expected})")
            all_passed = False
    
    # Test date extraction
    date_tests = [
        ("15/01/2024", "2024-01-15"),
        ("2024-01-15", "2024-01-15"),
    ]
    
    for date_str, expected in date_tests:
        result = extract_date(date_str)
        if result == expected:
            print(f"[OK] Date: '{date_str}' -> {result}")
        else:
            print(f"[FAIL] Date: '{date_str}' -> {result} (expected {expected})")
            all_passed = False
    
    # Test currency detection
    currency_tests = [
        ("Total: KES 500", "KES"),
        ("Amount: USD 100", "USD"),
    ]
    
    for text, expected in currency_tests:
        result = detect_currency(text)
        if result == expected:
            print(f"[OK] Currency: '{text}' -> {result}")
        else:
            print(f"[FAIL] Currency: '{text}' -> {result} (expected {expected})")
            all_passed = False
    
    print()
    return all_passed

def test_api():
    """Test API endpoints."""
    print("=" * 60)
    print("TEST 3: API Endpoints")
    print("=" * 60)
    try:
        from backend.api import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health
        response = client.get("/health")
        if response.status_code == 200:
            print("[OK] GET /health -> 200")
        else:
            print(f"[FAIL] GET /health -> {response.status_code}")
            return False
        
        # Test receipts
        response = client.get("/receipts")
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] GET /receipts -> 200 (found {data['count']} receipts)")
        else:
            print(f"[FAIL] GET /receipts -> {response.status_code}")
            return False
        
        # Test stats
        response = client.get("/stats")
        if response.status_code == 200:
            data = response.json()
            if "trust_score" in data and "data" in data:
                print("[OK] GET /stats -> 200 (with trust_score)")
            else:
                print("[FAIL] GET /stats missing required fields")
                return False
        else:
            print(f"[FAIL] GET /stats -> {response.status_code}")
            return False
        
        print()
        return True
    except Exception as e:
        print(f"[FAIL] API test error: {e}\n")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AFRILENS AI - COMPREHENSIVE TEST SUITE")
    print("=" * 60 + "\n")
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Utils", test_utils()))
    results.append(("API", test_api()))
    
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("[SUCCESS] All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("[FAILURE] Some tests failed")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
