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

# Initialize dark mode state
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False

# Custom CSS - Dynamic based on dark mode
if st.session_state['dark_mode']:
    # Dark mode colors
    st.markdown("""
    <style>
        /* Dark mode styling */
        .stApp {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        
        /* Set Arial font globally */
        * {
            font-family: Arial, sans-serif;
        }
        
        /* Main content area */
        .main {
            padding: 2rem;
            background-color: #1a1a1a;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #262626;
        }
        
        [data-testid="stSidebar"] * {
            color: #e0e0e0 !important;
        }
        
        /* Remove Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            font-family: Arial, sans-serif;
            font-weight: 600;
            color: #e0e0e0;
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            color: #e0e0e0;
        }
        
        [data-testid="stMetricLabel"] {
            color: #b0b0b0;
        }
        
        /* Buttons */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            font-family: Arial, sans-serif;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39,174,96,0.4);
        }
        
        /* Input fields */
        .stTextInput>div>div>input,
        .stSelectbox>div>div>select,
        .stNumberInput>div>div>input {
            background-color: #262626;
            color: #e0e0e0;
            border-color: #404040;
        }
        
        /* Dataframes and tables */
        .dataframe {
            font-family: Arial, sans-serif;
            background-color: #262626;
            color: #e0e0e0;
        }
        
        /* Info/warning/error boxes */
        .stAlert {
            font-family: Arial, sans-serif;
            background-color: #262626;
            border-color: #404040;
        }
        
        /* Expanders */
        [data-testid="stExpander"] {
            background-color: #262626;
            border-color: #404040;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #262626;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #b0b0b0;
        }
        
        .stTabs [aria-selected="true"] {
            color: #667eea;
        }
        
        /* Markdown text */
        .stMarkdown {
            color: #e0e0e0;
        }
        
        /* Links */
        a {
            color: #667eea;
        }
        
        a:hover {
            color: #764ba2;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    # Light mode colors (original)
    st.markdown("""
    <style>
        /* Set Arial font globally */
        * {
            font-family: Arial, sans-serif;
        }
        
        /* Main content area */
        .main {
            padding: 2rem;
        }
        
        /* Remove Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            font-family: Arial, sans-serif;
            font-weight: 600;
        }
        
        /* Metric cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 8px;
            color: white;
            margin: 1rem 0;
        }
        
        /* Buttons */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            font-family: Arial, sans-serif;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39,174,96,0.3);
        }
        
        /* Tables */
        .dataframe {
            font-family: Arial, sans-serif;
        }
        
        /* Warning boxes */
        .stAlert {
            font-family: Arial, sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("DPDPA Compliance")
st.sidebar.markdown("---")

# Dark mode toggle at top of sidebar
col1, col2 = st.sidebar.columns([3, 1])
with col1:
    st.markdown("**Theme:**")
with col2:
    if st.button("🌙" if not st.session_state['dark_mode'] else "☀️", key="theme_toggle"):
        st.session_state['dark_mode'] = not st.session_state['dark_mode']
        st.rerun()

st.sidebar.markdown("---")

# Get query params to determine page
query_params = st.query_params
current_page = query_params.get("page", "home")

# Navigation buttons (not radio - more reliable)
st.sidebar.markdown("### Navigation")

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

if st.sidebar.button("DPDPA Reference", use_container_width=True, type="primary" if current_page == "reference" else "secondary", key="nav_reference"):
    st.query_params["page"] = "reference"
    st.rerun()

if st.sidebar.button("About", use_container_width=True, type="primary" if current_page == "about" else "secondary", key="nav_about"):
    st.query_params["page"] = "about"
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Compliance Deadline
**May 13, 2027**

18 months from DPDP Rules 2025 notification
""")

# Calculate days remaining
from datetime import datetime
deadline = datetime(2027, 5, 13)
days_left = (deadline - datetime.now()).days

if days_left > 365:
    st.sidebar.success(f"{days_left} days remaining")
elif days_left > 180:
    st.sidebar.warning(f"{days_left} days remaining")
else:
    st.sidebar.error(f"{days_left} days remaining")

st.sidebar.markdown("---")
st.sidebar.caption("Built for Indian Startups & SMBs")

# Route to pages based on query params
if current_page == "home":
    from src.dashboard.pages import home
    home.show()
elif current_page == "assessment":
    from src.dashboard.pages import assessment
    assessment.show()
elif current_page == "results":
    from src.dashboard.pages import results
    results.show()
elif current_page == "reference":
    from src.dashboard.pages import dpdpa_reference
    dpdpa_reference.show()
elif current_page == "about":
    from src.dashboard.pages import about
    about.show()
else:
    # Default to home if invalid page
    st.query_params["page"] = "home"
    st.rerun()