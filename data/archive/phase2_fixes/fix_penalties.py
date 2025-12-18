#!/usr/bin/env python3
"""
Fix penalty amounts in database - they are 10x too high
Act Schedule: ₹250 crore max, not ₹2500 crore
"""

import sqlite3
import sys

def fix_penalties(db_path):
    """Divide all penalty amounts by 10 to match Act Schedule"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("="*80)
    print("FIXING PENALTY AMOUNTS - 10X ERROR")
    print("="*80)
    print()
    
    # Show current (wrong) values
    print("BEFORE FIX:")
    print("-"*80)
    cursor.execute('''
        SELECT category_name, amount_inr, amount_inr/10000000 as crore
        FROM penalties
        ORDER BY amount_inr DESC
    ''')
    
    for row in cursor.fetchall():
        print(f"  {row[0]:25} ₹{row[1]:>15,} (₹{row[2]:>6.0f} crore)")
    print()
    
    # Fix: divide by 10
    print("APPLYING FIX: Dividing all amounts by 10...")
    cursor.execute('UPDATE penalties SET amount_inr = amount_inr / 10')
    conn.commit()
    print("✓ Updated\n")
    
    # Show corrected values
    print("AFTER FIX:")
    print("-"*80)
    cursor.execute('''
        SELECT category_name, amount_inr, amount_inr/10000000 as crore
        FROM penalties
        ORDER BY amount_inr DESC
    ''')
    
    for row in cursor.fetchall():
        print(f"  {row[0]:25} ₹{row[1]:>15,} (₹{row[2]:>6.0f} crore)")
    print()
    
    # Verify against Act Schedule
    print("VERIFICATION AGAINST ACT SCHEDULE:")
    print("-"*80)
    
    act_penalties = {
        'security_breach': 250,  # crore
        'breach_notification': 200,
        'children_data': 200,
        'sdf_obligations': 150,
        'general_violations': 50,
        'data_principal_duties': 0.001  # ₹10,000
    }
    
    cursor.execute('SELECT category_name, amount_inr FROM penalties')
    all_correct = True
    
    for row in cursor.fetchall():
        name = row[0]
        actual_crore = row[1] / 10_000_000
        expected_crore = act_penalties.get(name, 0)
        
        status = "✓" if abs(actual_crore - expected_crore) < 0.01 else "❌"
        if status == "❌":
            all_correct = False
            
        print(f"  {status} {name:25} Expected: ₹{expected_crore:>6.1f}cr | Actual: ₹{actual_crore:>6.1f}cr")
    
    print()
    print("="*80)
    if all_correct:
        print("✅ ALL PENALTIES NOW MATCH ACT SCHEDULE")
    else:
        print("❌ SOME PENALTIES STILL INCORRECT")
    print("="*80)
    print()
    
    conn.close()
    return all_correct

if __name__ == '__main__':
    db_path = 'data/processed/dpdpa_compliance.db'
    
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    success = fix_penalties(db_path)
    sys.exit(0 if success else 1)