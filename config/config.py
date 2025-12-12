"""
Configuration for DPDPA Compliance Dashboard
"""

from pathlib import Path
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
TESTS_DIR = PROJECT_ROOT / "tests"

# Database
DATABASE_PATH = PROCESSED_DATA_DIR / "dpdpa_compliance.db"

# Official PDF URLs
DPDP_RULES_2025_URL = "https://dpdpa.com/DPDP_Rules_2025_English_only.pdf"
DPDP_ACT_2023_URL = "https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf"

# PDF file paths
RULES_PDF_PATH = RAW_DATA_DIR / "DPDP_Rules_2025.pdf"
ACT_PDF_PATH = RAW_DATA_DIR / "DPDP_Act_2023.pdf"

# Key dates
RULES_NOTIFICATION_DATE = datetime(2025, 11, 13)
CONSENT_MANAGER_DEADLINE = datetime(2026, 11, 13)  # 12 months
FULL_COMPLIANCE_DEADLINE = datetime(2027, 5, 13)   # 18 months

# Extraction parameters
MIN_REQUIREMENT_LENGTH = 20  # Characters
MAX_REQUIREMENT_LENGTH = 1000
OBLIGATION_KEYWORDS = [
    "shall", "must", "required", "obligation", "duty", 
    "mandatory", "necessary", "ensure", "implement"
]

# Rule patterns (regex)
RULE_NUMBER_PATTERN = r"Rule\s+\d+(?:\(\d+\))?(?:\([a-z]\))?"
SECTION_NUMBER_PATTERN = r"Section\s+\d+(?:\(\d+\))?(?:\([a-z]\))?"
SCHEDULE_PATTERN = r"(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh)\s+Schedule"

# Assessment configuration
ASSESSMENT_QUESTIONS_COUNT = 15
PRIORITY_SCORE_WEIGHTS = {
    "penalty_weight": 0.4,
    "deadline_weight": 0.3,
    "complexity_weight": 0.3
}

# Third Schedule thresholds (from Rules)
THIRD_SCHEDULE_THRESHOLDS = {
    "ecommerce": 20_000_000,      # 2 crore users
    "social_media": 20_000_000,   # 2 crore users
    "online_gaming": 5_000_000    # 50 lakh users
}

# Data retention periods
MANDATORY_LOG_RETENTION_DAYS = 365  # 1 year minimum (Rule 6(1)(e))
THIRD_SCHEDULE_RETENTION_YEARS = 3   # For qualifying entities

# Penalty structure (in crores INR)
PENALTIES = {
    "security_breach": 250,
    "breach_notification": 200,
    "children_data": 200,
    "sdf_obligations": 150,
    "general_violations": 50,
    "data_principal_duty": 0.001  # ₹10,000
}

# Entity types
ENTITY_TYPES = [
    "startup",
    "smb",
    "ecommerce",
    "social_media",
    "fintech",
    "healthcare",
    "edtech",
    "gaming",
    "other"
]

# Obligation categories
OBLIGATION_TYPES = [
    "consent",
    "notice",
    "security",
    "breach",
    "rights",
    "retention",
    "sdf",
    "children",
    "cross_border",
    "consent_manager"
]

# Document template types
DOCUMENT_TYPES = [
    "privacy_notice",
    "consent_notice",
    "breach_notification_dp",
    "breach_notification_board",
    "retention_policy",
    "dpa",
    "security_checklist",
    "dpia",
    "children_consent"
]

# Streamlit configuration
# Application metadata
APP_TITLE = "DPDPA Compliance Dashboard"
APP_ICON = "🔒"
VERSION = "0.1.0-alpha"

# Official document URLs
DPDP_RULES_2025_URL = "https://dpdpa.com/DPDP_Rules_2025_English_only.pdf"
DPDP_ACT_2023_URL = "https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf"

# Key dates
from datetime import datetime, timedelta
RULES_NOTIFICATION_DATE = datetime(2025, 11, 13)
CONSENT_MANAGER_DEADLINE = RULES_NOTIFICATION_DATE + timedelta(days=365)
FULL_COMPLIANCE_DEADLINE = RULES_NOTIFICATION_DATE + timedelta(days=545)

# Third Schedule thresholds
THIRD_SCHEDULE_THRESHOLDS = {
    "ecommerce": 20_000_000,
    "social_media": 20_000_000,
    "gaming": 5_000_000
}

# Penalty amounts (Section 33 - in INR)
PENALTY_AMOUNTS = {
    "security_breach": 25_000_000_000,        # ₹250 crore
    "breach_notification": 20_000_000_000,    # ₹200 crore
    "children_data": 20_000_000_000,          # ₹200 crore
    "sdf_obligations": 15_000_000_000,        # ₹150 crore
    "general_violations": 5_000_000_000,      # ₹50 crore
    "data_principal_duties": 10_000           # ₹10,000
}

# Database path
DB_PATH = "data/processed/dpdpa_compliance.db"

# Legal disclaimer
LEGAL_DISCLAIMER = """
⚠️ **IMPORTANT LEGAL DISCLAIMER**

This tool provides compliance guidance based on DPDP Act 2023 and Rules 2025. 
It is **NOT** legal advice. Consult qualified legal counsel for compliance decisions.

**Limitations:**
- SDF designation criteria not yet specified by government
- No countries currently blacklisted for cross-border transfers
- Consent Manager registration process pending Board operationalization
"""

SDF_DISCLAIMER = """
**SDF Designation**: Criteria not yet fully specified by government. This assessment is indicative only.
"""

CROSS_BORDER_DISCLAIMER = """
**Cross-Border Transfers**: No countries currently blacklisted. Monitor MeitY notifications for restrictions.
"""

CHILDREN_DISCLAIMER = """
**Children's Data**: Complex verification requirements. Seek legal review for implementation.
"""

# Contact information
SUPPORT_EMAIL = ""  # To be filled
GITHUB_REPO = ""    # To be filled