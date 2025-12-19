"""
DIAGNOSTIC: Why is compliance score always 0.0%?
Check gap_analyzer.py scoring logic
"""

print("="*80)
print("COMPLIANCE SCORE DIAGNOSTIC")
print("="*80)
print()

# Simulate your "perfect" answers
test_answers = {
    'business_name': 'TechCorp India',
    'entity_type': 'startup',
    'user_count': 50000,
    'processes_children_data': False,
    'cross_border_transfers': False,
    'data_types': ['name', 'email'],
    'uses_ai': False,
    'annual_revenue': '1-10 crore',
    'has_processors': False,
    'current_security': ['encryption', 'access_control', 'logging', 'backups'],
    'has_breach_plan': True,
    'tracks_behavior': False,
    'targeted_advertising': False,
    'has_consent_mechanism': True,
    'has_grievance_system': True
}

print("TEST ANSWERS:")
print("-"*80)
for key, value in test_answers.items():
    print(f"  {key}: {value}")
print()

# Check what gap_analyzer.py looks for
print("EXPECTED SCORING LOGIC (from gap_analyzer.py):")
print("-"*80)
print()

completed = 0
total = 36  # Universal requirements

# 1. Security (Rule 6) - 9 requirements
security_measures = ['encryption', 'access_control', 'logging', 'backups']
has_all_security = all(m in test_answers.get('current_security', []) for m in security_measures)
print(f"1. Security Check:")
print(f"   Looking for: {security_measures}")
print(f"   Found: {test_answers.get('current_security', [])}")
print(f"   Has all 4? {has_all_security}")
if has_all_security:
    completed += 9
    print(f"   ✓ Completed: +9 (Rule 6)")
print()

# 2. Breach Plan (Rule 7) - 14 requirements
has_breach = test_answers.get('has_breach_plan', False)
print(f"2. Breach Plan Check:")
print(f"   Looking for: has_breach_plan = True")
print(f"   Found: {has_breach}")
if has_breach:
    completed += 14
    print(f"   ✓ Completed: +14 (Rule 7)")
print()

# 3. Consent (Rule 3) - 6 requirements
has_consent = test_answers.get('has_consent_mechanism', False)
print(f"3. Consent Check:")
print(f"   Looking for: has_consent_mechanism = True")
print(f"   Found: {has_consent}")
if has_consent:
    completed += 6
    print(f"   ✓ Completed: +6 (Rule 3)")
print()

# 4. Grievance (Rule 14) - 7 requirements
has_grievance = test_answers.get('has_grievance_system', False)
print(f"4. Grievance Check:")
print(f"   Looking for: has_grievance_system = True")
print(f"   Found: {has_grievance}")
if has_grievance:
    completed += 7
    print(f"   ✓ Completed: +7 (Rule 14)")
print()

# Calculate score
score = (completed / total) * 100

print("="*80)
print("EXPECTED RESULTS:")
print("-"*80)
print(f"  Completed: {completed}")
print(f"  Total: {total}")
print(f"  Score: {score:.1f}%")
print()

if score == 0:
    print("⚠️  SCORE IS 0% - Possible issues:")
    print("    1. Field names don't match between questionnaire and gap_analyzer")
    print("    2. Data not in extended_data format")
    print("    3. Logic checking wrong location in profile dict")
else:
    print(f"✓ SCORE SHOULD BE {score:.1f}%")
    print()
    print("If dashboard shows 0.0%, then:")
    print("  - gap_analyzer.py not reading answers correctly")
    print("  - OR answers stored in database in different format")
    print("  - OR extended_data not being passed to analyzer")

print()
print("="*80)
print("NEXT STEP: Check actual gap_analyzer.py code")
print("="*80)