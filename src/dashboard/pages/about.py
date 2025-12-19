"""
About Page - DPDPA Compliance Dashboard
Project information and credits
"""

import streamlit as st

def show():
    """Render about page"""
    
    st.title("About This Project")
    
    st.markdown("""
    ## DPDPA Compliance Dashboard
    
    An automated compliance assessment tool for India's **Digital Personal Data Protection Act, 2023**.
    
    ### Purpose
    
    This dashboard helps **Indian startups and SMBs** navigate the complex requirements of DPDP Act 2023 
    by providing:
    
    - Automated compliance gap analysis
    - Personalized requirement matching
    - Penalty exposure calculation
    - Priority-based roadmap
    - Downloadable compliance reports
    
    ### Data Sources
    
    All requirements extracted from official government documents:
    
    - **DPDP Act 2023** (Enacted August 11, 2023)
    - **DPDP Rules 2025** (Notified November 13, 2025)
    - **Section 33 Penalty Schedule**
    - **Third Schedule** (Data retention requirements)
    
    ### Legal Disclaimer
    
    **This tool provides automated guidance only.**
    
    - Not a substitute for professional legal advice
    - Consult a qualified data protection lawyer for compliance strategy
    - Laws and rules may change - monitor MEITY website for updates
    - Final compliance responsibility lies with your organization
    
    ### Technical Stack
    
    - **Backend:** Python 3.13
    - **Database:** SQLite
    - **Frontend:** Streamlit
    - **PDF Extraction:** PyMuPDF
    - **Reports:** pandas, openpyxl
    
    ### Compliance Deadline
    
    **May 13, 2027** - 18 months from DPDP Rules 2025 notification date
    
    ### Target Audience
    
    - Startups processing Indian user data
    - Small and Medium Businesses (SMBs)
    - E-commerce platforms
    - Gaming companies
    - Fintech applications
    - SaaS businesses
    - Digital service providers
    
    ### Key Features
    
    **1. Smart Requirement Matching**
    - Identifies 36 universal requirements (apply to all)
    - Detects Third Schedule threshold breaches
    - Flags children's data processing requirements
    - Identifies cross-border transfer obligations
    - Calculates penalty exposure
    
    **2. Illegal Activity Detection**
    - Automatically detects DPDP Act Section 9(3) violations
    - Flags behavioral tracking of children
    - Flags targeted advertising to children
    - Shows Rs. 200 crore penalty warnings
    
    **3. Priority Scoring**
    - Weighted formula: 40% penalty + 30% urgency + 30% complexity
    - Helps focus on highest-risk items first
    - Considers May 13, 2027 deadline
    
    **4. Comprehensive Reporting**
    - Console reports
    - Excel exports with 4 sheets
    - Summary metrics
    - Detailed requirement lists
    
    ### Contact & Support
    
    This is an open-source compliance tool built for the Indian startup ecosystem.
    
    **For questions about:**
    - The tool itself: Check README.md in repository
    - DPDP Act compliance: Consult a legal professional
    - Technical implementation: Refer to source code documentation
    
    ### Privacy Notice
    
    **Your data stays local:**
    - All assessments stored in local SQLite database
    - No data sent to external servers
    - You control all business information
    - Export and delete assessments anytime
    
    ### License & Credits
    
    **Built for:** Indian Startups & SMBs
    
    **Purpose:** DPDP Act 2023 compliance assistance
    
    **Disclaimer:** Educational and informational use only
    
    ---
    
    ### Getting Started
    
    1. Click **"Start New Assessment"** in the sidebar
    2. Answer 15 questions about your business
    3. Get instant compliance report
    4. Download Excel roadmap
    5. Track progress over time
    
    ### Quick Facts
    
    - **50+ requirements** extracted from official rules
    - **6 penalty categories** (Rs. 10,000 to Rs. 250 crore)
    - **5 entity types** with specific thresholds
    - **3 Third Schedule** classes (e-commerce, gaming, social media)
    - **509 days** to compliance deadline (as of today)
    
    ---
    
    **Remember:** May 13, 2027 is a hard deadline. Start your compliance journey today!
    """)
    
    st.markdown("---")
    st.caption("Built for Indian Startups & SMBs | Educational Tool")

if __name__ == "__main__":
    show()