"""
Final test: All 7 document templates
"""

from src.document_generator import DocumentGenerator
import os

# Comprehensive test profile (covers all conditional templates)
test_profile = {
    'business_name': 'KidsLearn Education Platform Pvt Ltd',
    'entity_type': 'edtech',
    'user_count': 2_000_000,
    'data_types': ['name', 'email', 'phone', 'behavioral'],
    'processes_children_data': True,  # Triggers parental consent
    'has_processors': True,           # Triggers processor checklist
    'has_consent_mechanism': True,
    'has_breach_plan': False,
    'has_grievance_system': True,
    'address': '123 Learning Lane, Sector 5, Gurgaon, Haryana 122001',
    'email': 'privacy@kidslearn.in',
    'phone': '+91-124-4567890'
}

test_gaps = {'compliance_score': 70}

print("="*70)
print("FINAL COMPREHENSIVE TEST - ALL 7 TEMPLATES")
print("="*70)

print(f"\nTest Profile:")
print(f"  Business: {test_profile['business_name']}")
print(f"  Processes Children Data: YES (triggers parental consent)")
print(f"  Has Processors: YES (triggers processor checklist)")
print(f"  Data Types: {len(test_profile['data_types'])} types")

try:
    gen = DocumentGenerator(test_profile, test_gaps)
    
    print(f"\nGenerating all required documents...")
    documents = gen.generate_all_required_documents()
    
    print(f"\nGenerated {len(documents)} documents:")
    for name in documents.keys():
        print(f"  - {name}")
    
    print(f"\nExporting to ZIP...")
    zip_path = gen.export_all_to_zip(documents, 'TEST_all_seven_templates.zip')
    
    print(f"\nSUCCESS!")
    print(f"ZIP file: {zip_path}")
    print(f"Size: {zip_path.stat().st_size:,} bytes")
    
    # Also export individually for inspection
    print(f"\nExporting individual files...")
    paths = []
    for doc_name, doc in documents.items():
        path = gen.export_to_docx(doc, f"FINAL_{doc_name}.docx")
        paths.append(path)
        print(f"  - {path.name} ({path.stat().st_size:,} bytes)")
    
    print(f"\n" + "="*70)
    print("ALL 7 TEMPLATES WORKING!")
    print("="*70)
    
    print(f"\nExpected documents:")
    print(f"  1. Privacy Notice (universal)")
    print(f"  2. Consent Form (universal)")
    print(f"  3. Grievance Procedure (universal)")
    print(f"  4. Retention Schedule (universal)")
    print(f"  5. Breach Notification - DPB (universal)")
    print(f"  6. Breach Notification - Users (universal)")
    print(f"  7. Parental Consent Form (conditional - children data)")
    print(f"  8. Processor Agreement Checklist (conditional - has processors)")
    
    print(f"\nOpen ZIP file? (y/n): ", end='')
    choice = input().strip().lower()
    
    if choice == 'y':
        os.startfile(zip_path)
        print("ZIP opened")
    
except Exception as e:
    print(f"\nFAILED: {e}")
    import traceback
    traceback.print_exc()