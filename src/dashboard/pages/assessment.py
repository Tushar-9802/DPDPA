"""
Assessment Page - DPDPA Compliance Dashboard
Interactive 15-question form with validation
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.assessment.business_profiler import create_business_profile
from src.assessment.requirement_matcher import match_requirements
from src.assessment.gap_analyzer import analyze_gaps
from datetime import datetime

def show():
    """Render assessment form"""
    
    st.title("DPDPA Compliance Assessment")
    st.markdown("Answer 15 questions to get your personalized compliance report")
    
    # Initialize session state for form data
    if 'assessment_data' not in st.session_state:
        st.session_state['assessment_data'] = {}
    
    # Progress bar
    current_question = len([k for k in st.session_state['assessment_data'].keys() if k.startswith('q')])
    progress = min(current_question / 15, 1.0)
    st.progress(progress)
    st.caption(f"Question {min(current_question, 15)} of 15")
    
    # Form
    with st.form("assessment_form"):
        st.markdown("### Business Information")
        
        # Q1: Business Name
        business_name = st.text_input(
            "1. What is your business name? *",
            value=st.session_state['assessment_data'].get('business_name', ''),
            help="Legal name of your company"
        )
        
        # Q2: Entity Type
        entity_type = st.selectbox(
            "2. Select your entity type: *",
            options=["", "startup", "smb", "ecommerce", "social_media", "fintech", 
                    "healthcare", "edtech", "gaming", "other"],
            index=0,
            help="This determines which specific requirements apply"
        )
        
        # Q3: User Count
        user_count = st.number_input(
            "3. How many registered users do you have in India? *",
            min_value=0,
            value=st.session_state['assessment_data'].get('user_count', 0),
            help="Third Schedule applies if: E-commerce/Social Media >= 20M, Gaming >= 5M"
        )
        
        st.markdown("### Data Processing")
        
        # Q4: Children's Data
        processes_children_data = st.radio(
            "4. Do you process personal data of children (under 18)? *",
            options=["No", "Yes"],
            help="Children's data requires verifiable parent consent - Rs. 200cr penalty"
        ) == "Yes"
        
        # Q5: Cross-border
        cross_border_transfers = st.radio(
            "5. Do you transfer personal data outside India? *",
            options=["No", "Yes"],
            help="Cross-border transfers may face restrictions"
        ) == "Yes"
        
        # Q6: Data Types
        data_types = st.multiselect(
            "6. What types of personal data do you process? *",
            options=["name", "email", "phone", "address", "payment_info", 
                    "health_data", "biometric", "location", "behavioral"],
            help="Select all that apply"
        )
        
        # Q7: AI Usage
        uses_ai = st.radio(
            "7. Do you use AI or automated decision-making?",
            options=["No", "Yes", "Skip"],
            help="May trigger algorithmic due diligence for SDFs"
        )
        uses_ai = True if uses_ai == "Yes" else None if uses_ai == "Skip" else False
        
        # Q8: Revenue
        annual_revenue = st.selectbox(
            "8. What is your approximate annual revenue (INR)?",
            options=["Skip", "< 1 crore", "1-10 crore", "10-50 crore", 
                    "50-100 crore", "> 100 crore"],
            help="Optional - helps understand business scale"
        )
        annual_revenue = None if annual_revenue == "Skip" else annual_revenue
        
        st.markdown("### Current Compliance Status")
        
        # Q9: Processors
        has_processors = st.radio(
            "9. Do you have contracts with Data Processors (vendors)? *",
            options=["No", "Yes"],
            help="Rule 6(1)(f) requires security safeguards in contracts"
        ) == "Yes"
        
        # Q10: Security Measures
        current_security = st.multiselect(
            "10. What security measures do you currently have? *",
            options=["encryption", "access_control", "logging", "backups", "none"],
            help="Rule 6 requires minimum: encryption, access control, logging, backups"
        )
        
        # Q11: Breach Plan
        has_breach_plan = st.radio(
            "11. Do you have a documented breach response plan? *",
            options=["No", "Yes"],
            help="Rule 7 requires 72-hour notification to Board - Rs. 200cr penalty"
        ) == "Yes"
        
        # Q12-13: Tracking (CRITICAL for children!)
        tracks_behavior = st.radio(
            "12. Do you track user behavior or use analytics? *",
            options=["No", "Yes"],
            help="PROHIBITED for children under Rule 10"
        ) == "Yes"
        
        targeted_advertising = st.radio(
            "13. Do you do targeted advertising? *",
            options=["No", "Yes"],
            help="PROHIBITED for children under Rule 10"
        ) == "Yes"
        
        # Q14-15: Compliance Features
        has_consent_mechanism = st.radio(
            "14. Do you have a consent mechanism for users? *",
            options=["No", "Yes"],
            help="Required for ALL businesses"
        ) == "Yes"
        
        has_grievance_system = st.radio(
            "15. Do you have a grievance redressal system? *",
            options=["No", "Yes"],
            help="Rule 14 requires 90-day response time - Rs. 50cr penalty"
        ) == "Yes"
        
        # Submit button
        submitted = st.form_submit_button("Generate Compliance Report", use_container_width=True)
        
        if submitted:
            # Validation
            if not business_name or not entity_type or user_count is None:
                st.error("Please fill in all required fields marked with *")
            else:
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
                
                # Process assessment
                with st.spinner("Analyzing your compliance status..."):
                    try:
                        # Create business profile
                        business_id = create_business_profile(answers)
                        
                        # Match requirements
                        applicable_ids = match_requirements(answers)
                        
                        # Analyze gaps
                        analysis = analyze_gaps(business_id, applicable_ids, answers)
                        
                        # Store in session
                        st.session_state['current_assessment'] = {
                            'business_id': business_id,
                            'answers': answers,
                            'analysis': analysis
                        }
                        
                        # Success message
                        st.success("Assessment completed successfully!")
                        st.balloons()
                        
                        # Navigate to results page
                        st.query_params["page"] = "results"
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error processing assessment: {e}")
                        st.exception(e)

if __name__ == "__main__":
    show()