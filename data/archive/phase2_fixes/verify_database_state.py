#!/usr/bin/env python3
"""
Verify current database state - what's wrong with Rule 9?
"""

import sqlite3
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import DB_PATH

def verify_database():
    """Check current state of requirements"""
    
    print("="*80)
    print("DATABASE STATE VERIFICATION")
    print("="*80)
    print()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check ALL Rule 9 requirements
    print("1. ALL RULE 9 REQUIREMENTS:")
    print("-"*80)
    cursor.execute("""
        SELECT id, rule_number, obligation_type, 
               SUBSTR(requirement_text, 1, 60) as text_preview
        FROM requirements
        WHERE rule_number LIKE 'Rule 9%'
        ORDER BY rule_number
    """)
    
    rule9_reqs = cursor.fetchall()
    if rule9_reqs:
        for row in rule9_reqs:
            print(f"  ID {row[0]:3d}: {row[1]:20s} → {row[2]:15s} | {row[3]}...")
    else:
        print("  NO Rule 9 requirements found!")
    print()
    
    # Check universal requirements query (what matcher uses)
    print("2. UNIVERSAL REQUIREMENTS QUERY:")
    print("-"*80)
    cursor.execute("""
        SELECT obligation_type, COUNT(*) as count
        FROM requirements
        WHERE obligation_type IN ('notice', 'security', 'breach', 'rights')
          AND is_sdf_specific = 0
        GROUP BY obligation_type
        ORDER BY obligation_type
    """)
    
    print("  Query: obligation_type IN ('notice', 'security', 'breach', 'rights')")
    print("         AND is_sdf_specific = 0")
    print()
    total_universal = 0
    for row in cursor.fetchall():
        print(f"  {row[0]:15s}: {row[1]:3d} requirements")
        total_universal += row[1]
    print(f"  {'TOTAL':15s}: {total_universal:3d} requirements")
    print()
    
    # Check if there's a Rule 9 in universal
    print("3. IS RULE 9 IN UNIVERSAL?")
    print("-"*80)
    cursor.execute("""
        SELECT id, rule_number, obligation_type
        FROM requirements
        WHERE rule_number LIKE 'Rule 9%'
          AND obligation_type IN ('notice', 'security', 'breach', 'rights')
          AND is_sdf_specific = 0
    """)
    
    in_universal = cursor.fetchall()
    if in_universal:
        print("  ✓ YES - Rule 9 IS in universal:")
        for row in in_universal:
            print(f"    ID {row[0]:3d}: {row[1]:20s} → {row[2]:15s}")
    else:
        print("  ✗ NO - Rule 9 is NOT in universal")
    print()
    
    # Check children requirements
    print("4. CHILDREN REQUIREMENTS:")
    print("-"*80)
    cursor.execute("""
        SELECT rule_number, COUNT(*) as count
        FROM requirements
        WHERE obligation_type = 'children'
        GROUP BY rule_number
        ORDER BY rule_number
    """)
    
    children_by_rule = cursor.fetchall()
    total_children = 0
    for row in children_by_rule:
        print(f"  {row[0]:20s}: {row[1]:3d} requirements")
        total_children += row[1]
    print(f"  {'TOTAL':20s}: {total_children:3d} requirements")
    print()
    
    # The mystery: Check if there's ANOTHER Rule 9 somewhere
    print("5. ALL REQUIREMENTS WITH 'Rule 9' OR 'contact' IN TEXT:")
    print("-"*80)
    cursor.execute("""
        SELECT id, rule_number, obligation_type, is_sdf_specific,
               SUBSTR(requirement_text, 1, 80) as text_preview
        FROM requirements
        WHERE rule_number LIKE '%9%'
           OR requirement_text LIKE '%contact%information%'
        ORDER BY rule_number
    """)
    
    all_rule9_like = cursor.fetchall()
    for row in all_rule9_like:
        sdf_flag = "[SDF]" if row[3] else ""
        print(f"  ID {row[0]:3d}: {row[1]:20s} → {row[2]:15s} {sdf_flag}")
        print(f"         {row[4]}...")
        print()
    
    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Rule 9 requirements: {len(rule9_reqs)}")
    print(f"Rule 9 in universal query: {len(in_universal)}")
    print(f"Total universal (from query): {total_universal}")
    print(f"Total children requirements: {total_children}")
    print()
    
    if total_universal == 36:
        print("⚠️  Universal count is 36 - SOMETHING IS WRONG")
        print()
        print("HYPOTHESIS:")
        print("  - Matcher might have OLD code still using 'OR rule_number LIKE Rule 9%'")
        print("  - OR there's a different requirement being counted")
        print()
    
    conn.close()

if __name__ == "__main__":
    verify_database()