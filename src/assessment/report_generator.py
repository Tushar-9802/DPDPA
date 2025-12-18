"""
Formats and exports assessment results

Usage:
    from src.assessment.report_generator import print_console_report, export_to_excel
"""

import pandas as pd
from pathlib import Path
import sys
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def print_console_report(business_profile: Dict[str, Any], analysis: Dict[str, Any]):
    """
    Print formatted console report
    
    Args:
        business_profile: Business profile dictionary
        analysis: Gap analysis dictionary
    """
    
    print("\n" + "="*70)
    print("DPDPA COMPLIANCE ASSESSMENT REPORT")
    print("="*70)
    print()
    
    # Business Profile
    print("BUSINESS PROFILE")
    print("-"*70)
    print(f"  Name: {business_profile.get('business_name', 'N/A')}")
    print(f"  Type: {business_profile.get('entity_type', 'N/A').title()}")
    print(f"  Users: {business_profile.get('user_count', 0):,}")
    print(f"  Children's Data: {'Yes' if business_profile.get('processes_children_data') else 'No'}")
    print(f"  Cross-Border Transfers: {'Yes' if business_profile.get('cross_border_transfers') else 'No'}")
    print()
    
    # Requirements Summary
    print("APPLICABLE REQUIREMENTS")
    print("-"*70)
    print(f"  Total: {analysis['total_requirements']} requirements")
    print()
    print("  By Obligation Type:")
    for t, count in sorted(analysis['by_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"    • {t.title():15s}: {count:3d} requirements")
    print()
    
    # Compliance Status
    print("COMPLIANCE STATUS")
    print("-"*70)
    print(f"  Completed: {analysis['completed']} / {analysis['total_requirements']}")
    print(f"  Gaps: {len(analysis['gaps'])}")
    print(f"  Score: {analysis['compliance_score']:.1f}%")
    print()
    
    # Penalty Exposure
    print("PENALTY EXPOSURE")
    print("-"*70)
    max_penalty_cr = analysis['max_penalty_exposure'] / 10_000_000
    total_exposure_cr = analysis['total_penalty_exposure'] / 10_000_000
    print(f"  Highest Single Penalty: ₹{max_penalty_cr:,.0f} crore")
    print(f"  Total Exposure: ₹{total_exposure_cr:,.0f} crore")
    print()
    
    # Top Priority Requirements
    print("TOP 10 PRIORITY REQUIREMENTS")
    print("-"*70)
    for i, req in enumerate(analysis['priority_requirements'][:10], 1):
        penalty_cr = req['penalty_amount'] / 10_000_000
        days = req['days_remaining']
        print(f"{i:2d}. {req['rule_number']:20s} [{req['obligation_type']:10s}]")
        print(f"    Penalty: ₹{penalty_cr:>6.0f} crore | Priority: {req['priority_score']:>5.1f}/100 | {days} days left")
        print(f"    {req['requirement_text'][:100]}...")
        print()
    
    # Deadline Warning
    if analysis['gaps']:
        days_left = analysis['gaps'][0]['days_remaining']
        print("DEADLINE")
        print("-"*70)
        print(f"  Full Compliance: May 13, 2027")
        print(f"  Days Remaining: {days_left}")
        if days_left < 180:
            print(f"  ⚠️  WARNING: Less than 6 months remaining!")
        print()
    
    print("="*70)


def export_to_excel(business_profile: Dict[str, Any], analysis: Dict[str, Any], filepath: str):
    """
    Export assessment results to Excel
    
    Args:
        business_profile: Business profile dictionary
        analysis: Gap analysis dictionary
        filepath: Output file path
    """
    
    # Sheet 1: Summary
    summary_data = {
        'Metric': [
            'Business Name',
            'Entity Type',
            'Users in India',
            'Processes Children Data',
            'Cross-Border Transfers',
            '',
            'Total Applicable Requirements',
            'Completed Requirements',
            'Compliance Gaps',
            'Compliance Score (%)',
            '',
            'Highest Single Penalty (INR)',
            'Total Penalty Exposure (INR)',
            '',
            'Days to Deadline',
            'Deadline Date'
        ],
        'Value': [
            business_profile.get('business_name', 'N/A'),
            business_profile.get('entity_type', 'N/A').title(),
            f"{business_profile.get('user_count', 0):,}",
            'Yes' if business_profile.get('processes_children_data') else 'No',
            'Yes' if business_profile.get('cross_border_transfers') else 'No',
            '',
            analysis['total_requirements'],
            analysis['completed'],
            len(analysis['gaps']),
            f"{analysis['compliance_score']:.1f}%",
            '',
            f"₹{analysis['max_penalty_exposure']:,}",
            f"₹{analysis['total_penalty_exposure']:,}",
            '',
            analysis['gaps'][0]['days_remaining'] if analysis['gaps'] else 'N/A',
            'May 13, 2027'
        ]
    }
    df_summary = pd.DataFrame(summary_data)
    
    # Sheet 2: All Requirements/Gaps
    gaps_data = []
    for gap in analysis['gaps']:
        gaps_data.append({
            'Priority Score': gap['priority_score'],
            'Rule Number': gap['rule_number'],
            'Obligation Type': gap['obligation_type'].title(),
            'Requirement': gap['requirement_text'][:200],  # Truncate for Excel
            'Penalty Category': gap['penalty_category'],
            'Penalty Amount (INR)': gap['penalty_amount'],
            'Penalty (Crore)': f"₹{gap['penalty_amount'] / 10_000_000:.0f}",
            'Days to Deadline': gap['days_remaining'],
            'Deadline': gap['deadline'],
            'Status': gap['status'].title(),
            'SDF Specific': 'Yes' if gap['is_sdf_specific'] else 'No'
        })
    
    if gaps_data:
        df_gaps = pd.DataFrame(gaps_data)
        df_gaps = df_gaps.sort_values('Priority Score', ascending=False)
    else:
        df_gaps = pd.DataFrame()
    
    # Sheet 3: By Obligation Type
    by_type_data = [
        {'Obligation Type': t.title(), 'Count': count}
        for t, count in sorted(analysis['by_type'].items(), key=lambda x: x[1], reverse=True)
    ]
    df_by_type = pd.DataFrame(by_type_data)
    
    # Sheet 4: By Penalty Category
    by_penalty_data = [
        {'Penalty Category': cat, 'Count': count}
        for cat, count in sorted(analysis['by_penalty_category'].items(), key=lambda x: x[1], reverse=True)
    ]
    df_by_penalty = pd.DataFrame(by_penalty_data)
    
    # Write to Excel with formatting
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        if not df_gaps.empty:
            df_gaps.to_excel(writer, sheet_name='All Requirements', index=False)
        
        df_by_type.to_excel(writer, sheet_name='By Obligation Type', index=False)
        df_by_penalty.to_excel(writer, sheet_name='By Penalty Category', index=False)
        
        # Auto-adjust column widths
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 100)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"\n✓ Exported to: {filepath}")


# For testing
if __name__ == "__main__":
    print("="*70)
    print("REPORT GENERATOR - TEST MODE")
    print("="*70)
    
    # Use gap_analyzer test data
    from src.assessment.business_profiler import create_business_profile
    from src.assessment.requirement_matcher import match_requirements
    from src.assessment.gap_analyzer import analyze_gaps
    
    test_profile = {
        'business_name': 'Report Test Corp',
        'entity_type': 'ecommerce',
        'user_count': 10_000_000,
        'processes_children_data': True,
        'cross_border_transfers': True,
        'extended_data': {'has_processors': True}
    }
    
    print("\nCreating test business profile...")
    business_id = create_business_profile(test_profile)
    
    print("Matching requirements...")
    applicable = match_requirements(test_profile)
    
    print("Analyzing gaps...")
    analysis = analyze_gaps(business_id, applicable)
    
    # Test console report
    print_console_report(test_profile, analysis)
    
    # Test Excel export
    output_dir = project_root / "data" / "processed" / "assessment_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = output_dir / "test_assessment_report.xlsx"
    export_to_excel(test_profile, analysis, str(filepath))
    
    print("\n" + "="*70)
    print("✓ Report generator working correctly")
    print("="*70)