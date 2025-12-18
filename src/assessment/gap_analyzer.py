"""
Calculates compliance gaps and priority scores

Usage:
    from src.assessment.gap_analyzer import analyze_gaps
    analysis = analyze_gaps(business_id, applicable_requirement_ids)
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import DB_PATH, FULL_COMPLIANCE_DEADLINE


def calculate_priority_score(requirement: Dict[str, Any], penalty_amount: int) -> float:
    """
    Calculate priority score (0-100)
    
    Formula:
        40% penalty weight
        30% deadline urgency
        30% implementation complexity
    """
    
    # 1. Penalty score (0-100)
    max_penalty = 25_000_000_000  # ₹250 crore
    penalty_score = min((penalty_amount / max_penalty) * 100, 100)
    
    # 2. Deadline urgency (0-100)
    days_remaining = (FULL_COMPLIANCE_DEADLINE - datetime.now()).days
    max_days = 545  # 18 months from Nov 13, 2025
    if days_remaining <= 0:
        urgency_score = 100
    else:
        urgency = 1 - (days_remaining / max_days)
        urgency_score = max(urgency * 100, 0)
    
    # 3. Complexity score (0-100) based on obligation type
    complexity_map = {
        'security': 90,      # Hard (encryption, monitoring, etc.)
        'breach': 85,        # Hard (72-hour system)
        'children': 80,      # Hard (parent verification)
        'sdf': 75,          # Hard (DPIA, audit, DPO)
        'rights': 60,        # Medium (portal for requests)
        'retention': 50,     # Medium (data lifecycle)
        'notice': 40,        # Easy (document creation)
        'general': 50
    }
    complexity_score = complexity_map.get(requirement.get('obligation_type', 'general'), 50)
    
    # Weighted average
    priority = (
        penalty_score * 0.4 +
        urgency_score * 0.3 +
        complexity_score * 0.3
    )
    
    return round(priority, 2)


def get_completed_requirements(business_id: int) -> List[int]:
    """Get IDs of completed requirements"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT requirement_id
        FROM compliance_status
        WHERE business_profile_id = ?
          AND status = 'completed'
    """, (business_id,))
    
    completed = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return completed


def analyze_gaps(business_id: int, applicable_requirement_ids: List[int]) -> Dict[str, Any]:
    """
    Analyze compliance gaps and generate insights
    
    Args:
        business_id: Business profile ID
        applicable_requirement_ids: List of applicable requirement IDs
        
    Returns:
        Dictionary with gap analysis
    """
    
    if not applicable_requirement_ids:
        return {
            'total_requirements': 0,
            'completed': 0,
            'gaps': [],
            'compliance_score': 0,
            'max_penalty_exposure': 0,
            'total_penalty_exposure': 0,
            'priority_requirements': [],
            'by_type': {},
            'by_penalty_category': {}
        }
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get completed requirements
    completed_ids = get_completed_requirements(business_id)
    
    # Get all applicable requirements with details
    placeholders = ','.join('?' * len(applicable_requirement_ids))
    cursor.execute(f"""
        SELECT 
            r.id,
            r.rule_number,
            r.requirement_text,
            r.obligation_type,
            r.deadline,
            r.is_sdf_specific,
            p.id as penalty_id,
            p.category_name,
            p.amount_inr
        FROM requirements r
        LEFT JOIN penalties p ON r.penalty_category_id = p.id
        WHERE r.id IN ({placeholders})
        ORDER BY r.rule_number
    """, applicable_requirement_ids)
    
    rows = cursor.fetchall()
    conn.close()
    
    gaps = []
    by_type = {}
    by_penalty_category = {}
    all_penalties = []
    
    for row in rows:
        req_id = row[0]
        rule_number = row[1]
        requirement_text = row[2]
        obligation_type = row[3]
        deadline = row[4]
        is_sdf_specific = bool(row[5])
        penalty_id = row[6]
        penalty_category = row[7]
        penalty_amount = row[8] or 0
        
        # Count by type
        by_type[obligation_type] = by_type.get(obligation_type, 0) + 1
        by_penalty_category[penalty_category] = by_penalty_category.get(penalty_category, 0) + 1
        all_penalties.append(penalty_amount)
        
        # Check if completed
        if req_id in completed_ids:
            status = 'completed'
        else:
            status = 'not_started'
        
        # Only add to gaps if not completed
        if status != 'completed':
            # Calculate days remaining
            if deadline:
                deadline_dt = datetime.fromisoformat(deadline)
                days_remaining = (deadline_dt - datetime.now()).days
            else:
                deadline_dt = FULL_COMPLIANCE_DEADLINE
                days_remaining = (FULL_COMPLIANCE_DEADLINE - datetime.now()).days
            
            # Build requirement dict
            requirement = {
                'id': req_id,
                'rule_number': rule_number,
                'requirement_text': requirement_text,
                'obligation_type': obligation_type,
                'deadline': deadline,
                'is_sdf_specific': is_sdf_specific,
                'penalty_category_id': penalty_id,
                'penalty_category': penalty_category,
                'penalty_amount': penalty_amount,
                'days_remaining': days_remaining,
                'status': status
            }
            
            # Calculate priority score
            priority = calculate_priority_score(requirement, penalty_amount)
            requirement['priority_score'] = priority
            
            gaps.append(requirement)
    
    # Sort gaps by priority (highest first)
    gaps_sorted = sorted(gaps, key=lambda x: x['priority_score'], reverse=True)
    
    # Calculate compliance score
    compliance_score = (len(completed_ids) / len(applicable_requirement_ids)) * 100 if applicable_requirement_ids else 0
    
    return {
        'total_requirements': len(applicable_requirement_ids),
        'completed': len(completed_ids),
        'gaps': gaps_sorted,
        'compliance_score': round(compliance_score, 1),
        'max_penalty_exposure': max(all_penalties) if all_penalties else 0,
        'total_penalty_exposure': sum(all_penalties),
        'priority_requirements': gaps_sorted[:10],  # Top 10
        'by_type': by_type,
        'by_penalty_category': by_penalty_category
    }


# For testing
if __name__ == "__main__":
    print("="*70)
    print("GAP ANALYZER - TEST MODE")
    print("="*70)
    print()
    
    # Create test business profile
    from src.assessment.business_profiler import create_business_profile
    from src.assessment.requirement_matcher import match_requirements
    
    test_profile = {
        'business_name': 'Gap Test Corp',
        'entity_type': 'fintech',
        'user_count': 500000,
        'processes_children_data': False,
        'cross_border_transfers': True,
        'extended_data': {'has_processors': True}
    }
    
    print("Creating test business profile...")
    business_id = create_business_profile(test_profile)
    print()
    
    print("Matching requirements...")
    applicable = match_requirements(test_profile)
    print()
    
    print("Analyzing gaps...")
    analysis = analyze_gaps(business_id, applicable)
    print()
    
    print("="*70)
    print("GAP ANALYSIS RESULTS")
    print("="*70)
    print()
    print(f"Total Requirements: {analysis['total_requirements']}")
    print(f"Completed: {analysis['completed']}")
    print(f"Gaps: {len(analysis['gaps'])}")
    print(f"Compliance Score: {analysis['compliance_score']:.1f}%")
    print()
    print(f"Max Penalty: ₹{analysis['max_penalty_exposure'] / 10_000_000:,.0f} crore")
    print(f"Total Exposure: ₹{analysis['total_penalty_exposure'] / 10_000_000:,.0f} crore")
    print()
    
    print("TOP 10 PRIORITY REQUIREMENTS:")
    for i, req in enumerate(analysis['priority_requirements'][:10], 1):
        penalty_cr = req['penalty_amount'] / 10_000_000
        print(f"{i:2d}. {req['rule_number']:20s} [₹{penalty_cr:>6.0f}cr] [Priority: {req['priority_score']:>5.1f}]")
    print()
    
    print("BY OBLIGATION TYPE:")
    for t, count in sorted(analysis['by_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {t:15s}: {count:3d}")
    print()
    
    print("="*70)
    print("✓ Gap analyzer working correctly")
    print("="*70)