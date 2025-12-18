"""
DPDPA Compliance Assessment - Business Profiler Module
Saves assessment answers to business_profiles table

Usage:
    from src.assessment.business_profiler import create_business_profile
    business_id = create_business_profile(answers)
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import DB_PATH


def create_business_profile(answers: Dict[str, Any]) -> int:
    """
    Save business profile to database
    
    Args:
        answers: Dictionary from questionnaire.run_questionnaire()
        
    Returns:
        business_profile_id: Primary key of inserted record
    """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Extract core fields (match business_profiles schema)
        business_name = answers.get('business_name', 'Unknown')
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
            'has_grievance_system': answers.get('has_grievance_system', False)
        }
        
        # Check if business_profiles table has extended_data column
        cursor.execute("PRAGMA table_info(business_profiles)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'extended_data' in columns:
            # Insert with extended_data column
            cursor.execute("""
                INSERT INTO business_profiles (
                    business_name,
                    entity_type,
                    user_count,
                    processes_children_data,
                    cross_border_transfers,
                    assessment_score,
                    extended_data,
                    created_at,
                    last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                business_name,
                entity_type,
                user_count,
                1 if processes_children_data else 0,
                1 if cross_border_transfers else 0,
                0.0,  # Initial score
                json.dumps(extended_data),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
        else:
            # Add extended_data column first
            try:
                cursor.execute("""
                    ALTER TABLE business_profiles
                    ADD COLUMN extended_data TEXT
                """)
                conn.commit()
                print("✓ Added extended_data column to business_profiles")
            except sqlite3.OperationalError:
                # Column already exists, that's fine
                pass
            
            # Now insert with extended_data
            cursor.execute("""
                INSERT INTO business_profiles (
                    business_name,
                    entity_type,
                    user_count,
                    processes_children_data,
                    cross_border_transfers,
                    assessment_score,
                    extended_data,
                    created_at,
                    last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                business_name,
                entity_type,
                user_count,
                1 if processes_children_data else 0,
                1 if cross_border_transfers else 0,
                0.0,
                json.dumps(extended_data),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
        
        business_id = cursor.lastrowid
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


def get_business_profile(business_id: int) -> Dict[str, Any]:
    """
    Retrieve business profile from database
    
    Args:
        business_id: Primary key
        
    Returns:
        Dictionary with business profile data
    """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                id,
                business_name,
                entity_type,
                user_count,
                processes_children_data,
                cross_border_transfers,
                assessment_score,
                created_at,
                last_updated
            FROM business_profiles
            WHERE id = ?
        """, (business_id,))
        
        row = cursor.fetchone()
        
        if not row:
            raise ValueError(f"Business profile {business_id} not found")
        
        profile = {
            'id': row[0],
            'business_name': row[1],
            'entity_type': row[2],
            'user_count': row[3],
            'processes_children_data': bool(row[4]),
            'cross_border_transfers': bool(row[5]),
            'assessment_score': row[6],
            'created_at': row[7],
            'last_updated': row[8]
        }
        
        # Try to get extended data
        cursor.execute("PRAGMA table_info(business_profiles)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'extended_data' in columns:
            cursor.execute("""
                SELECT extended_data
                FROM business_profiles
                WHERE id = ?
            """, (business_id,))
            extended_json = cursor.fetchone()[0]
            if extended_json:
                profile['extended_data'] = json.loads(extended_json)
        else:
            # Get from attributes table
            cursor.execute("""
                SELECT attribute_name, attribute_value
                FROM business_profile_attributes
                WHERE business_profile_id = ?
            """, (business_id,))
            
            extended_data = {}
            for attr_name, attr_value in cursor.fetchall():
                extended_data[attr_name] = json.loads(attr_value)
            
            profile['extended_data'] = extended_data
        
        return profile
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        raise
    finally:
        conn.close()


def update_assessment_score(business_id: int, score: float) -> None:
    """
    Update compliance assessment score
    
    Args:
        business_id: Primary key
        score: Compliance score (0-100)
    """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE business_profiles
            SET assessment_score = ?,
                last_updated = ?
            WHERE id = ?
        """, (score, datetime.now().isoformat(), business_id))
        
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
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                id,
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
    
    conn = sqlite3.connect(DB_PATH)
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
                business_profile_id INTEGER NOT NULL,
                attribute_name TEXT NOT NULL,
                attribute_value TEXT,
                FOREIGN KEY (business_profile_id) REFERENCES business_profiles(id),
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
    print(f"  Type: {profile['entity_type']}")
    print(f"  Users: {profile['user_count']:,}")
    if 'extended_data' in profile:
        print(f"  Extended data keys: {list(profile['extended_data'].keys())}")
    print()
    
    # List all profiles
    print("All business profiles:")
    profiles = list_business_profiles()
    for p in profiles:
        print(f"  {p['id']:3d}. {p['business_name']:30s} ({p['entity_type']}) - {p['assessment_score']:.1f}%")
    print()
    
    print("="*70)
    print("✓ Business profiler working correctly")
    print("="*70)