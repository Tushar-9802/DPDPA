#!/usr/bin/env python3
"""
CRITICAL DATABASE FIX
Updates Rule 9 obligation_type from 'children' to 'notice'

Run this BEFORE re-running assessments!
"""

import sqlite3
from pathlib import Path
import sys

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import DB_PATH

def fix_rule_9_tagging():
    """Fix Rule 9 obligation type"""
    
    print("="*70)
    print("DATABASE FIX: Rule 9 Obligation Type")
    print("="*70)
    print()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check current state
    print("BEFORE FIX:")
    print("-"*70)
    cursor.execute("""
        SELECT rule_number, obligation_type, COUNT(*) as count
        FROM requirements
        WHERE rule_number LIKE 'Rule 9%'
        GROUP BY rule_number, obligation_type
        ORDER BY rule_number
    """)
    
    before_results = cursor.fetchall()
    for row in before_results:
        print(f"  {row[0]:20} {row[1]:15} ({row[2]} requirements)")
    print()
    
    # Apply fix
    print("APPLYING FIX...")
    print("-"*70)
    cursor.execute("""
        UPDATE requirements
        SET obligation_type = 'notice'
        WHERE rule_number LIKE 'Rule 9%'
          AND obligation_type = 'children'
    """)
    
    rows_updated = cursor.rowcount
    print(f"  ✓ Updated {rows_updated} requirements")
    print()
    
    conn.commit()
    
    # Verify fix
    print("AFTER FIX:")
    print("-"*70)
    cursor.execute("""
        SELECT rule_number, obligation_type, COUNT(*) as count
        FROM requirements
        WHERE rule_number LIKE 'Rule 9%'
        GROUP BY rule_number, obligation_type
        ORDER BY rule_number
    """)
    
    after_results = cursor.fetchall()
    for row in after_results:
        print(f"  {row[0]:20} {row[1]:15} ({row[2]} requirements)")
    print()
    
    # Verify universal requirements count
    print("VERIFICATION:")
    print("-"*70)
    cursor.execute("""
        SELECT obligation_type, COUNT(*) as count
        FROM requirements
        WHERE obligation_type IN ('notice', 'security', 'breach', 'rights')
          AND is_sdf_specific = 0
        GROUP BY obligation_type
        ORDER BY count DESC
    """)
    
    print("  Universal requirements by type:")
    total_universal = 0
    for row in cursor.fetchall():
        print(f"    {row[0]:15} : {row[1]:3} requirements")
        total_universal += row[1]
    
    print(f"    {'TOTAL':15} : {total_universal:3} requirements")
    print()
    
    # Check for any children requirements in universal
    cursor.execute("""
        SELECT rule_number, obligation_type
        FROM requirements
        WHERE obligation_type = 'children'
          AND rule_number LIKE 'Rule 9%'
    """)
    
    wrong_tags = cursor.fetchall()
    if wrong_tags:
        print("  ⚠️  WARNING: Still found Rule 9 with 'children' tag:")
        for row in wrong_tags:
            print(f"    {row[0]} → {row[1]}")
    else:
        print("  ✓ No Rule 9 requirements tagged as 'children'")
    
    print()
    print("="*70)
    if rows_updated > 0:
        print("✅ FIX APPLIED SUCCESSFULLY")
    else:
        print("ℹ️  NO CHANGES NEEDED (already fixed)")
    print("="*70)
    print()
    
    conn.close()
    
    return rows_updated > 0

if __name__ == "__main__":
    fixed = fix_rule_9_tagging()
    
    if fixed:
        print("NEXT STEPS:")
        print("1. Re-run assessment: python src/assessment/run_assessment.py")
        print("2. Verify universal count is now 35 (not 36)")
        print()
    
    sys.exit(0 if fixed else 1)