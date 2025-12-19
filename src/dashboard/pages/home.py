"""
Home Page - DPDPA Compliance Dashboard
Landing page with project overview and past assessments
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.assessment.business_profiler import list_business_profiles
from datetime import datetime

def show():
    """Render home page"""
    
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; font-family: Arial, sans-serif;'>
        <h1>DPDPA Compliance Dashboard</h1>
        <p style='font-size: 1.2rem; color: #666;'>
            Assess your compliance with India's Digital Personal Data Protection Act 2023
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Requirements",
            value="50+",
            delta="Extracted from DPDP Rules 2025"
        )
    
    with col2:
        deadline = datetime(2027, 5, 13)
        days_left = (deadline - datetime.now()).days
        st.metric(
            label="Days to Compliance",
            value=days_left,
            delta="May 13, 2027 deadline"
        )
    
    with col3:
        st.metric(
            label="Max Penalty",
            value="Rs. 250 Cr",
            delta="Security breach violations"
        )
    
    st.markdown("---")
    
    # Call to action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; font-family: Arial, sans-serif;'>
            <h3>Ready to assess your compliance?</h3>
            <p>Complete our 15-question assessment to identify your gaps and get a prioritized roadmap.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start New Assessment", use_container_width=True):
            # Clear any existing state
            if 'current_assessment' in st.session_state:
                del st.session_state['current_assessment']
            if 'selected_business_id' in st.session_state:
                del st.session_state['selected_business_id']
            # Navigate
            st.query_params["page"] = "assessment"
            st.rerun()
    
    st.markdown("---")
    
    # Past assessments
    st.subheader("Your Past Assessments")
    
    try:
        profiles = list_business_profiles()
        
        if profiles:
            # Create options for selectbox
            profile_options = ["Select an assessment..."] + [
                f"{p['business_name']} ({p['entity_type'].title()}) - {p['created_at'][:10] if p.get('created_at') else 'N/A'}"
                for p in profiles[:10]  # Show last 10
            ]
            
            selected = st.selectbox(
                "Choose an assessment to view:",
                options=profile_options,
                key="assessment_selector"
            )
            
            if selected != "Select an assessment...":
                # Find the selected profile
                selected_index = profile_options.index(selected) - 1
                selected_profile = profiles[selected_index]
                
                # Show details
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Users", f"{selected_profile['user_count']:,}")
                with col2:
                    st.metric("Compliance", f"{selected_profile['assessment_score']:.1f}%")
                with col3:
                    st.metric("Type", selected_profile['entity_type'].title())
                with col4:
                    created = selected_profile['created_at'][:10] if selected_profile.get('created_at') else 'N/A'
                    st.metric("Created", created)
                
                # View button
                if st.button("View Full Report", use_container_width=True):
                    st.session_state['selected_business_id'] = selected_profile['id']
                    st.query_params["page"] = "results"
                    st.rerun()
        else:
            st.info("No assessments yet. Start your first assessment above!")
            
    except Exception as e:
        st.error(f"Error loading assessments: {e}")
        import traceback
        st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # Quick info
    st.markdown("""
    ### What is DPDPA?
    
    The **Digital Personal Data Protection Act, 2023** is India's comprehensive data protection law. 
    It regulates how organizations collect, process, and store personal data of Indian citizens.
    
    **Key Highlights:**
    - Compliance deadline: **May 13, 2027** (18 months from Rules notification)
    - Applies to: All businesses processing Indian user data
    - Penalties: Up to **Rs. 250 crore** for violations
    - Focus areas: Consent, security, breach notification, children's data
    
    ### Who Should Use This Tool?
    
    - **Startups** processing user data
    - **SMBs** with Indian customers
    - **E-commerce** platforms
    - **Gaming** companies
    - **Fintech** applications
    - **SaaS** businesses
    
    ### Need Help?
    
    This tool provides automated compliance assessment. For legal advice, 
    consult a qualified data protection lawyer.
    """)
    
    st.markdown("---")
    st.caption("Built for Indian Startups & SMBs")

if __name__ == "__main__":
    show()