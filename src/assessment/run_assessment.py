"""
Runs complete assessment from questionnaire to Excel export

Usage:
    python src/assessment/run_assessment.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.assessment.questionnaire import run_questionnaire
from src.assessment.business_profiler import create_business_profile, get_business_profile, update_assessment_score
from src.assessment.requirement_matcher import match_requirements
from src.assessment.gap_analyzer import analyze_gaps
from src.assessment.report_generator import print_console_report, export_to_excel


def main():
    """Main assessment workflow"""
    
    print("\n" + "="*70)
    print("DPDPA COMPLIANCE ASSESSMENT")
    print("="*70)
    print()
    print("This assessment will:")
    print("  • Ask 15 questions about your business")
    print("  • Identify applicable DPDP requirements")
    print("  • Calculate compliance gaps")
    print("  • Generate priority roadmap")
    print("  • Export results to Excel")
    print()
    print("Estimated time: 10-15 minutes")
    print()
    
    try:
        input("Press Enter to begin...")
    except KeyboardInterrupt:
        print("\n\n❌ Assessment cancelled.")
        return 1
    
    print()
    
    try:
        # ================================================================
        # STEP 1: Run Questionnaire
        # ================================================================
        print("[1/6] Running assessment questionnaire...")
        print()
        
        answers = run_questionnaire()
        
        print()
        print(f"✓ Collected {len(answers)} answers")
        print()
        
        # ================================================================
        # STEP 2: Create Business Profile
        # ================================================================
        print("[2/6] Creating business profile...")
        print()
        
        business_id = create_business_profile(answers)
        
        print()
        
        # ================================================================
        # STEP 3: Match Requirements
        # ================================================================
        print("[3/6] Matching applicable requirements...")
        print()
        
        applicable_ids = match_requirements(answers)
        
        print()
        
        # ================================================================
        # STEP 4: Analyze Gaps
        # ================================================================
        print("[4/6] Analyzing compliance gaps...")
        print()
        
        analysis = analyze_gaps(business_id, applicable_ids)
        
        print(f"✓ Identified {len(analysis['gaps'])} compliance gaps")
        print(f"✓ Calculated priority scores")
        print()
        
        # Update compliance score in database
        update_assessment_score(business_id, analysis['compliance_score'])
        
        # ================================================================
        # STEP 5: Display Console Report
        # ================================================================
        print("[5/6] Generating report...")
        print()
        
        # Get full business profile for report
        business_profile = get_business_profile(business_id)
        
        # Merge with answers for complete profile
        business_profile.update(answers)
        
        print_console_report(business_profile, analysis)
        
        # ================================================================
        # STEP 6: Export to Excel
        # ================================================================
        print("[6/6] Exporting to Excel...")
        print()
        
        # Create output directory
        output_dir = project_root / "data" / "processed" / "assessment_results"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        business_name_clean = answers['business_name'].replace(' ', '_').replace('/', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"assessment_{business_id}_{business_name_clean}_{timestamp}.xlsx"
        filepath = output_dir / filename
        
        # Export
        export_to_excel(business_profile, analysis, str(filepath))
        
        print()
        
        # ================================================================
        # COMPLETION
        # ================================================================
        print("="*70)
        print("ASSESSMENT COMPLETE")
        print("="*70)
        print()
        print(f"✓ Business Profile ID: {business_id}")
        print(f"✓ Total Requirements: {analysis['total_requirements']}")
        print(f"✓ Compliance Gaps: {len(analysis['gaps'])}")
        print(f"✓ Compliance Score: {analysis['compliance_score']:.1f}%")
        print(f"✓ Max Penalty Exposure: ₹{analysis['max_penalty_exposure'] / 10_000_000:,.0f} crore")
        print()
        print(f"Report saved to:")
        print(f"  {filepath}")
        print()
        print("="*70)
        print("NEXT STEPS")
        print("="*70)
        print()
        print("1. Review your top 10 priority requirements")
        print("2. Focus on high-penalty items first:")
        print("   • Rule 6 (Security) - ₹250 crore penalty")
        print("   • Rule 7 (Breach Notification) - ₹200 crore penalty")
        print("   • Rule 10 (Children's Data) - ₹200 crore penalty")
        print()
        print("3. Download document templates (coming in Phase 3):")
        print("   • Privacy Notice")
        print("   • Breach Response Plan")
        print("   • Security Checklist")
        print()
        print("4. Track progress in dashboard (coming in Phase 4)")
        print()
        print(f"Deadline: May 13, 2027 ({analysis['gaps'][0]['days_remaining'] if analysis['gaps'] else 'N/A'} days remaining)")
        print()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n❌ Assessment cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error during assessment: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)