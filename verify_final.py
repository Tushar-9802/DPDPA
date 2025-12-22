import sqlite3

conn = sqlite3.connect('data/processed/dpdpa_compliance.db')
cursor = conn.cursor()

print("="*70)
print("FINAL DATABASE STATE")
print("="*70)

# Total
cursor.execute('SELECT COUNT(*) FROM requirements')
total = cursor.fetchone()[0]
print(f'\n1. Total requirements: {total}')
print(f'   Expected: 45-50')
print(f'   Status: {"✅ CORRECT" if 45 <= total <= 50 else "⚠️ CHECK"}')

# Universal
cursor.execute("""
    SELECT COUNT(*) FROM requirements
    WHERE obligation_type IN ('notice', 'security', 'breach', 'rights')
      AND is_sdf_specific = 0
""")
universal = cursor.fetchone()[0]
print(f'\n2. Universal requirements: {universal}')
print(f'   Expected: 30-35')
print(f'   Status: {"✅ CORRECT" if 30 <= universal <= 35 else "⚠️ CHECK"}')

# Penalties
cursor.execute("""
    SELECT category_name, amount_inr/10000000 as crore
    FROM penalties
    ORDER BY amount_inr DESC
""")
print(f'\n3. Penalties:')
for cat, crore in cursor.fetchall():
    print(f'   {cat:30s} Rs. {crore:>6.0f} crore')

# Check specific penalty
cursor.execute("""
    SELECT amount_inr/10000000 
    FROM penalties 
    WHERE category_name='security_breach'
""")
sec_penalty = cursor.fetchone()[0]
print(f'\n4. Security breach penalty: Rs. {sec_penalty:.0f} crore')
print(f'   Expected: Rs. 250 crore')
print(f'   Status: {"✅ CORRECT" if sec_penalty == 250 else "❌ WRONG (should be 250)"}')

# Duplicates
cursor.execute("""
    SELECT COUNT(*) FROM (
        SELECT rule_number, requirement_text, COUNT(*) as cnt
        FROM requirements
        GROUP BY rule_number, requirement_text
        HAVING cnt > 1
    )
""")
dups = cursor.fetchone()[0]
print(f'\n5. Duplicate requirements: {dups}')
print(f'   Status: {"✅ NO DUPLICATES" if dups == 0 else "❌ DUPLICATES FOUND"}')

# By type
print(f'\n6. Requirements by type:')
cursor.execute("""
    SELECT obligation_type, COUNT(*) 
    FROM requirements 
    GROUP BY obligation_type 
    ORDER BY COUNT(*) DESC
""")
for otype, count in cursor.fetchall():
    pct = (count/total)*100 if total > 0 else 0
    print(f'   {otype:15s}: {count:3d} ({pct:5.1f}%)')

print('\n' + "="*70)
if 45 <= total <= 50 and 30 <= universal <= 35 and dups == 0 and sec_penalty == 250:
    print('✅ DATABASE IS PERFECT - READY TO DEPLOY!')
else:
    print('⚠️ SOME ISSUES DETECTED - SEE ABOVE')
print("="*70)

conn.close()
