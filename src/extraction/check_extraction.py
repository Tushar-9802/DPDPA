"""Quick script to check extraction results"""
import sqlite3
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import DB_PATH

def main():
    """Check extraction results"""
    print("=" * 70)
    print("EXTRACTION VERIFICATION REPORT")
    print("=" * 70)
    print()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check total unique requirements
    cursor.execute('SELECT COUNT(DISTINCT rule_number || requirement_text) FROM requirements')
    unique_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM requirements')
    total_count = cursor.fetchone()[0]
    duplicates = total_count - unique_count
    
    print("📊 REQUIREMENTS SUMMARY")
    print("-" * 70)
    print(f"  Total requirements in database: {total_count}")
    print(f"  Unique requirements:            {unique_count}")
    print(f"  Duplicates found:               {duplicates}")
    
    if duplicates == 0:
        print("  ✓ Status: No duplicates detected")
    else:
        print(f"  ⚠ Status: {duplicates} duplicate(s) found")
    print()

    # Check requirements by rule
    cursor.execute('''
        SELECT rule_number, COUNT(*) as count 
        FROM requirements 
        GROUP BY rule_number 
        ORDER BY CAST(SUBSTR(rule_number, 6) AS INTEGER)
    ''')
    rule_rows = cursor.fetchall()
    print(f"📋 REQUIREMENTS BY RULE ({len(rule_rows)} unique rule numbers)")
    print("-" * 70)
    for row in rule_rows:
        print(f"  {row[0]:30} : {row[1]:3} entry/entries")
    print()

    # Check Third Schedule
    cursor.execute('SELECT * FROM schedule_references WHERE schedule_name = ?', ('Third Schedule',))
    schedule_rows = cursor.fetchall()
    print("📅 THIRD SCHEDULE ENTRIES")
    print("-" * 70)
    print(f"  Total entries: {len(schedule_rows)}")
    print(f"  Expected:      3 (ecommerce, gaming, social_media)")
    
    if len(schedule_rows) == 3:
        print("  ✓ Status: Correct number of entries")
    else:
        print(f"  ⚠ Status: Expected 3, found {len(schedule_rows)}")
    print()
    
    print("  Details:")
    for row in schedule_rows:
        print(f"    • {row[2]:15} : {row[3]:>12,} users, {row[4]:>4} days retention")
    print()

    # Check for duplicate schedule entries
    cursor.execute('''
        SELECT entity_class, COUNT(*) as count 
        FROM schedule_references 
        WHERE schedule_name = 'Third Schedule'
        GROUP BY entity_class
        HAVING COUNT(*) > 1
    ''')
    duplicate_schedules = cursor.fetchall()
    if duplicate_schedules:
        print("⚠ DUPLICATE SCHEDULE ENTRIES DETECTED")
        print("-" * 70)
        for row in duplicate_schedules:
            print(f"  {row[0]:15} : {row[1]} entries (expected: 1)")
        print()

    # Sample requirement text
    cursor.execute('SELECT rule_number, requirement_text FROM requirements WHERE rule_number = ? LIMIT 1', ('Rule 6(1(a))',))
    sample = cursor.fetchone()
    if sample:
        print("📝 SAMPLE REQUIREMENT")
        print("-" * 70)
        print(f"  Rule: {sample[0]}")
        print(f"  Text: {sample[1][:200]}...")
        print()

    # Final summary
    print("=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)
    print(f"✓ Requirements: {unique_count} unique entries")
    print(f"✓ Third Schedule: {len(schedule_rows)} entries")
    if duplicates == 0 and len(schedule_rows) == 3:
        print("✓ All checks passed!")
    print()

    conn.close()

if __name__ == "__main__":
    main()

