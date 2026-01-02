"""
DPDPA Compliance Assessment - Business Profiler Module
Saves assessment answers to business_profiles table

Usage:
    from src.assessment.business_profiler import create_business_profile
    business_id = create_business_profile(answers)
"""

import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import DB_PATH


def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)


def create_business_profile(answers: Dict[str, Any]) -> str:
    """
    Save business profile to database
    
    Args:
        answers: Dictionary from questionnaire including:
                - business_name, business_address, business_email, business_phone
                - entity_type, user_count, etc.
        
    Returns:
        business_id: UUID string of inserted record
    """
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Generate unique ID
        business_id = str(uuid.uuid4())
        
        # Extract core fields (match business_profiles schema)
        business_name = answers.get('business_name', 'Unknown')
        business_address = answers.get('business_address', '')
        business_email = answers.get('business_email', '')
        business_phone = answers.get('business_phone', '')
        entity_type = answers.get('entity_type', 'other')
        user_count = answers.get('user_count', 0)
        processes_children_data = answers.get('processes_children_data', False)
        cross_border_transfers = answers.get('cross_border_transfers', False)
        
        # Extended fields stored as JSON
        extended_data = {
            'data_types': answers.get('data_types', []),
            'uses_ai': answers.get('uses_ai'),
            'annual_revenue': answers.get('annual_revenue'),
            'has_processors': answers.get('has_processors', False),
            'current_security': answers.get('current_security', []),
            'has_breach_plan': answers.get('has_breach_plan', False),
            'tracks_behavior': answers.get('tracks_behavior', False),
            'targeted_advertising': answers.get('targeted_advertising', False),
            'has_consent_mechanism': answers.get('has_consent_mechanism', False),
            'has_grievance_system': answers.get('has_grievance_system', False),
            'processes_children_data': processes_children_data,
            'cross_border_transfers': cross_border_transfers
        }
        
        # Check if business_profiles table has the new contact columns
        cursor.execute("PRAGMA table_info(business_profiles)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'business_address' in columns:
            # New schema with contact fields
            cursor.execute("""
                INSERT INTO business_profiles (
                    business_id,
                    business_name,
                    business_address,
                    business_email,
                    business_phone,
                    entity_type,
                    user_count,
                    extended_data,
                    assessment_score,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                business_id,
                business_name,
                business_address,
                business_email,
                business_phone,
                entity_type,
                user_count,
                json.dumps(extended_data),
                0.0,  # Initial score
                datetime.now().isoformat()
            ))
        else:
            # Old schema without contact fields
            cursor.execute("""
                INSERT INTO business_profiles (
                    business_id,
                    business_name,
                    entity_type,
                    user_count,
                    extended_data,
                    assessment_score,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                business_id,
                business_name,
                entity_type,
                user_count,
                json.dumps(extended_data),
                0.0,
                datetime.now().isoformat()
            ))
        
        conn.commit()
        
        print(f"✓ Business profile created (ID: {business_id})")
        print(f"  Name: {business_name}")
        print(f"  Type: {entity_type}")
        print(f"  Users: {user_count:,}")
        
        return business_id
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
        raise
    except Exception as e:
        print(f"❌ Error creating business profile: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def get_business_profile(business_id: str) -> Dict[str, Any]:
    """
    Retrieve business profile from database
    
    Args:
        business_id: UUID string
        
    Returns:
        Dictionary with business profile data including contact fields
    """
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check which columns exist
        cursor.execute("PRAGMA table_info(business_profiles)")
        columns = [col[1] for col in cursor.fetchall()]
        
        has_contact_fields = 'business_address' in columns
        
        if has_contact_fields:
            # New schema with contact fields
            cursor.execute("""
                SELECT 
                    business_id,
                    business_name,
                    business_address,
                    business_email,
                    business_phone,
                    entity_type,
                    user_count,
                    created_at,
                    extended_data,
                    assessment_score
                FROM business_profiles
                WHERE business_id = ?
            """, (business_id,))
        else:
            # Old schema without contact fields
            cursor.execute("""
                SELECT 
                    business_id,
                    business_name,
                    entity_type,
                    user_count,
                    created_at,
                    extended_data,
                    assessment_score
                FROM business_profiles
                WHERE business_id = ?
            """, (business_id,))
        
        row = cursor.fetchone()
        
        if not row:
            raise ValueError(f"Business profile {business_id} not found")
        
        if has_contact_fields:
            profile = {
                'id': row[0],
                'business_name': row[1],
                'business_address': row[2],
                'business_email': row[3],
                'business_phone': row[4],
                'entity_type': row[5],
                'user_count': row[6],
                'created_at': row[7],
                'assessment_score': row[9]
            }
            extended_json = row[8]
        else:
            profile = {
                'id': row[0],
                'business_name': row[1],
                'entity_type': row[2],
                'user_count': row[3],
                'created_at': row[4],
                'assessment_score': row[6]
            }
            extended_json = row[5]
        
        # Parse extended data
        if extended_json:
            try:
                extended = json.loads(extended_json)
                profile['extended_data'] = extended
                # Also merge extended data into top level for convenience
                profile.update(extended)
            except json.JSONDecodeError:
                profile['extended_data'] = {}
        else:
            profile['extended_data'] = {}
        
        return profile
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        raise
    finally:
        conn.close()


def update_assessment_score(business_id: str, score: float) -> None:
    """
    Update compliance assessment score
    
    Args:
        business_id: UUID string
        score: Compliance score (0-100)
    """
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE business_profiles
            SET assessment_score = ?
            WHERE business_id = ?
        """, (score, business_id))
        
        conn.commit()
        print(f"✓ Updated assessment score to {score:.1f}%")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def list_business_profiles() -> list:
    """
    List all business profiles
    
    Returns:
        List of dictionaries with profile summaries
    """
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check which columns exist
        cursor.execute("PRAGMA table_info(business_profiles)")
        columns = [col[1] for col in cursor.fetchall()]
        
        has_contact_fields = 'business_address' in columns
        
        if has_contact_fields:
            cursor.execute("""
                SELECT 
                    business_id,
                    business_name,
                    entity_type,
                    user_count,
                    assessment_score,
                    created_at
                FROM business_profiles
                ORDER BY created_at DESC
            """)
        else:
            cursor.execute("""
                SELECT 
                    business_id,
                    business_name,
                    entity_type,
                    user_count,
                    assessment_score,
                    created_at
                FROM business_profiles
                ORDER BY created_at DESC
            """)
        
        profiles = []
        for row in cursor.fetchall():
            profiles.append({
                'id': row[0],
                'business_name': row[1],
                'entity_type': row[2],
                'user_count': row[3],
                'assessment_score': row[4],
                'created_at': row[5]
            })
        
        return profiles
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        raise
    finally:
        conn.close()


def ensure_extended_data_support():
    """
    Add extended_data column to business_profiles if missing
    Also create business_profile_attributes table as fallback
    """
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if extended_data column exists
        cursor.execute("PRAGMA table_info(business_profiles)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'extended_data' not in columns:
            print("Adding extended_data column to business_profiles...")
            cursor.execute("""
                ALTER TABLE business_profiles
                ADD COLUMN extended_data TEXT
            """)
            conn.commit()
            print("✓ Added extended_data column")
        
        # Create attributes table as alternative storage
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS business_profile_attributes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_profile_id TEXT NOT NULL,
                attribute_name TEXT NOT NULL,
                attribute_value TEXT,
                FOREIGN KEY (business_profile_id) REFERENCES business_profiles(business_id),
                UNIQUE(business_profile_id, attribute_name)
            )
        """)
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"⚠️  Could not add extended_data support: {e}")
        print("   Using business_profile_attributes table instead")
    finally:
        conn.close()


# For testing
if __name__ == "__main__":
    print("="*70)
    print("BUSINESS PROFILER - TEST MODE")
    print("="*70)
    print()
    
    # Ensure database is ready
    print("Checking database schema...")
    ensure_extended_data_support()
    print()
    
    # Create sample profile
    sample_answers = {
        'business_name': 'Test Corp',
        'business_address': '123 Test Street, Test City, Test State 123456',
        'business_email': 'test@testcorp.com',
        'business_phone': '+91-80-12345678',
        'entity_type': 'startup',
        'user_count': 50000,
        'processes_children_data': False,
        'cross_border_transfers': True,
        'data_types': ['email', 'phone'],
        'uses_ai': True,
        'annual_revenue': '1-10 crore',
        'has_processors': True,
        'current_security': ['encryption'],
        'has_breach_plan': False,
        'tracks_behavior': True,
        'targeted_advertising': False,
        'has_consent_mechanism': True,
        'has_grievance_system': False
    }
    
    print("Creating test business profile...")
    business_id = create_business_profile(sample_answers)
    print()
    
    # Retrieve it
    print("Retrieving business profile...")
    profile = get_business_profile(business_id)
    print(f"✓ Retrieved profile: {profile['business_name']}")
    print(f"  Address: {profile.get('business_address', 'N/A')}")
    print(f"  Email: {profile.get('business_email', 'N/A')}")
    print(f"  Phone: {profile.get('business_phone', 'N/A')}")
    print(f"  Type: {profile['entity_type']}")
    print(f"  Users: {profile['user_count']:,}")
    if 'extended_data' in profile:
        print(f"  Extended data keys: {list(profile['extended_data'].keys())}")
    print()
    
    # List all profiles
    print("All business profiles:")
    profiles = list_business_profiles()
    for p in profiles:
        print(f"  {p['business_name']:30s} ({p['entity_type']}) - {p.get('assessment_score', 0):.1f}%")
    print()
    
    print("="*70)
    print("✓ Business profiler working correctly")
    print("="*70)