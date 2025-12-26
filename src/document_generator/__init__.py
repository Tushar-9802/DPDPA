"""
DPDPA Document Generator Package
Generates DPDP-compliant legal document templates from business profiles.
"""

from .generator import DocumentGenerator, DocumentGenerationError
from .constants import DATA_TYPE_DISPLAY_NAMES, RETENTION_REQUIREMENTS, LEGAL_BASIS_MAP
from .validators import validate_profile, sanitize_input, ValidationError

__all__ = [
    'DocumentGenerator',
    'DocumentGenerationError',
    'validate_profile',
    'sanitize_input',
    'ValidationError',
    'DATA_TYPE_DISPLAY_NAMES',
    'RETENTION_REQUIREMENTS',
    'LEGAL_BASIS_MAP'
]

__version__ = '1.0.0'