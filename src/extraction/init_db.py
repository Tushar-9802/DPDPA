"""
DPDPA Compliance Dashboard - Database Initialization
Creates SQLite database with schema for compliance tracking

Tables:
1. requirements - Regulatory obligations from DPDP Rules 2025
2. penalties - Penalty categories from Section 33 of DPDP Act 2023
3. business_profiles - User business information
4. requirement_mappings - Business-to-requirement matching logic
5. compliance_status - Compliance progress tracking
6. schedule_references - Third Schedule data retention requirements
7. document_templates - Document template metadata
8. assessment_questions - Assessment questionnaire
"""

import sqlite3
from pathlib import Path
from datetime import datetime

# Database path
DB_PATH = Path(__file__).parent.parent.parent / "data" / "processed" / "dpdpa_compliance.db"

def init_database():
    """Initialize database with complete schema and pre-populated data"""
    
    # Ensure directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("DPDPA Compliance Database Initialization")
    print("=" * 70)
    print(f"\nDatabase location: {DB_PATH}\n")
    
    # =========================================================================
    # TABLE 1: REQUIREMENTS
    # =========================================================================
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_number TEXT NOT NULL,
            section_number TEXT,
            requirement_text TEXT NOT NULL,
            obligation_type TEXT NOT NULL,
            deadline DATE,
            penalty_category_id INTEGER,
            schedule_reference TEXT,
            is_sdf_specific BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (penalty_category_id) REFERENCES penalties(id)
        )
    """)
    print("✓ Created table: requirements")
    
    # =========================================================================
    # TABLE 2: PENALTIES (Section 33 of DPDP Act 2023)
    # =========================================================================
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penalties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL,
            amount_inr INTEGER NOT NULL,
            section_reference TEXT
        )
    """)
    print("✓ Created table: penalties")
    
    # Pre-populate penalties (Section 33 amounts in RUPEES)
    penalties_data = [
        ("security_breach", 25_000_000_000, "Section 33(1)"),        # ₹250 crore
        ("breach_notification", 20_000_000_000, "Section 33(2)"),    # ₹200 crore
        ("children_data", 20_000_000_000, "Section 33(3)"),          # ₹200 crore
        ("sdf_obligations", 15_000_000_000, "Section 33(4)"),        # ₹150 crore
        ("general_violations", 5_000_000_000, "Section 33(5)"),      # ₹50 crore
        ("data_principal_duties", 10_000, "Section 33(6)")           # ₹10,000
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO penalties (category_name, amount_inr, section_reference)
        VALUES (?, ?, ?)
    """, penalties_data)
    
    print(f"✓ Pre-populated penalties: {len(penalties_data)} categories")
    
    # =========================================================================
    # TABLE 3: BUSINESS PROFILES
    # =========================================================================
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_profiles (
        business_id TEXT PRIMARY KEY,
        business_name TEXT NOT NULL,
        business_address TEXT,
        business_email TEXT,
        business_phone TEXT,
        entity_type TEXT NOT NULL,
        user_count INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        extended_data TEXT,
        assessment_score REAL
    )
    """)
    print("✓ Created table: business_profiles")
    
    # =========================================================================
    # TABLE 4: REQUIREMENT MAPPINGS
    # =========================================================================
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requirement_mappings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_id INTEGER NOT NULL,
            trigger_condition TEXT,
            priority_weight REAL DEFAULT 1.0,
            FOREIGN KEY (requirement_id) REFERENCES requirements(id)
        )
    """)
    print("✓ Created table: requirement_mappings")
    
    # =========================================================================
    # TABLE 5: COMPLIANCE STATUS
    # =========================================================================
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compliance_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_profile_id INTEGER NOT NULL,
            requirement_id INTEGER NOT NULL,
            status TEXT DEFAULT 'not_started',
            completion_date DATE,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (business_profile_id) REFERENCES business_profiles(id),
            FOREIGN KEY (requirement_id) REFERENCES requirements(id)
        )
    """)
    print("✓ Created table: compliance_status")
    
    # =========================================================================
    # TABLE 6: SCHEDULE REFERENCES (Third Schedule)
    # =========================================================================
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule_references (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_name TEXT NOT NULL,
            entity_class TEXT NOT NULL,
            threshold_users INTEGER,
            retention_period_days INTEGER,
            specific_requirements TEXT
        )
    """)
    print("✓ Created table: schedule_references")
    
    # Pre-populate Third Schedule data
    third_schedule_data = [
        ("Third Schedule", "ecommerce", 20_000_000, 1095, 
         "Must maintain logs of significant data processing activities"),
        ("Third Schedule", "social_media", 20_000_000, 1095, 
         "Must maintain logs of significant data processing activities"),
        ("Third Schedule", "gaming", 5_000_000, 1095, 
         "Must maintain logs of significant data processing activities")
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO schedule_references 
        (schedule_name, entity_class, threshold_users, retention_period_days, specific_requirements)
        VALUES (?, ?, ?, ?, ?)
    """, third_schedule_data)
    
    print(f"✓ Pre-populated Third Schedule: {len(third_schedule_data)} entity classes")
    
    # =========================================================================
    # TABLE 7: DOCUMENT TEMPLATES
    # =========================================================================
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_name TEXT NOT NULL,
            template_type TEXT,
            file_path TEXT,
            rule_references TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created table: document_templates")
    
    # =========================================================================
    # TABLE 8: ASSESSMENT QUESTIONS
    # =========================================================================
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            question_type TEXT NOT NULL,
            options TEXT,
            maps_to_field TEXT,
            display_order INTEGER
        )
    """)
    print("✓ Created table: assessment_questions")
    
    # =========================================================================
    # COMMIT AND VERIFY
    # =========================================================================
    
    conn.commit()
    
    # Verify tables created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\n{'=' * 70}")
    print("DATABASE INITIALIZATION COMPLETE")
    print(f"{'=' * 70}")
    print(f"\nTables created: {len(tables)}")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]:30s} ({count} rows)")
    
    # Verify penalties
    cursor.execute("SELECT category_name, amount_inr FROM penalties ORDER BY amount_inr DESC")
    penalties = cursor.fetchall()
    
    print(f"\n{'=' * 70}")
    print("PENALTY CATEGORIES (Section 33)")
    print(f"{'=' * 70}")
    for category, amount in penalties:
        amount_crore = amount / 10_000_000
        print(f"  {category:30s} ₹{amount_crore:>8.0f} crore (₹{amount:,})")
    
    print(f"\n{'=' * 70}")
    print("✓ Database ready for use")
    print(f"{'=' * 70}\n")
    
    conn.close()


if __name__ == "__main__":
    init_database()