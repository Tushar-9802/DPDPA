"""
Legal constants for DPDP Act document generation.
Maps data types, retention requirements, and legal bases.
"""

# Human-readable names for data types
DATA_TYPE_DISPLAY_NAMES = {
    'name': 'Full Name',
    'email': 'Email Address',
    'phone': 'Phone Number',
    'address': 'Physical Address',
    'payment_info': 'Payment/Financial Information',
    'health_data': 'Health/Medical Records',
    'biometric': 'Biometric Data (fingerprint, facial recognition)',
    'location': 'Location/GPS Data',
    'behavioral': 'Behavioral/Usage Patterns',
    'device_info': 'Device Information',
    'ip_address': 'IP Address',
    'cookies': 'Cookies and Tracking Data'
}

# Legal retention requirements by data type
RETENTION_REQUIREMENTS = {
    # Statutory requirements
    'payment_info': '7 years (Income Tax Act, 1961)',
    'health_data': '10 years (Clinical Establishments Act, 2010)',
    'employment': '3 years (Labour Laws)',
    
    # Third Schedule requirements (applied conditionally)
    'third_schedule_ecommerce': '3 years from account closure',
    'third_schedule_gaming': '3 years from last activity',
    
    # Default DPDP requirement
    'default': 'Until purpose completion or consent withdrawal'
}

# Legal basis for processing under DPDP Act
LEGAL_BASIS_MAP = {
    'consent': 'Consent of Data Principal (Section 6)',
    'contract': 'Performance of contract (Section 7(a))',
    'legal_obligation': 'Compliance with legal obligation (Section 7(b))',
    'vital_interests': 'Protection of life or health of Data Principal (Section 7(c))',
    'public_function': 'Function of the State (Section 7(d))',
    'legitimate_interests': 'Legitimate use (Section 7(e))'
}

# Entity types for validation
VALID_ENTITY_TYPES = [
    'startup',
    'smb',
    'ecommerce',
    'social_media',
    'fintech',
    'healthcare',
    'edtech',
    'gaming',
    'other'
]

# Third Schedule thresholds (user counts)
THIRD_SCHEDULE_THRESHOLDS = {
    'ecommerce': 20_000_000,
    'social_media': 20_000_000,
    'gaming': 5_000_000
}

# Detailed data type descriptions for consent forms
DATA_TYPE_DETAILED_DESCRIPTIONS = {
    'name': 'Full Name (first name, middle name, last name)',
    'email': 'Email Address (for account management and communication)',
    'phone': 'Phone Number (for verification, contact, and support)',
    'address': 'Physical Address (billing address, shipping address)',
    'payment_info': 'Payment Information (credit/debit card details, UPI ID, transaction history)',
    'health_data': 'Health/Medical Data (health conditions, medical history, prescriptions)',
    'biometric': 'Biometric Data (fingerprints, facial recognition data, iris scans)',
    'location': 'Location Data (GPS coordinates, IP address geolocation)',
    'behavioral': 'Usage/Behavioral Data (browsing history, app usage patterns, preferences)',
    'device_info': 'Device Information (device model, operating system, browser type)',
    'ip_address': 'IP Address (for security and analytics)',
    'cookies': 'Cookies and Tracking Data (session cookies, tracking pixels)'
}