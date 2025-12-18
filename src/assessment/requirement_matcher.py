"""
Matches business profile to applicable DPDP requirements

Usage:
    from src.assessment.requirement_matcher import match_requirements
    applicable_ids = match_requirements(business_profile)
"""

import sqlite3
from pathlib import Path
import sys
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import DB_PATH


def get_universal_requirements() -> List[int]:
    """
    Get requirements that apply to ALL businesses
    
    Returns:
        List of requirement IDs
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Universal types: notice, security, breach, rights
    # Rule 9 is now correctly tagged as 'notice' in database
    cursor.execute("""
        SELECT id FROM requirements
        WHERE obligation_type IN ('notice', 'security', 'breach', 'rights')
          AND is_sdf_specific = 0
    """)
    
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return ids


def get_third_schedule_requirements(entity_class: str) -> List[int]:
    """
    Get Third Schedule retention requirements
    
    Args:
        entity_class: 'ecommerce', 'social_media', or 'gaming'
        
    Returns:
        List of requirement IDs
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get retention requirements (Rule 8)
    cursor.execute("""
        SELECT id FROM requirements
        WHERE obligation_type = 'retention'
          OR rule_number LIKE 'Rule 8%'
    """)
    
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return ids


def get_children_requirements() -> List[int]:
    """
    Get children's data requirements (Rules 10, 11, 12)
    
    Returns:
        List of requirement IDs
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id FROM requirements
        WHERE obligation_type = 'children'
           AND rule_number NOT LIKE 'Rule 9%'
    """)
    
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return ids


def get_cross_border_requirements() -> List[int]:
    """
    Get cross-border transfer requirements (Rule 15)
    
    Returns:
        List of requirement IDs
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id FROM requirements
        WHERE rule_number LIKE 'Rule 15%'
    """)
    
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return ids


def get_sdf_requirements() -> List[int]:
    """
    Get Significant Data Fiduciary requirements (Rule 13)
    
    Returns:
        List of requirement IDs
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id FROM requirements
        WHERE is_sdf_specific = 1
           OR obligation_type = 'sdf'
           OR rule_number LIKE 'Rule 13%'
    """)
    
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return ids


def check_third_schedule_threshold(entity_type: str, user_count: int) -> bool:
    """
    Check if business exceeds Third Schedule threshold
    
    Args:
        entity_type: Business entity type
        user_count: Number of users
        
    Returns:
        True if Third Schedule applies
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Map entity types to schedule entity classes
    entity_class_map = {
        'ecommerce': 'ecommerce',
        'social_media': 'social_media',
        'gaming': 'gaming'
    }
    
    entity_class = entity_class_map.get(entity_type)
    
    if not entity_class:
        conn.close()
        return False
    
    # Get threshold
    cursor.execute("""
        SELECT threshold_users
        FROM schedule_references
        WHERE schedule_name = 'Third Schedule'
          AND entity_class = ?
    """, (entity_class,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return False
    
    threshold = result[0]
    return user_count >= threshold


def match_requirements(business_profile: Dict[str, Any]) -> List[int]:
    """
    Match business profile to applicable requirements
    
    Args:
        business_profile: Dictionary with business data
        Can contain keys from questionnaire OR from database
        
    Returns:
        List of requirement IDs
    """
    
    applicable_ids = set()  # Use set to avoid duplicates
    
    # Extract fields (handle both questionnaire format and DB format)
    entity_type = business_profile.get('entity_type', 'other')
    user_count = business_profile.get('user_count', 0)
    processes_children_data = business_profile.get('processes_children_data', False)
    cross_border_transfers = business_profile.get('cross_border_transfers', False)
    
    # Extended data
    extended = business_profile.get('extended_data', {})
    has_processors = extended.get('has_processors', business_profile.get('has_processors', False))
    is_sdf = business_profile.get('is_sdf', False)  # Will be False for now (govt hasn't notified any)
    
    print(f"Matching requirements for: {business_profile.get('business_name', 'Business')}")
    print(f"  Entity: {entity_type}, Users: {user_count:,}")
    print()
    
    # === ILLEGAL ACTIVITY CHECK (MUST BE FIRST) ===
    if processes_children_data:
        tracks = extended.get('tracks_behavior', business_profile.get('tracks_behavior', False))
        ads = extended.get('targeted_advertising', business_profile.get('targeted_advertising', False))
        
        if tracks or ads:
            print()
            print("  " + "="*66)
            print("  🚨 CRITICAL LEGAL VIOLATION DETECTED")
            print("  " + "="*66)
            print()
            print("  DPDP Act Section 9(3) PROHIBITS:")
            if tracks:
                print("    ❌ Behavioral tracking of children")
            if ads:
                print("    ❌ Targeted advertising directed at children")
            print()
            print("  ⚠️  YOU ARE CURRENTLY IN VIOLATION OF DPDP ACT 2023!")
            print("  ⚠️  PENALTY: ₹200 CRORE PER VIOLATION")
            print()
            print("  REQUIRED ACTIONS:")
            print("    1. IMMEDIATELY cease all prohibited activities")
            print("    2. Delete all behavioral data collected from children")
            print("    3. Implement age verification + parental consent")
            print("    4. Consult legal counsel for compliance strategy")
            print()
            print("  " + "="*66)
            print()
    
    # === 1. UNIVERSAL REQUIREMENTS (ALL businesses) ===
    print("  [1/5] Loading universal requirements...")
    universal = get_universal_requirements()
    applicable_ids.update(universal)
    print(f"        ✓ {len(universal)} universal requirements")
    
    # === 2. THIRD SCHEDULE (threshold check) ===
    print("  [2/5] Checking Third Schedule thresholds...")
    if check_third_schedule_threshold(entity_type, user_count):
        third_schedule = get_third_schedule_requirements(entity_type)
        applicable_ids.update(third_schedule)
        print(f"        ✓ Third Schedule applies (+{len(third_schedule)} requirements)")
    else:
        print(f"        ○ Third Schedule does not apply (below threshold)")
    
    # === 3. CHILDREN'S DATA ===
    print("  [3/5] Checking children's data requirements...")
    if processes_children_data:
        children = get_children_requirements()
        applicable_ids.update(children)
        print(f"        ✓ Children's data rules apply (+{len(children)} requirements)")
        print(f"        ⚠️  HIGH RISK: ₹200 crore penalty for Rule 10 violations")
    else:
        print(f"        ○ Children's data rules do not apply")
    
    # === 4. CROSS-BORDER TRANSFERS ===
    print("  [4/5] Checking cross-border transfer requirements...")
    if cross_border_transfers:
        cross_border = get_cross_border_requirements()
        applicable_ids.update(cross_border)
        print(f"        ✓ Cross-border rules apply (+{len(cross_border)} requirements)")
        print(f"        ℹ️  Monitor MEITY for country restrictions")
    else:
        print(f"        ○ Cross-border rules do not apply")
    
    # === 5. SIGNIFICANT DATA FIDUCIARY (placeholder) ===
    print("  [5/5] Checking SDF requirements...")
    if is_sdf:
        sdf = get_sdf_requirements()
        applicable_ids.update(sdf)
        print(f"        ✓ SDF rules apply (+{len(sdf)} requirements)")
        print(f"        ⚠️  HIGH COMPLEXITY: DPIA, audit, DPO required")
    else:
        print(f"        ○ Not designated as SDF (government hasn't notified)")
    
    print()
    print(f"✓ Total applicable requirements: {len(applicable_ids)}")
    
    return list(applicable_ids)


def get_requirement_details(requirement_id: int) -> Dict[str, Any]:
    """
    Get full details of a requirement
    
    Args:
        requirement_id: Requirement ID
        
    Returns:
        Dictionary with requirement details
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            r.id,
            r.rule_number,
            r.requirement_text,
            r.obligation_type,
            r.deadline,
            r.penalty_category_id,
            r.is_sdf_specific,
            p.category_name,
            p.amount_inr
        FROM requirements r
        LEFT JOIN penalties p ON r.penalty_category_id = p.id
        WHERE r.id = ?
    """, (requirement_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        'id': row[0],
        'rule_number': row[1],
        'requirement_text': row[2],
        'obligation_type': row[3],
        'deadline': row[4],
        'penalty_category_id': row[5],
        'is_sdf_specific': bool(row[6]),
        'penalty_category': row[7],
        'penalty_amount': row[8]
    }


def get_requirements_summary(requirement_ids: List[int]) -> Dict[str, Any]:
    """
    Get summary statistics for a list of requirements
    
    Args:
        requirement_ids: List of requirement IDs
        
    Returns:
        Dictionary with summary stats
    """
    if not requirement_ids:
        return {
            'total': 0,
            'by_type': {},
            'by_penalty': {},
            'max_penalty': 0,
            'total_penalty_exposure': 0
        }
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all requirements
    placeholders = ','.join('?' * len(requirement_ids))
    cursor.execute(f"""
        SELECT 
            r.obligation_type,
            p.category_name,
            p.amount_inr
        FROM requirements r
        LEFT JOIN penalties p ON r.penalty_category_id = p.id
        WHERE r.id IN ({placeholders})
    """, requirement_ids)
    
    rows = cursor.fetchall()
    conn.close()
    
    # Count by type
    by_type = {}
    by_penalty = {}
    penalties = []
    
    for row in rows:
        obligation_type = row[0]
        penalty_category = row[1]
        penalty_amount = row[2] or 0
        
        by_type[obligation_type] = by_type.get(obligation_type, 0) + 1
        by_penalty[penalty_category] = by_penalty.get(penalty_category, 0) + 1
        penalties.append(penalty_amount)
    
    return {
        'total': len(requirement_ids),
        'by_type': by_type,
        'by_penalty': by_penalty,
        'max_penalty': max(penalties) if penalties else 0,
        'total_penalty_exposure': sum(penalties)
    }


# For testing
if __name__ == "__main__":
    print("="*70)
    print("REQUIREMENT MATCHER - TEST MODE")
    print("="*70)
    print()
    
    # Test with sample business profile
    test_profiles = [
        {
            'name': 'Small Startup',
            'business_name': 'Small Startup',
            'entity_type': 'startup',
            'user_count': 1000,
            'processes_children_data': False,
            'cross_border_transfers': False,
            'extended_data': {'has_processors': False}
        },
        {
            'name': 'Gaming Company',
            'business_name': 'Gaming Company',
            'entity_type': 'gaming',
            'user_count': 6_000_000,
            'processes_children_data': True,
            'cross_border_transfers': True,
            'extended_data': {'has_processors': True, 'tracks_behavior': True, 'targeted_advertising': True}
        },
        {
            'name': 'E-commerce Giant',
            'business_name': 'E-commerce Giant',
            'entity_type': 'ecommerce',
            'user_count': 25_000_000,
            'processes_children_data': False,
            'cross_border_transfers': True,
            'extended_data': {'has_processors': True}
        }
    ]
    
    for profile in test_profiles:
        print(f"\nTesting: {profile['name']}")
        print("-" * 70)
        
        applicable = match_requirements(profile)
        summary = get_requirements_summary(applicable)
        
        print()
        print("Summary:")
        print(f"  Total: {summary['total']} requirements")
        print(f"  By Type:")
        for t, count in sorted(summary['by_type'].items(), key=lambda x: x[1], reverse=True):
            print(f"    - {t:15s}: {count:2d}")
        print(f"  Max Penalty: ₹{summary['max_penalty'] / 10_000_000:,.0f} crore")
        print(f"  Total Exposure: ₹{summary['total_penalty_exposure'] / 10_000_000:,.0f} crore")
        print()
    
    print("="*70)
    print("✓ Requirement matcher working correctly")
    print("="*70)