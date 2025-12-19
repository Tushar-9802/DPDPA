"""
DPDPA Reference Page - Legal Framework Documentation
Provides quick reference to DPDP Act 2023 key provisions
"""

import streamlit as st
import pandas as pd
def show():
    """Render DPDPA reference page"""
    
    st.title("DPDPA 2023 - Quick Reference")
    
    st.markdown("""
    This page provides a quick reference to key provisions of India's Digital Personal 
    Data Protection Act, 2023 and DPDP Rules, 2025.
    """)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview", 
        "Key Definitions", 
        "Main Requirements", 
        "Penalties", 
        "Compliance Checklist"
    ])
    
    with tab1:
        st.header("Act Overview")
        
        st.markdown("""
        ### Digital Personal Data Protection Act, 2023
        
        **Enacted:** August 11, 2023
        
        **Rules Notified:** November 13, 2025
        
        **Compliance Deadline:** May 13, 2027 (18 months from Rules notification)
        
        **Objective:** To provide for the processing of digital personal data in a manner 
        that recognizes both the right of individuals to protect their personal data and 
        the need to process such data for lawful purposes.
        
        ---
        
        ### Scope of Application
        
        The Act applies to:
        
        1. **Processing within India:** Processing of digital personal data within the territory of India
        
        2. **Processing outside India:** Processing of digital personal data outside India, if in connection with:
           - Any activity related to offering of goods or services to Data Principals within India
           - Profiling of Data Principals within India
        
        3. **Government and Private:** Both government and private entities
        
        ---
        
        ### Key Principles
        
        1. **Lawfulness, fairness and transparency**
        2. **Purpose limitation**
        3. **Data minimization**
        4. **Accuracy**
        5. **Storage limitation**
        6. **Reasonable security safeguards**
        7. **Accountability**
        """)
    
    with tab2:
        st.header("Key Definitions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Data Fiduciary
            Any person who alone or in conjunction with other persons determines 
            the purpose and means of processing of personal data.
            
            **Example:** Your business/company
            
            ---
            
            ### Data Principal
            The individual to whom the personal data relates.
            
            **Example:** Your customers/users
            
            ---
            
            ### Data Processor
            Any person who processes personal data on behalf of a Data Fiduciary.
            
            **Example:** Cloud service providers, payment processors
            
            ---
            
            ### Personal Data
            Any data about an individual who is identifiable by or in relation to such data.
            
            **Examples:**
            - Name, email, phone
            - Address, location
            - Payment information
            - Biometric data
            - Behavioral data
            """)
        
        with col2:
            st.markdown("""
            ### Consent
            A free, specific, informed, unconditional and unambiguous indication of 
            Data Principal's agreement to processing of their personal data.
            
            **Requirements:**
            - Must be clear and plain language
            - Separate from other terms
            - Itemized for different purposes
            - Withdrawable
            
            ---
            
            ### Significant Data Fiduciary (SDF)
            A Data Fiduciary notified by the Central Government based on:
            - Volume and sensitivity of data
            - Risk to rights of Data Principals
            - Impact on sovereignty and integrity of India
            - Potential to affect electoral democracy
            
            **Additional Obligations:**
            - Data Protection Impact Assessment
            - Data Protection Officer
            - Independent Data Auditor
            
            ---
            
            ### Children
            Individuals below the age of 18 years.
            
            **Special Protection:** Cannot be tracked or targeted for advertising
            """)
    
    with tab3:
        st.header("Main Requirements")
        
        with st.expander("Rule 3 - Notice", expanded=False):
            st.markdown("""
            **Every Data Fiduciary must provide notice that:**
            
            1. Can be presented and understood independently
            2. Is in clear and plain language
            3. Provides:
               - Itemized description of personal data being processed
               - Specified purpose of processing
               - Communication links to:
                 - Withdraw consent
                 - Exercise rights
                 - Make complaints to Data Protection Board
            
            **Penalty:** Rs. 50 crore
            """)
        
        with st.expander("Rule 6 - Security Safeguards", expanded=False):
            st.markdown("""
            **Data Fiduciaries must implement:**
            
            1. **Data security measures:**
               - Encryption
               - Obfuscation
               - Other appropriate measures
            
            2. **Access control:**
               - Control access to computer resources
               - Limit access to authorized personnel
            
            3. **Monitoring:**
               - Visibility on data access
               - Appropriate logs (retain for 1 year minimum)
               - Regular monitoring and review
            
            4. **Business continuity:**
               - Measures for continued processing
               - Handle confidentiality, integrity, availability issues
            
            5. **Incident detection:**
               - Detection of unauthorized access
               - Investigation procedures
               - Remediation measures
               - Prevent recurrence
            
            6. **Data Processor contracts:**
               - Security safeguards in contracts
               - Processor compliance requirements
            
            **Penalty:** Rs. 250 crore
            """)
        
        with st.expander("Rule 7 - Breach Notification", expanded=False):
            st.markdown("""
            **On becoming aware of a breach, Data Fiduciary must:**
            
            **To Data Principals (immediately):**
            - Description of breach
            - Possible consequences
            - Measures already implemented
            - Safety measures Data Principal may take
            - Business contact information
            
            **To Data Protection Board:**
            - **Without delay:** Description of breach
            - **Within 72 hours:**
              - Updated information
              - Broad facts of breach
              - Measures to mitigate adverse effects
              - Findings on who caused breach
              - Remedial measures taken
              - Report on intimations sent to Data Principals
            
            **Penalty:** Rs. 200 crore
            """)
        
        with st.expander("Rule 9 - Contact Information", expanded=False):
            st.markdown("""
            **Every Data Fiduciary must:**
            
            Prominently publish on website and mobile app (if any):
            - Contact information of person who can answer questions about 
              processing of personal data
            
            **Penalty:** Rs. 50 crore
            """)
        
        with st.expander("Rule 10 - Children's Data", expanded=False):
            st.markdown("""
            **Special protections for children (under 18):**
            
            1. **Prohibited activities:**
               - Tracking or behavioral monitoring of children
               - Targeted advertising directed at children
            
            2. **Required:**
               - Verifiable consent of parent or guardian
               - Age verification mechanism
            
            3. **Exceptions:**
               - Children between 13-18 may consent themselves
               - For certain specified purposes (health, education)
            
            **Penalty:** Rs. 200 crore
            """)
        
        with st.expander("Rule 14 - Rights of Data Principals", expanded=False):
            st.markdown("""
            **Data Principals have right to:**
            
            1. **Access** their personal data
            2. **Correct** inaccurate or incomplete data
            3. **Erase** personal data
            4. **Data portability** (to another Data Fiduciary)
            5. **Grievance redressal**
            
            **Data Fiduciary must:**
            - Publish details of means to make requests
            - Respond within reasonable time (suggest: 30 days)
            - Establish grievance redressal mechanism
            - Respond to grievances within 90 days (extended to 180 days)
            
            **Penalty:** Rs. 50 crore
            """)
    
    with tab4:
        st.header("Penalty Schedule")
        
        st.markdown("""
        ### Section 33 - Penalties
        
        The Data Protection Board may impose penalties for violations:
        """)
        
        penalty_data = {
            'Violation': [
                'Security breach (Rule 6)',
                'Breach notification failure (Rule 7)',
                "Children's data violations (Rule 10)",
                'SDF obligations (Rule 13)',
                'General violations (Notice, Rights)',
                'Processing without valid consent',
                'Failure to implement technical measures',
                'Non-compliance with Board orders'
            ],
            'Penalty (Rs. Crore)': [
                '250',
                '200',
                '200',
                '150',
                '50',
                '50',
                '50',
                'Up to 250'
            ],
            'Reference': [
                'Section 8(5)',
                'Section 8(6)',
                'Section 9',
                'Section 10',
                'Section 6, 11',
                'Section 6',
                'Section 8',
                'Section 33(1)'
            ]
        }
        
        df_penalties = pd.DataFrame(penalty_data)
        st.dataframe(df_penalties, use_container_width=True, hide_index=True)
        
        st.warning("""
        **Important:** Penalties are imposed per violation. Multiple violations 
        can result in cumulative penalties.
        """)
    
    with tab5:
        st.header("Compliance Checklist")
        
        st.markdown("""
        ### Universal Requirements (All Businesses)
        
        Use this checklist to track your compliance progress:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Notice & Consent:**
            - [ ] Privacy notice published on website/app
            - [ ] Notice in clear and plain language
            - [ ] Itemized description of data processing
            - [ ] Purpose of processing clearly stated
            - [ ] Consent mechanism implemented
            - [ ] Links to withdraw consent provided
            
            **Security:**
            - [ ] Data encryption implemented
            - [ ] Access control mechanisms in place
            - [ ] Logging and monitoring system active
            - [ ] Logs retained for minimum 1 year
            - [ ] Backup and recovery procedures
            - [ ] Incident detection system
            
            **Breach Response:**
            - [ ] Breach response plan documented
            - [ ] Notification procedures to Data Principals
            - [ ] Notification procedures to Board (72 hours)
            - [ ] Breach investigation process
            - [ ] Remediation procedures
            """)
        
        with col2:
            st.markdown("""
            **Rights & Grievances:**
            - [ ] Data access request process
            - [ ] Data correction mechanism
            - [ ] Data deletion process
            - [ ] Data portability support
            - [ ] Grievance redressal system
            - [ ] 90-day response timeline
            
            **Transparency:**
            - [ ] Contact information published
            - [ ] Person designated to answer queries
            - [ ] Data processing purposes documented
            
            **Conditional Requirements:**
            - [ ] Third Schedule compliance (if applicable)
            - [ ] Children's data protections (if applicable)
            - [ ] Parental consent verification (if applicable)
            - [ ] Cross-border transfer compliance (if applicable)
            - [ ] Data Processor contracts (if applicable)
            - [ ] SDF requirements (if notified)
            """)
        
        st.info("""
        **Deadline:** All requirements must be complied with by **May 13, 2027**
        """)
    
    st.markdown("---")
    
    # Resources
    st.header("Additional Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Official Sources
        
        - [DPDP Act 2023 - Full Text](https://www.meity.gov.in/dpdpa)
        - [DPDP Rules 2025](https://www.meity.gov.in/dpdpa-rules)
        - [Data Protection Board](https://www.dpb.gov.in)
        - [MEITY Website](https://www.meity.gov.in)
        """)
    
    with col2:
        st.markdown("""
        ### Compliance Support
        
        - Complete assessment in "New Assessment" page
        - View your gaps in "View Results" page
        - Download detailed Excel reports
        - Track progress over time
        """)
    
    st.markdown("---")
    st.caption("This is a quick reference guide. For legal advice, consult a qualified professional.")

if __name__ == "__main__":
    show()