"""
Migration: Add contact fields to business_profiles table
Run this ONCE if you have existing database with data
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'dpdpa_compliance.db'

def migrate():
    """Add address, email, phone columns to business_profiles"""
    
    if not DB_PATH.exists():
        print("No existing database found. Run init_db.py instead.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(business_profiles)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'business_address' in columns:
        print("Migration already applied. Contact fields exist.")
        conn.close()
        return
    
    print("Adding contact fields to business_profiles table...")
    
    try:
        # Add new columns
        cursor.execute("ALTER TABLE business_profiles ADD COLUMN business_address TEXT")
        cursor.execute("ALTER TABLE business_profiles ADD COLUMN business_email TEXT")
        cursor.execute("ALTER TABLE business_profiles ADD COLUMN business_phone TEXT")
        
        conn.commit()
        print("✓ Successfully added contact fields")
        print("  - business_address")
        print("  - business_email")
        print("  - business_phone")
        
    except sqlite3.Error as e:
        print(f"✗ Migration failed: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()