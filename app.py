"""
DPDPA Compliance Dashboard
Interactive web application for DPDP Act 2023 compliance assessment

Deployment: Streamlit Cloud
Run locally: streamlit run app.py
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Page configuration
st.set_page_config(
    page_title="DPDPA Compliance Dashboard",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS - No dark mode, sharp edges, corporate colors
st.markdown("""
<style>
    /* Global font */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Main content area */
    .main {
        padding: 2rem;
        background-color: #ffffff;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Headers - Professional styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 600;
        color: #1a202c;
    }
    
    h1 {
        border-bottom: 3px solid #2c5282;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Buttons - Corporate blue */
    .stButton>button {
        width: 100%;
        background-color: #2c5282;
        color: white;
        border: none;
        padding: 0.6rem 1.25rem;
        border-radius: 2px;
        font-weight: 500;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        transition: background-color 0.2s;
        border: 1px solid #2c5282;
    }
    
    .stButton>button:hover {
        background-color: #1a365d;
        border-color: #1a365d;
    }
    
    /* Primary buttons */
    .stButton>button[kind="primary"] {
        background-color: #2c5282;
        border-color: #2c5282;
    }
    
    .stButton>button[kind="primary"]:hover {
        background-color: #1a365d;
        border-color: #1a365d;
    }
    
    /* Secondary buttons */
    .stButton>button[kind="secondary"] {
        background-color: #ffffff;
        color: #2c5282;
        border: 1px solid #cbd5e0;
    }
    
    .stButton>button[kind="secondary"]:hover {
        background-color: #f7fafc;
        border-color: #2c5282;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f7fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #1a202c;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input {
        border: 1px solid #cbd5e0;
        border-radius: 2px;
        padding: 0.5rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #2c5282;
        box-shadow: 0 0 0 1px #2c5282;
    }
    
    /* Dataframes */
    .dataframe {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        border: 1px solid #e2e8f0;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #1a202c;
        font-size: 1.75rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4a5568;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 2px;
        border-left-width: 4px;
    }
    
    /* Info boxes */
    .stAlert[data-baseweb="notification"][kind="info"] {
        background-color: #ebf8ff;
        border-left-color: #2c5282;
    }
    
    /* Success boxes */
    .stAlert[data-baseweb="notification"][kind="success"] {
        background-color: #f0fff4;
        border-left-color: #38a169;
    }
    
    /* Warning boxes */
    .stAlert[data-baseweb="notification"][kind="warning"] {
        background-color: #fffaf0;
        border-left-color: #dd6b20;
    }
    
    /* Error boxes */
    .stAlert[data-baseweb="notification"][kind="error"] {
        background-color: #fff5f5;
        border-left-color: #e53e3e;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        color: #4a5568;
        border-radius: 0;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #2c5282;
        border-bottom: 3px solid #2c5282;
    }
    
    /* Expanders */
    [data-testid="stExpander"] {
        border: 1px solid #e2e8f0;
        border-radius: 2px;
    }
    
    /* Links */
    a {
        color: #2c5282;
        text-decoration: none;
    }
    
    a:hover {
        color: #1a365d;
        text-decoration: underline;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background-color: #2c5282;
    }
    
    /* Download buttons */
    .stDownloadButton>button {
        background-color: #38a169;
        border-color: #38a169;
    }
    
    .stDownloadButton>button:hover {
        background-color: #2f855a;
        border-color: #2f855a;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #2c5282;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem 0; border-bottom: 1px solid #e2e8f0;'>
    <h2 style='margin: 0; color: #1a202c; font-size: 1.25rem;'>DPDPA Compliance</h2>
    <p style='margin: 0.25rem 0 0 0; color: #718096; font-size: 0.75rem;'>Assessment Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Get query params to determine page
query_params = st.query_params
current_page = query_params.get("page", "home")

# Navigation
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("**Navigation**")

if st.sidebar.button("Home", use_container_width=True, type="primary" if current_page == "home" else "secondary", key="nav_home"):
    st.query_params["page"] = "home"
    if 'selected_business_id' in st.session_state:
        del st.session_state['selected_business_id']
    st.rerun()

if st.sidebar.button("New Assessment", use_container_width=True, type="primary" if current_page == "assessment" else "secondary", key="nav_assessment"):
    st.query_params["page"] = "assessment"
    if 'current_assessment' in st.session_state:
        del st.session_state['current_assessment']
    if 'selected_business_id' in st.session_state:
        del st.session_state['selected_business_id']
    st.rerun()

if st.sidebar.button("View Results", use_container_width=True, type="primary" if current_page == "results" else "secondary", key="nav_results"):
    st.query_params["page"] = "results"
    st.rerun()

if st.sidebar.button("Generate Documents", use_container_width=True, type="primary" if current_page == "documents" else "secondary", key="nav_documents"):
    st.query_params["page"] = "documents"
    st.rerun()

if st.sidebar.button("DPDPA Reference", use_container_width=True, type="primary" if current_page == "reference" else "secondary", key="nav_reference"):
    st.query_params["page"] = "reference"
    st.rerun()

if st.sidebar.button("About", use_container_width=True, type="primary" if current_page == "about" else "secondary", key="nav_about"):
    st.query_params["page"] = "about"
    st.rerun()

st.sidebar.markdown("---")

# Compliance deadline
st.sidebar.markdown("""
<div style='padding: 1rem; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 2px;'>
    <p style='margin: 0 0 0.5rem 0; font-weight: 600; color: #1a202c; font-size: 0.9rem;'>Compliance Deadline</p>
    <p style='margin: 0; color: #2c5282; font-size: 1.25rem; font-weight: 700;'>May 13, 2027</p>
    <p style='margin: 0.25rem 0 0 0; color: #718096; font-size: 0.75rem;'>18 months from DPDP Rules notification</p>
</div>
""", unsafe_allow_html=True)

# Calculate days remaining
from datetime import datetime
deadline = datetime(2027, 5, 13)
days_left = (deadline - datetime.now()).days

if days_left > 365:
    st.sidebar.success(f"**{days_left} days** remaining")
elif days_left > 180:
    st.sidebar.warning(f"**{days_left} days** remaining")
else:
    st.sidebar.error(f"**{days_left} days** remaining")

st.sidebar.markdown("---")
st.sidebar.caption("Built for Indian Startups & SMBs")

# Route to pages
if current_page == "home":
    from src.dashboard.pages import home
    home.show()
elif current_page == "assessment":
    from src.dashboard.pages import assessment
    assessment.show()
elif current_page == "results":
    from src.dashboard.pages import results
    results.show()
elif current_page == "documents":
    from src.dashboard.pages import documents
    documents.show()
elif current_page == "reference":
    from src.dashboard.pages import dpdpa_ref
    dpdpa_ref.show()
elif current_page == "about":
    from src.dashboard.pages import about
    about.show()
else:
    # Default to home if invalid page
    st.query_params["page"] = "home"
    st.rerun()