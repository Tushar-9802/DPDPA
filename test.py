import sys
import os
from pathlib import Path
import sqlite3
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Test results storage
test_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_test(name, status, message=""):
    """Print test result"""
    if status == "PASS":
        symbol = "✅"
        test_results["passed"].append(name)
    elif status == "FAIL":
        symbol = "❌"
        test_results["failed"].append(name)
    else:  # WARNING
        symbol = "⚠️"
        test_results["warnings"].append(name)
    
    print(f"{symbol} {name:50s} [{status}]")
    if message:
        print(f"   → {message}")

# ============================================================================
# TEST 1: FOLDER STRUCTURE
# ============================================================================

print_header("TEST 1: FOLDER STRUCTURE")

folders_to_check = [
    "config",
    "data",
    "data/raw",
    "data/processed",
    "data/cache",
    "src",
    "src/extraction",
    "src/assessment",
    "src/documents",
    "src/dashboard",
    "src/dashboard/pages",
    "src/dashboard/components",
    "src/utils",
    "templates",
    "templates/docx",
    "templates/pdf",
    "tests",
    "tests/unit",
    "tests/integration",
    "tests/fixtures",
    "docs",
    ".streamlit"
]

for folder in folders_to_check:
    folder_path = project_root / folder
    if folder_path.exists() and folder_path.is_dir():
        print_test(f"Folder: {folder}", "PASS")
    else:
        print_test(f"Folder: {folder}", "FAIL", "Folder does not exist")

# ============================================================================
# TEST 2: __init__.py FILES
# ============================================================================

print_header("TEST 2: PYTHON PACKAGE STRUCTURE")

init_files_to_check = [
    "config/__init__.py",
    "data/__init__.py",
    "src/__init__.py",
    "src/extraction/__init__.py",
    "src/assessment/__init__.py",
    "src/documents/__init__.py",
    "src/dashboard/__init__.py",
    "src/dashboard/pages/__init__.py",
    "src/dashboard/components/__init__.py",
    "src/utils/__init__.py",
    "tests/__init__.py",
    "tests/unit/__init__.py",
    "tests/integration/__init__.py",
    "tests/fixtures/__init__.py"
]

for init_file in init_files_to_check:
    file_path = project_root / init_file
    if file_path.exists() and file_path.is_file():
        print_test(f"__init__.py: {init_file}", "PASS")
    else:
        print_test(f"__init__.py: {init_file}", "FAIL", "File does not exist")

# ============================================================================
# TEST 3: CRITICAL FILES
# ============================================================================

print_header("TEST 3: CRITICAL FILES")

critical_files = [
    "config/config.py",
    "src/extraction/init_db.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
    "LICENSE"
]

for file in critical_files:
    file_path = project_root / file
    if file_path.exists() and file_path.is_file():
        size = file_path.stat().st_size
        print_test(f"File: {file}", "PASS", f"{size} bytes")
    else:
        print_test(f"File: {file}", "FAIL", "File does not exist")

# ============================================================================
# TEST 4: CONFIGURATION IMPORTS
# ============================================================================

print_header("TEST 4: CONFIGURATION MODULE")

try:
    from config.config import (
        APP_TITLE,
        APP_ICON,
        VERSION,
        DPDP_RULES_2025_URL,
        DPDP_ACT_2023_URL,
        RULES_NOTIFICATION_DATE,
        CONSENT_MANAGER_DEADLINE,
        FULL_COMPLIANCE_DEADLINE,
        THIRD_SCHEDULE_THRESHOLDS,
        PENALTY_AMOUNTS,
        DB_PATH,
        LEGAL_DISCLAIMER
    )
    print_test("Import config.config", "PASS", "All constants imported successfully")
    
    # Verify key constants
    if isinstance(APP_TITLE, str) and len(APP_TITLE) > 0:
        print_test("APP_TITLE constant", "PASS", f"Value: {APP_TITLE}")
    else:
        print_test("APP_TITLE constant", "FAIL", "Invalid or empty")
    
    if isinstance(DPDP_RULES_2025_URL, str) and DPDP_RULES_2025_URL.startswith("http"):
        print_test("DPDP_RULES_2025_URL", "PASS", f"Value: {DPDP_RULES_2025_URL[:50]}...")
    else:
        print_test("DPDP_RULES_2025_URL", "FAIL", "Invalid URL")
    
    if isinstance(FULL_COMPLIANCE_DEADLINE, datetime):
        days_remaining = (FULL_COMPLIANCE_DEADLINE - datetime.now()).days
        print_test("FULL_COMPLIANCE_DEADLINE", "PASS", 
                   f"{FULL_COMPLIANCE_DEADLINE.date()} ({days_remaining} days remaining)")
    else:
        print_test("FULL_COMPLIANCE_DEADLINE", "FAIL", "Not a datetime object")
    
    if isinstance(THIRD_SCHEDULE_THRESHOLDS, dict) and len(THIRD_SCHEDULE_THRESHOLDS) > 0:
        print_test("THIRD_SCHEDULE_THRESHOLDS", "PASS", 
                   f"{len(THIRD_SCHEDULE_THRESHOLDS)} thresholds defined")
    else:
        print_test("THIRD_SCHEDULE_THRESHOLDS", "FAIL", "Invalid or empty")
    
    if isinstance(PENALTY_AMOUNTS, dict) and len(PENALTY_AMOUNTS) == 6:
        print_test("PENALTY_AMOUNTS", "PASS", f"6 penalty categories defined")
    else:
        print_test("PENALTY_AMOUNTS", "WARNING", f"Expected 6 categories, got {len(PENALTY_AMOUNTS)}")
    
except ImportError as e:
    print_test("Import config.config", "FAIL", f"Import error: {e}")
except Exception as e:
    print_test("Import config.config", "FAIL", f"Error: {e}")

# ============================================================================
# TEST 5: DATABASE
# ============================================================================

print_header("TEST 5: DATABASE")

# Check if database file exists
db_path = project_root / "data" / "processed" / "dpdpa_compliance.db"

if db_path.exists():
    print_test("Database file exists", "PASS", f"Location: {db_path}")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print_test("Database connection", "PASS", "Connected successfully")
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = [
            "requirements",
            "penalties",
            "business_profiles",
            "requirement_mappings",
            "compliance_status",
            "schedule_references",
            "document_templates",
            "assessment_questions"
        ]
        
        for table in expected_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print_test(f"Table: {table}", "PASS", f"{count} rows")
            else:
                print_test(f"Table: {table}", "FAIL", "Table does not exist")
        
        # Verify pre-populated data
        cursor.execute("SELECT COUNT(*) FROM penalties")
        penalty_count = cursor.fetchone()[0]
        if penalty_count == 6:
            print_test("Penalties pre-populated", "PASS", "6 penalty categories")
        else:
            print_test("Penalties pre-populated", "WARNING", 
                      f"Expected 6, got {penalty_count}")
        
        cursor.execute("SELECT COUNT(*) FROM schedule_references")
        schedule_count = cursor.fetchone()[0]
        if schedule_count == 3:
            print_test("Third Schedule pre-populated", "PASS", "3 entity classes")
        else:
            print_test("Third Schedule pre-populated", "WARNING", 
                      f"Expected 3, got {schedule_count}")
        
        # Check penalty amounts
        cursor.execute("SELECT category_name, amount_inr FROM penalties ORDER BY amount_inr DESC")
        penalties = cursor.fetchall()
        
        if penalties and penalties[0][1] == 25_000_000_000:
            print_test("Max penalty (₹250 crore)", "PASS", 
                      f"Category: {penalties[0][0]}")
        else:
            print_test("Max penalty verification", "FAIL", "Incorrect amount")
        
        conn.close()
        print_test("Database closed", "PASS")
        
    except sqlite3.Error as e:
        print_test("Database operations", "FAIL", f"SQLite error: {e}")
    except Exception as e:
        print_test("Database operations", "FAIL", f"Error: {e}")
else:
    print_test("Database file exists", "FAIL", 
              "Run: python src/extraction/init_db.py")

# ============================================================================
# TEST 6: DEPENDENCIES
# ============================================================================

print_header("TEST 6: PYTHON DEPENDENCIES")

required_packages = [
    ("streamlit", "1.40.2"),
    ("PyMuPDF", "1.24.14"),
    ("pdfplumber", "0.11.4"),
    ("pandas", "2.2.3"),
    ("numpy", "2.1.3"),
    ("python-docx", "1.1.2"),
    ("reportlab", "4.2.5"),
    ("requests", "2.32.3"),
]

for package, expected_version in required_packages:
    try:
        if package == "PyMuPDF":
            import fitz
            module = fitz
            package_name = "PyMuPDF (fitz)"
        elif package == "python-docx":
            import docx
            module = docx
            package_name = "python-docx (docx)"
        else:
            module = __import__(package)
            package_name = package
        
        # Try to get version
        version = getattr(module, '__version__', 'unknown')
        
        if version == expected_version or version == 'unknown':
            print_test(f"Package: {package_name}", "PASS", f"Version: {version}")
        else:
            print_test(f"Package: {package_name}", "WARNING", 
                      f"Expected {expected_version}, got {version}")
    
    except ImportError:
        print_test(f"Package: {package}", "FAIL", "Not installed")
    except Exception as e:
        print_test(f"Package: {package}", "WARNING", f"Error: {e}")

# ============================================================================
# TEST 7: .gitignore VALIDATION
# ============================================================================

print_header("TEST 7: .gitignore VALIDATION")

gitignore_path = project_root / ".gitignore"

if gitignore_path.exists():
    with open(gitignore_path, 'r') as f:
        gitignore_content = f.read()
    
    required_patterns = [
        ("venv/", "Virtual environment excluded"),
        ("*.db", "Database files excluded"),
        ("*.pdf", "PDF files excluded"),
        ("__pycache__/", "Python cache excluded"),
        (".env", "Environment files excluded"),
        ("*.log", "Log files excluded"),
        ("app.py", "Work-in-progress app.py excluded")
    ]
    
    for pattern, description in required_patterns:
        if pattern in gitignore_content:
            print_test(f".gitignore: {pattern}", "PASS", description)
        else:
            print_test(f".gitignore: {pattern}", "WARNING", 
                      f"Pattern not found: {description}")
else:
    print_test(".gitignore exists", "FAIL", "File not found")

# ============================================================================
# TEST SUMMARY
# ============================================================================

print_header("TEST SUMMARY")

total_tests = len(test_results["passed"]) + len(test_results["failed"]) + len(test_results["warnings"])

print(f"\n📊 Results:")
print(f"   ✅ Passed:   {len(test_results['passed']):3d} / {total_tests}")
print(f"   ❌ Failed:   {len(test_results['failed']):3d} / {total_tests}")
print(f"   ⚠️  Warnings: {len(test_results['warnings']):3d} / {total_tests}")

if len(test_results['failed']) == 0:
    print("\n" + "=" * 70)
    print("  ✅ ALL CRITICAL TESTS PASSED - READY FOR GITHUB PUSH")
    print("=" * 70)
    exit_code = 0
elif len(test_results['failed']) <= 3:
    print("\n" + "=" * 70)
    print("  ⚠️  MINOR ISSUES DETECTED - REVIEW FAILURES BEFORE PUSH")
    print("=" * 70)
    exit_code = 1
else:
    print("\n" + "=" * 70)
    print("  ❌ MULTIPLE FAILURES - FIX ISSUES BEFORE PUSH")
    print("=" * 70)
    exit_code = 2

print("\nFailed tests:")
if test_results['failed']:
    for test in test_results['failed']:
        print(f"  ❌ {test}")
else:
    print("  None")

print("\nWarnings:")
if test_results['warnings']:
    for test in test_results['warnings']:
        print(f"  ⚠️  {test}")
else:
    print("  None")

print("\n" + "=" * 70)
sys.exit(exit_code)