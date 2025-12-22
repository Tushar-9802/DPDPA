import sqlite3

DB_PATH = "data/processed/dpdpa_compliance.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("="*70)
print("FIXING PENALTY AMOUNTS (Divide by 10)")
print("="*70)
print()

# Show before
print("BEFORE:")
cursor.execute("SELECT category_name, amount_inr/10000000 as crore FROM penalties ORDER BY amount_inr DESC")
for cat, crore in cursor.fetchall():
    print(f"  {cat:30s} ₹{crore:>6.0f} crore")
print()

# Fix: divide by 10
cursor.execute("UPDATE penalties SET amount_inr = amount_inr / 10")
conn.commit()

# Show after
print("AFTER:")
cursor.execute("SELECT category_name, amount_inr/10000000 as crore FROM penalties ORDER BY amount_inr DESC")
for cat, crore in cursor.fetchall():
    print(f"  {cat:30s} ₹{crore:>6.0f} crore")
print()

# Verify against Act
print("VERIFICATION AGAINST DPDP ACT SECTION 33:")
print("-"*70)
expected = {
    'security_breach': 250,
    'breach_notification': 200,
    'children_data': 200,
    'sdf_obligations': 150,
    'general_violations': 50,
    'data_principal_duties': 0.001
}

cursor.execute("SELECT category_name, amount_inr/10000000 as crore FROM penalties")
all_correct = True
for cat, actual_crore in cursor.fetchall():
    expected_crore = expected.get(cat, 0)
    match = abs(actual_crore - expected_crore) < 0.01
    status = "✅" if match else "❌"
    print(f"  {status} {cat:30s} Expected: ₹{expected_crore:>6.1f}cr | Actual: ₹{actual_crore:>6.1f}cr")
    if not match:
        all_correct = False

print()
print("="*70)
if all_correct:
    print("✅ ALL PENALTIES NOW MATCH DPDP ACT SECTION 33")
else:
    print("❌ PENALTIES STILL INCORRECT")
print("="*70)

conn.close()