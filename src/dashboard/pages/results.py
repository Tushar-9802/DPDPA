"""
Results Page - DPDPA Compliance Dashboard
Display assessment results with metrics and downloadable report
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.assessment.business_profiler import get_business_profile
from src.assessment.requirement_matcher import match_requirements
from src.assessment.gap_analyzer import analyze_gaps
from src.assessment.report_generator import export_to_excel

def show():
    """Render results page"""
    
    st.title("Compliance Report")
    
    # Check if we have assessment data
    if 'current_assessment' in st.session_state:
        data = st.session_state['current_assessment']
        business_id = data['business_id']
        answers = data['answers']
        analysis = data['analysis']
    elif 'selected_business_id' in st.session_state:
        # Load from database
        business_id = st.session_state['selected_business_id']
        try:
            profile = get_business_profile(business_id)
            answers = profile
            if 'extended_data' in profile:
                answers.update(profile['extended_data'])
            
            # Re-run analysis with answers
            applicable_ids = match_requirements(answers)
            analysis = analyze_gaps(business_id, applicable_ids, answers)
        except Exception as e:
            st.error(f"Error loading assessment: {e}")
            return
    else:
        st.warning("No assessment data found. Please complete an assessment first.")
        if st.button("Start New Assessment"):
            st.query_params["page"] = "assessment"
            st.rerun()
        return
    
    # Business info header
    st.markdown(f"### {answers.get('business_name', 'N/A')}")
    st.caption(f"{answers.get('entity_type', 'N/A').title()} | {answers.get('user_count', 0):,} users")
    
    st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = analysis['compliance_score']
        st.metric(
            label="Compliance Score",
            value=f"{score:.1f}%",
            delta=f"{analysis['completed']}/{analysis['total_requirements']} complete"
        )
    
    with col2:
        max_penalty_cr = analysis['max_penalty_exposure'] / 10_000_000
        st.metric(
            label="Max Single Penalty",
            value=f"Rs. {max_penalty_cr:.0f} Cr",
            delta="Security breach"
        )
    
    with col3:
        total_exposure_cr = analysis['total_penalty_exposure'] / 10_000_000
        st.metric(
            label="Total Exposure",
            value=f"Rs. {total_exposure_cr:,.0f} Cr",
            delta=f"{len(analysis['gaps'])} gaps"
        )
    
    with col4:
        deadline = datetime(2027, 5, 13)
        days_left = (deadline - datetime.now()).days
        st.metric(
            label="Days to Deadline",
            value=days_left,
            delta="May 13, 2027"
        )
    
    st.markdown("---")
    
    # Illegal activity warning (if applicable)
    if answers.get('processes_children_data'):
        if answers.get('tracks_behavior') or answers.get('targeted_advertising'):
            violations = []
            if answers.get('tracks_behavior'):
                violations.append("Behavioral tracking of children")
            if answers.get('targeted_advertising'):
                violations.append("Targeted advertising to children")
                
            st.error(f"""
            ### CRITICAL LEGAL VIOLATION
            
            You are currently violating **DPDP Act Section 9(3)**:
            
            {chr(10).join('- ' + v for v in violations)}
            
            **PENALTY: Rs. 200 CRORE PER VIOLATION**
            
            **Action required: IMMEDIATELY cease these activities!**
            """)
    
    # Requirements breakdown
    st.subheader("Requirements Breakdown")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Summary table
        breakdown_data = []
        for oblig_type, count in sorted(
            analysis['by_type'].items(), 
            key=lambda x: x[1], 
            reverse=True
        ):
            breakdown_data.append({
                'Type': oblig_type.title(),
                'Count': count
            })
        
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown(f"""
        **Total Applicable Requirements:** {analysis['total_requirements']}
        
        **Compliance Status:**
        - Completed: {analysis['completed']}
        - Pending: {len(analysis['gaps'])}
        
        **Key Areas:**
        - Security: {analysis['by_type'].get('security', 0)} requirements
        - Breach Notification: {analysis['by_type'].get('breach', 0)} requirements
        - Children's Data: {analysis['by_type'].get('children', 0)} requirements
        - Notice: {analysis['by_type'].get('notice', 0)} requirements
        - Rights: {analysis['by_type'].get('rights', 0)} requirements
        """)
    
    st.markdown("---")
    
    # Top priorities
    st.subheader("Top 10 Priority Requirements")
    
    priorities_data = []
    for req in analysis['priority_requirements'][:10]:
        priorities_data.append({
            'Priority': f"{req['priority_score']:.1f}/100",
            'Rule': req['rule_number'],
            'Type': req['obligation_type'].title(),
            'Penalty': f"Rs. {req['penalty_amount'] / 10_000_000:.0f} Cr",
            'Days Left': req['days_remaining'],
            'Description': req['requirement_text'][:80] + "..."
        })
    
    df_priorities = pd.DataFrame(priorities_data)
    st.dataframe(df_priorities, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export to Excel
        if st.button("Download Excel Report", use_container_width=True):
            try:
                # Generate Excel
                output_dir = project_root / "data" / "processed" / "assessment_results"
                output_dir.mkdir(parents=True, exist_ok=True)
                
                business_name_clean = answers['business_name'].replace(' ', '_').replace('/', '_')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"assessment_{business_id}_{business_name_clean}_{timestamp}.xlsx"
                filepath = output_dir / filename
                
                # Get full profile
                profile = get_business_profile(business_id)
                profile.update(answers)
                
                export_to_excel(profile, analysis, str(filepath))
                
                # Provide download
                with open(filepath, 'rb') as f:
                    st.download_button(
                        label="Save Excel File",
                        data=f,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"Error generating Excel: {e}")
    
    with col2:
        if st.button("New Assessment", use_container_width=True):
            # Clear session state
            if 'current_assessment' in st.session_state:
                del st.session_state['current_assessment']
            if 'selected_business_id' in st.session_state:
                del st.session_state['selected_business_id']
            st.query_params["page"] = "assessment"
            st.rerun()
    
    with col3:
        if st.button("Back to Home", use_container_width=True):
            # Clear selected business ID
            if 'selected_business_id' in st.session_state:
                del st.session_state['selected_business_id']
            st.query_params["page"] = "home"
            st.rerun()
    
    st.markdown("---")
    
    # Next steps
    st.subheader("Next Steps")
    
    st.markdown("""
    1. **Review Priority Requirements** - Focus on high-penalty items first
    2. **Implement Security Measures** - Rule 6 (Rs. 250 crore penalty)
    3. **Setup Breach Response** - Rule 7 (Rs. 200 crore penalty, 72-hour timeline)
    4. **Children's Data Compliance** - Rule 10 (Rs. 200 crore penalty if applicable)
    5. **Track Progress** - Update compliance status as you implement
    
    **Need Help?**
    - Download the Excel report for detailed analysis
    - Consult a data protection lawyer for legal advice
    - Monitor MEITY website for updates and guidance
    """)

if __name__ == "__main__":
    show()