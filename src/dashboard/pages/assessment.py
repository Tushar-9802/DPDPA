"""
Assessment Page - DPDPA Compliance Dashboard
Interactive 15-question form with validation and demo mode
"""

import streamlit as st
import sys
from pathlib import Path
import time

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.assessment.business_profiler import create_business_profile
from src.assessment.requirement_matcher import match_requirements
from src.assessment.gap_analyzer import analyze_gaps

# Demo data for quick testing
DEMO_DATA = {
    'business_name': 'TechStartup Pvt Ltd',
    'entity_type': 'startup',
    'user_count': 15000,
    'processes_children_data': False,
    'cross_border_transfers': False,
    'data_types': ['name', 'email', 'phone'],
    'uses_ai': True,
    'annual_revenue': '1-10 crore',
    'has_processors': True,
    'current_security': ['encryption', 'access_control', 'logging', 'backups'],
    'has_breach_plan': True,
    'tracks_behavior': False,
    'targeted_advertising': False,
    'has_consent_mechanism': True,
    'has_grievance_system': True
}

def show():
    """Render assessment form with demo mode"""
    
    st.title("DPDPA Compliance Assessment")
    
    # Demo mode button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Try Demo (Pre-filled Data)", use_container_width=True, type="secondary"):
            st.session_state['demo_mode'] = True
            st.rerun()
    
    if st.session_state.get('demo_mode', False):
        st.info("Demo Mode Active - Form pre-filled with sample data. Edit as needed or submit as-is.")
    
    st.markdown("Answer 15 questions to get your personalized compliance report")
    st.markdown("---")
    
    # Form with demo data support
    with st.form("assessment_form", clear_on_submit=False):
        
        # Section 1: Business Information
        st.markdown("### Business Information")
        
        # Q1: Business Name
        business_name = st.text_input(
            "1. What is your business name? *",
            value=DEMO_DATA['business_name'] if st.session_state.get('demo_mode') else '',
            help="Legal name of your company",
            placeholder="e.g., TechCorp India Pvt Ltd"
        )
        
        # Q2: Entity Type
        entity_options = ["", "startup", "smb", "ecommerce", "social_media", "fintech",
                         "healthcare", "edtech", "gaming", "other"]
        entity_index = 0
        if st.session_state.get('demo_mode'):
            try:
                entity_index = entity_options.index(DEMO_DATA['entity_type'])
            except ValueError:
                entity_index = 0
        
        entity_type = st.selectbox(
            "2. Select your entity type: *",
            options=entity_options,
            index=entity_index,
            help="Determines which specific requirements apply (e.g., Third Schedule thresholds)"
        )
        
        # Q3: User Count
        user_count = st.number_input(
            "3. How many registered users do you have in India? *",
            min_value=0,
            value=DEMO_DATA['user_count'] if st.session_state.get('demo_mode') else 0,
            step=1000,
            help="Third Schedule applies if: E-commerce/Social Media >=20M, Gaming >=5M"
        )
        
        st.markdown("---")
        
        # Section 2: Data Processing
        st.markdown("### Data Processing")
        
        # Q4: Children's Data
        children_default = "Yes" if (st.session_state.get('demo_mode') and DEMO_DATA['processes_children_data']) else "No"
        processes_children_data = st.radio(
            "4. Do you process personal data of children (under 18)? *",
            options=["No", "Yes"],
            index=1 if children_default == "Yes" else 0,
            help="WARNING: Children's data requires verifiable parent consent - Rs. 200 crore penalty"
        ) == "Yes"
        
        # Q5: Cross-border
        cross_border_default = "Yes" if (st.session_state.get('demo_mode') and DEMO_DATA['cross_border_transfers']) else "No"
        cross_border_transfers = st.radio(
            "5. Do you transfer personal data outside India? *",
            options=["No", "Yes"],
            index=1 if cross_border_default == "Yes" else 0,
            help="May face restrictions per Rule 15; monitor MEITY notifications"
        ) == "Yes"
        
        # Q6: Data Types
        data_types = st.multiselect(
            "6. What types of personal data do you process? *",
            options=["name", "email", "phone", "address", "payment_info",
                    "health_data", "biometric", "location", "behavioral"],
            default=DEMO_DATA['data_types'] if st.session_state.get('demo_mode') else [],
            help="Health/biometric = higher risk; select all that apply"
        )
        
        # Q7: AI Usage
        ai_options = ["No", "Yes", "Skip"]
        ai_default = 1 if (st.session_state.get('demo_mode') and DEMO_DATA.get('uses_ai')) else 0
        uses_ai_raw = st.radio(
            "7. Do you use AI or automated decision-making?",
            options=ai_options,
            index=ai_default,
            help="May trigger algorithmic due diligence if designated as SDF"
        )
        uses_ai = True if uses_ai_raw == "Yes" else None if uses_ai_raw == "Skip" else False
        
        # Q8: Revenue
        revenue_options = ["Skip", "< 1 crore", "1-10 crore", "10-50 crore", "50-100 crore", "> 100 crore"]
        revenue_default = 0
        if st.session_state.get('demo_mode') and DEMO_DATA.get('annual_revenue'):
            try:
                revenue_default = revenue_options.index(DEMO_DATA['annual_revenue'])
            except ValueError:
                revenue_default = 0
        
        annual_revenue = st.selectbox(
            "8. What is your approximate annual revenue (INR)?",
            options=revenue_options,
            index=revenue_default,
            help="Optional - helps understand business scale"
        )
        annual_revenue = None if annual_revenue == "Skip" else annual_revenue
        
        st.markdown("---")
        
        # Section 3: Current Compliance
        st.markdown("### Current Compliance Status")
        
        # Q9: Processors
        processors_default = "Yes" if (st.session_state.get('demo_mode') and DEMO_DATA['has_processors']) else "No"
        has_processors = st.radio(
            "9. Do you have contracts with Data Processors (vendors)? *",
            options=["No", "Yes"],
            index=1 if processors_default == "Yes" else 0,
            help="Rule 6(1)(f) requires security safeguards in contracts"
        ) == "Yes"
        
        # Q10: Security Measures
        current_security = st.multiselect(
            "10. What security measures do you currently have? *",
            options=["encryption", "access_control", "logging", "backups", "none"],
            default=DEMO_DATA['current_security'] if st.session_state.get('demo_mode') else [],
            help="WARNING: Rule 6 requires ALL FOUR: encryption, access control, logging, backups (Rs. 250 crore penalty)"
        )
        
        # Q11: Breach Plan
        breach_default = "Yes" if (st.session_state.get('demo_mode') and DEMO_DATA['has_breach_plan']) else "No"
        has_breach_plan = st.radio(
            "11. Do you have a documented breach response plan? *",
            options=["No", "Yes"],
            index=1 if breach_default == "Yes" else 0,
            help="WARNING: Rule 7 requires 72-hour notification to Board - Rs. 200 crore penalty"
        ) == "Yes"
        
        # Q12: Tracking
        tracking_default = "Yes" if (st.session_state.get('demo_mode') and DEMO_DATA['tracks_behavior']) else "No"
        tracks_behavior = st.radio(
            "12. Do you track user behavior or use analytics? *",
            options=["No", "Yes"],
            index=1 if tracking_default == "Yes" else 0,
            help="WARNING: PROHIBITED for children under Rule 10 - Rs. 200 crore penalty"
        ) == "Yes"
        
        # Q13: Advertising
        ads_default = "Yes" if (st.session_state.get('demo_mode') and DEMO_DATA['targeted_advertising']) else "No"
        targeted_advertising = st.radio(
            "13. Do you do targeted advertising? *",
            options=["No", "Yes"],
            index=1 if ads_default == "Yes" else 0,
            help="WARNING: PROHIBITED for children under Rule 10 - Rs. 200 crore penalty"
        ) == "Yes"
        
        # Q14: Consent
        consent_default = "Yes" if (st.session_state.get('demo_mode') and DEMO_DATA['has_consent_mechanism']) else "No"
        has_consent_mechanism = st.radio(
            "14. Do you have a consent mechanism for users? *",
            options=["No", "Yes"],
            index=1 if consent_default == "Yes" else 0,
            help="Rule 3 + Section 6 - Required for ALL businesses"
        ) == "Yes"
        
        # Q15: Grievance
        grievance_default = "Yes" if (st.session_state.get('demo_mode') and DEMO_DATA['has_grievance_system']) else "No"
        has_grievance_system = st.radio(
            "15. Do you have a grievance redressal system? *",
            options=["No", "Yes"],
            index=1 if grievance_default == "Yes" else 0,
            help="WARNING: Rule 14 requires 90-day response time - Rs. 50 crore penalty"
        ) == "Yes"
        
        st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "Generate Compliance Report",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            # Clear demo mode
            if 'demo_mode' in st.session_state:
                del st.session_state['demo_mode']
            
            # Validation
            errors = []
            if not business_name or len(business_name) < 2:
                errors.append("Business name is required")
            if not entity_type:
                errors.append("Entity type is required")
            if user_count is None:
                errors.append("User count is required")
            if not data_types:
                errors.append("At least one data type must be selected")
            if not current_security or 'none' in current_security:
                if 'none' not in current_security:
                    errors.append("At least one security measure must be selected")
            
            if errors:
                st.error("Please fix the following errors:\n\n" + "\n".join(f"- {e}" for e in errors))
                st.stop()
            
            # Check for illegal activity
            if processes_children_data and (tracks_behavior or targeted_advertising):
                st.error("""
                ### CRITICAL LEGAL VIOLATION DETECTED
                
                **DPDP Act Section 9(3) PROHIBITS:**
                - Behavioral tracking of children
                - Targeted advertising directed at children
                
                **PENALTY: Rs. 200 CRORE PER VIOLATION**
                
                **REQUIRED ACTIONS:**
                1. IMMEDIATELY cease all prohibited activities
                2. Delete all behavioral data collected from children
                3. Implement age verification + parental consent
                4. Consult legal counsel
                
                The assessment will continue, but you MUST address these violations immediately.
                """)
                
                if not st.checkbox("I acknowledge these violations and will take immediate action"):
                    st.stop()
            
            # Prepare data
            answers = {
                'business_name': business_name,
                'entity_type': entity_type,
                'user_count': user_count,
                'processes_children_data': processes_children_data,
                'cross_border_transfers': cross_border_transfers,
                'data_types': data_types,
                'uses_ai': uses_ai,
                'annual_revenue': annual_revenue,
                'has_processors': has_processors,
                'current_security': current_security,
                'has_breach_plan': has_breach_plan,
                'tracks_behavior': tracks_behavior,
                'targeted_advertising': targeted_advertising,
                'has_consent_mechanism': has_consent_mechanism,
                'has_grievance_system': has_grievance_system
            }
            
            # Process with loading states
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Create profile
                status_text.text("Creating business profile...")
                progress_bar.progress(25)
                time.sleep(0.3)
                business_id = create_business_profile(answers)
                
                # Step 2: Match requirements
                status_text.text("Matching applicable requirements...")
                progress_bar.progress(50)
                time.sleep(0.3)
                applicable_ids = match_requirements(answers)
                
                # Step 3: Analyze gaps
                status_text.text("Analyzing compliance gaps...")
                progress_bar.progress(75)
                time.sleep(0.3)
                analysis = analyze_gaps(business_id, applicable_ids, answers)
                
                # Complete
                progress_bar.progress(100)
                status_text.text("Assessment complete!")
                time.sleep(0.5)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Store in session
                st.session_state['current_assessment'] = {
                    'business_id': business_id,
                    'answers': answers,
                    'analysis': analysis
                }
                
                # Success message
                st.success("Assessment completed successfully!")
                
                # Navigate to results
                time.sleep(0.5)
                st.query_params["page"] = "results"
                st.rerun()
                
            except Exception as e:
                st.error(f"Error processing assessment: {str(e)}")
                with st.expander("Technical Details"):
                    st.code(str(e))
                st.info("Troubleshooting: Check that the database exists and all required fields are filled.")

if __name__ == "__main__":
    show()