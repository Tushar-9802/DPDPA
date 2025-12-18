"""
Requirements Extraction
Extracts requirements from parsed PDFs and inserts into database

"""

import re
import sqlite3
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import DB_PATH, RULES_NOTIFICATION_DATE, FULL_COMPLIANCE_DEADLINE

# Paths
PROCESSED_DATA_PATH = project_root / "data" / "processed"

# Penalty mapping: Rule → Penalty Category
PENALTY_MAP = {
    '6': 'security_breach',
    '7': 'breach_notification',
    '10': 'children_data',
    '11': 'children_data',
    '13': 'sdf_obligations',
    # Default to general_violations for other rules
}

def load_text_file(filename: str) -> str:
    """Load extracted text file"""
    filepath = PROCESSED_DATA_PATH / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def clean_text(text: str) -> str:
    """Remove page markers and noise"""
    # Remove page breaks
    text = re.sub(r'={70,}\s*\r?\n\s*PAGE \d+\s*\r?\n\s*={70,}\s*\r?\n', '\n', text)
    
    # Remove Hindi headings
    text = re.sub(r'\[भाग[^\]]*\]\s*\r?\n', '', text)
    text = re.sub(r'भारत का रािपत्र[^\n]*\r?\n', '', text)
    
    # Remove gazette headings (multi-line)
    text = re.sub(r'THE GAZETTE OF INDIA[^\n]*\r?\n[^\n]*\r?\n', '', text, flags=re.IGNORECASE)
    
    # Remove standalone page numbers
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Normalize whitespace but preserve structure
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
    text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines to double
    
    return text

def extract_rules(text: str) -> list:
    """
    Extract individual rules with their content (Rules 1-16 only, exclude schedules)
    
    Returns: List of (rule_number, title, content) tuples
    """
    rules = []
    
    # Find FIRST SCHEDULE marker and stop there
    # Make it more specific: look for "FIRST SCHEDULE" as a heading (usually on its own line or after newline)
    # This avoids matching "First Schedule" mentioned in rule content
    first_schedule_match = re.search(r'\n\s*FIRST SCHEDULE\s*\n|^FIRST SCHEDULE\s*\n', text, re.IGNORECASE | re.MULTILINE)
    if first_schedule_match:
        main_text = text[:first_schedule_match.start()]
    else:
        main_text = text
    
    # Find all rule starts: pattern "number. Title. —"
    rule_starts = []
    # Pattern: number. Title (can span lines) ending with period, then dash
    # Simpler approach: match "number. Title" where Title ends with ". " or "." followed by dash
    # Use lookahead to ensure we match the period-dash pattern
    # Match any characters (including newlines with DOTALL) until we find ". " + dash or "." + dash
    rule_pattern = r'(\d{1,2})\.\s+([A-Z].*?)\s*\.(?:\s+|)[—–-\u2014\u2013]'
    
    all_matches = list(re.finditer(rule_pattern, main_text, re.MULTILINE | re.DOTALL))
    
    for match in all_matches:
        rule_num = match.group(1).strip()
        title = match.group(2).strip()
        # Clean title - remove newlines, normalize spaces
        title = re.sub(r'\s+', ' ', title).strip()
        start_pos = match.end()  # Start of content after em dash
        rule_starts.append((int(rule_num), title, start_pos, match.start()))
    
    # Extract content for each rule
    for i, (rule_num, title, content_start, rule_start) in enumerate(rule_starts):
        # Only include Rules 1-16
        if rule_num > 16:
            continue
        
        # Find end of this rule's content (start of next rule or end of text)
        if i + 1 < len(rule_starts):
            content_end = rule_starts[i + 1][3]  # Start position of next rule
        else:
            content_end = len(main_text)
        
        # Extract content
        content = main_text[content_start:content_end].strip()
        
        # Clean up content - normalize whitespace but preserve structure
        content = re.sub(r'[ \t]+', ' ', content)  # Multiple spaces/tabs to single space
        content = re.sub(r'\n+', ' ', content)  # Newlines to space
        content = re.sub(r'\s+', ' ', content)  # Multiple spaces to single
        content = content.strip()
        
        if content:  # Only add if content exists
            rules.append((str(rule_num), title, content))
    
    return rules

def extract_subrules(content: str) -> list:
    """
    Extract sub-rules from rule content.
    Handles both lettered sub-rules: (a), (b), (c) and numbered: (1), (2), (3)
    Includes all nested content within each sub-rule
    
    Returns: List of (identifier, text) tuples where identifier is like 'a', 'b', '1', '2'
    """
    subrules = []
    
    # Find all potential sub-rule markers at the start
    # Look for patterns like "(a)", "(b)" or "(1)", "(2)" at word boundaries
    
    # First, try to find lettered sub-rules (a-z) - these are top-level
    lettered_pattern = r'\(([a-z])\)\s+'
    lettered_positions = [(m.start(), m.end(), m.group(1)) for m in re.finditer(lettered_pattern, content)]
    
    # Also find numbered sub-rules (1-9) - these might be top-level
    numbered_pattern = r'\((\d+)\)\s+'
    numbered_positions = [(m.start(), m.end(), m.group(1)) for m in re.finditer(numbered_pattern, content)]
    
    # Determine which type is top-level by checking which appears first and more frequently
    if lettered_positions and (not numbered_positions or lettered_positions[0][0] < numbered_positions[0][0]):
        # Lettered sub-rules are top-level
        positions = lettered_positions
        is_lettered = True
    elif numbered_positions:
        # Numbered sub-rules are top-level
        positions = numbered_positions
        is_lettered = False
    else:
        # No sub-rules found
        return subrules
    
    # Extract each sub-rule with its content
    for i, (start, end, identifier) in enumerate(positions):
        # Find the end of this sub-rule (start of next sub-rule at same level, or end of content)
        if i + 1 < len(positions):
            # Content until next sub-rule
            next_start = positions[i + 1][0]
            text = content[end:next_start].strip()
        else:
            # Last sub-rule - content until end
            text = content[end:].strip()
        
        # Clean up text
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = text.strip()
        
        # Skip if too short or empty
        if len(text) > 30:
            subrules.append((identifier, text))
    
    # If we found numbered top-level sub-rules, check if they contain lettered nested sub-rules
    # and extract those separately for better granularity
    if not is_lettered and subrules:
        # Re-examine: if numbered sub-rules contain lettered sub-rules, extract nested ones
        enhanced_subrules = []
        for identifier, text in subrules:
            # Check if this numbered sub-rule contains lettered sub-rules
            nested_lettered = list(re.finditer(r'\(([a-z]+)\)\s+([^()]+?)(?=\s*\([a-z]+\)|$)', text, re.DOTALL))
            
            if nested_lettered and len(nested_lettered) > 1:
                # Extract nested lettered sub-rules separately
                for nested in nested_lettered:
                    nested_id = nested.group(1)
                    nested_text = nested.group(2).strip()
                    nested_text = re.sub(r'\s+', ' ', nested_text)
                    if len(nested_text) > 30:
                        # Format: "1(a)" for nested sub-rules
                        enhanced_subrules.append((f"{identifier}({nested_id})", nested_text))
            else:
                # Keep the numbered sub-rule as-is
                enhanced_subrules.append((identifier, text))
        
        return enhanced_subrules
    
    return subrules

def is_mandatory(text: str) -> bool:
    """Check if requirement contains 'shall' (mandatory)"""
    return bool(re.search(r'\bshall\b', text, re.IGNORECASE))

def get_penalty_category(rule_num: str) -> str:
    """Map rule number to penalty category"""
    return PENALTY_MAP.get(rule_num, 'general_violations')

def extract_third_schedule(text: str) -> list:
    """
    Extract Third Schedule retention requirements
    
    Returns: List of (entity_class, threshold, retention_days) tuples
    """
    schedule_data = []
    
    # Find Third Schedule section
    schedule_match = re.search(
        r'THIRD SCHEDULE.*?(?=FOURTH SCHEDULE|$)',
        text,
        re.DOTALL | re.IGNORECASE
    )
    
    if not schedule_match:
        return schedule_data
    
    schedule_text = schedule_match.group(0)
    
    # Extract e-commerce entities
    if 'e-commerce entity' in schedule_text and 'two crore' in schedule_text:
        schedule_data.append(('ecommerce', 20000000, 1095))
    
    # Extract online gaming entities
    if 'online gaming' in schedule_text and 'fifty lakh' in schedule_text:
        schedule_data.append(('gaming', 5000000, 1095))
    
    # Extract social media entities
    if 'social media' in schedule_text and 'two crore' in schedule_text:
        schedule_data.append(('social_media', 20000000, 1095))
    
    return schedule_data

def insert_requirement(cursor, rule_number, text, obligation_type, is_sdf=False):
    """Insert requirement into database (skip if duplicate)"""
    
    # Check if this requirement already exists
    cursor.execute('''
        SELECT id FROM requirements 
        WHERE rule_number = ? AND requirement_text = ?
    ''', (rule_number, text))
    if cursor.fetchone():
        return  # Skip duplicate
    
    # Get penalty category for the main rule
    main_rule = rule_number.split('(')[0].replace('Rule ', '').strip()
    penalty_category = get_penalty_category(main_rule)
    
    # Get penalty_category_id for the penalty category
    cursor.execute(
        'SELECT id FROM penalties WHERE category_name = ?',
        (penalty_category,)
    )
    result = cursor.fetchone()
    penalty_category_id = result[0] if result else None
    
    # Insert requirement into the database [SQLite database]
    cursor.execute('''
        INSERT INTO requirements (
            rule_number,
            requirement_text,
            obligation_type,
            penalty_category_id,
            deadline,
            is_sdf_specific
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        rule_number,
        text,
        obligation_type,
        penalty_category_id,
        FULL_COMPLIANCE_DEADLINE.isoformat(),
        is_sdf
    ))

def insert_third_schedule_entry(cursor, entity_class, threshold, retention_days):
    """Insert Third Schedule entry (skip if duplicate)"""
    # Check if this entry already exists
    cursor.execute('''
        SELECT id FROM schedule_references 
        WHERE schedule_name = ? AND entity_class = ?
    ''', ('Third Schedule', entity_class))
    if cursor.fetchone():
        return  # Skip duplicate
    
    cursor.execute('''
        INSERT INTO schedule_references (
            schedule_name,
            entity_class,
            threshold_users,
            retention_period_days
        ) VALUES (?, ?, ?, ?)
    ''', ('Third Schedule', entity_class, threshold, retention_days))

def main():
    """Main extraction process"""
    print("=" * 70)
    print("DPDPA Requirements Extraction")
    print("=" * 70)
    print()
    
    # Load extracted text
    print("Loading extracted text files...")
    rules_text = load_text_file('rules_2025_extracted.txt')
    print(f"✓ Loaded Rules 2025 ({len(rules_text):,} characters)")
    
    # Clean text
    print("Cleaning text...")
    rules_text = clean_text(rules_text)
    print("✓ Text cleaned")
    print()
    
    # Connect to database
    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print(f"✓ Connected to {DB_PATH}")
    
    # Clean up duplicates before inserting
    print("Cleaning up duplicates...")
    cursor.execute('''
        DELETE FROM requirements 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM requirements 
            GROUP BY rule_number, requirement_text
        )
    ''')
    req_duplicates = cursor.rowcount
    
    cursor.execute('''
        DELETE FROM schedule_references 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM schedule_references 
            WHERE schedule_name = 'Third Schedule'
            GROUP BY entity_class
        ) AND schedule_name = 'Third Schedule'
    ''')
    schedule_duplicates = cursor.rowcount
    
    if req_duplicates > 0 or schedule_duplicates > 0:
        print(f"  Removed {req_duplicates} duplicate requirements")
        print(f"  Removed {schedule_duplicates} duplicate Third Schedule entries")
        conn.commit()
    else:
        print("  No duplicates found")
    print()
    
    # Extract rules
    print("Extracting rules...")
    rules = extract_rules(rules_text)
    print(f"✓ Found {len(rules)} rules")
    if rules:
        print("  Extracted rules:", [f"Rule {r[0]}: {r[1][:40]}..." for r in rules])
    print()
    
    # Process key rules (3, 6, 7, 8, 9, 10, 13, 14)
    target_rules = ['3', '6', '7', '8', '9', '10', '13', '14']
    requirements_count = 0
    
    print("Processing requirements...")
    
    for rule_num, title, content in rules:
        if rule_num not in target_rules:
            continue
        
        print(f"  Processing Rule {rule_num}: {title[:50]}...")
        print(f"    Content length: {len(content)} chars")
        
        # Determine obligation type
        if rule_num == '3':
            obligation_type = 'notice'
        elif rule_num == '6':
            obligation_type = 'security'
        elif rule_num == '7':
            obligation_type = 'breach'
        elif rule_num == '8':
            obligation_type = 'retention'
        elif rule_num == '9':
            obligation_type = 'notice'
        elif rule_num == '10':
            obligation_type = 'children'
        elif rule_num == '13':
            obligation_type = 'sdf'
        elif rule_num == '14':
            obligation_type = 'rights'
        else:
            obligation_type = 'general'
        
        # Check if SDF-specific
        is_sdf = (rule_num == '13')
        
        # Remove illustrations/examples that might interfere
        # Look for "Illustration." or "Case" patterns and remove them
        content_clean = re.sub(r'\bIllustration\.?\s+.*?(?=\s*\([a-z]\)|\s*\(\d+\)|$)', '', content, flags=re.DOTALL | re.IGNORECASE)
        content_clean = re.sub(r'\bCase \d+:.*?(?=\s*Case \d+:|$)', '', content_clean, flags=re.DOTALL | re.IGNORECASE)
        
        # Extract sub-rules
        subrules = extract_subrules(content_clean)
        print(f"    Found {len(subrules)} sub-rules")
        if subrules:
            print(f"    Sub-rule identifiers: {[s[0] for s in subrules]}")
        
        if subrules:
            # Insert each sub-rule separately
            for identifier, text in subrules:
                # Filter out very short or meaningless text
                if len(text) > 50 and not text.strip().lower() in ['illustration', 'case', 'note:']:
                    # Handle nested format like "2(a)" or simple "a" or "1"
                    if '(' in identifier:
                        # Already in nested format like "2(a)"
                        rule_ref = f"Rule {rule_num}({identifier})"
                    else:
                        # Simple identifier
                        rule_ref = f"Rule {rule_num}({identifier})"
                    
                    insert_requirement(
                        cursor, rule_ref, text, obligation_type, is_sdf
                    )
                    requirements_count += 1
        else:
            # Insert whole rule if no sub-rules found
            if len(content_clean) > 50:
                rule_ref = f"Rule {rule_num}"
                # Truncate very long content but preserve structure
                rule_content = content_clean
                if len(rule_content) > 2000:
                    rule_content = rule_content[:2000] + "..."
                insert_requirement(
                    cursor, rule_ref, rule_content, obligation_type, is_sdf
                )
                requirements_count += 1
    
    print(f"✓ Inserted {requirements_count} requirements")
    print()
    
    # Extract Third Schedule
    print("Extracting Third Schedule...")
    schedule_entries = extract_third_schedule(rules_text)
    
    for entity_class, threshold, retention_days in schedule_entries:
        insert_third_schedule_entry(cursor, entity_class, threshold, retention_days)
        print(f"  ✓ {entity_class}: {threshold:,} users, {retention_days} days retention")
    
    print(f"✓ Inserted {len(schedule_entries)} Third Schedule entries")
    print()
    
    # Commit changes
    conn.commit()
    
    # Verify insertion
    cursor.execute('SELECT COUNT(*) FROM requirements')
    total_requirements = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM schedule_references WHERE schedule_name = "Third Schedule"')
    total_schedule = cursor.fetchone()[0]
    
    conn.close()
    
    # Summary
    print("=" * 70)
    print("EXTRACTION COMPLETE")
    print("=" * 70)
    print()
    print(f"Total requirements in database: {total_requirements}")
    print(f"Total Third Schedule entries: {total_schedule}")
    print()
    print("Next step: Verify data with query:")
    print("  SELECT rule_number, obligation_type FROM requirements LIMIT 10;")

if __name__ == "__main__":
    main()