"""
Collects business profile data through 15 questions

Usage:
    from src.assessment.questionnaire import run_questionnaire
    answers = run_questionnaire()
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Question definitions
QUESTIONS = [
    {
        "id": "Q1",
        "text": "What is your business name?",
        "type": "text",
        "maps_to": "business_name",
        "required": True,
        "help": None
    },
    {
        "id": "Q2",
        "text": "Select your entity type:",
        "type": "select",
        "options": [
            "startup",
            "smb", 
            "ecommerce",
            "social_media",
            "fintech",
            "healthcare",
            "edtech",
            "gaming",
            "other"
        ],
        "maps_to": "entity_type",
        "required": True,
        "help": "This determines which specific requirements apply to your business"
    },
    {
        "id": "Q3",
        "text": "How many registered users do you have in India?",
        "type": "number",
        "maps_to": "user_count",
        "required": True,
        "help": "Third Schedule applies if: E-commerce/Social Media ≥20M, Gaming ≥5M"
    },
    {
        "id": "Q4",
        "text": "Do you process personal data of children (under 18)?",
        "type": "yes_no",
        "maps_to": "processes_children_data",
        "required": True,
        "help": "Children's data requires verifiable parent consent (Rule 10) - ₹200cr penalty"
    },
    {
        "id": "Q5",
        "text": "Do you transfer personal data outside India?",
        "type": "yes_no",
        "maps_to": "cross_border_transfers",
        "required": True,
        "help": "Cross-border transfers may face restrictions (Rule 15)"
    },
    {
        "id": "Q6",
        "text": "What types of personal data do you process? (comma-separated)",
        "type": "multiselect",
        "options": [
            "name",
            "email",
            "phone",
            "address",
            "payment_info",
            "health_data",
            "biometric",
            "location",
            "behavioral"
        ],
        "maps_to": "data_types",
        "required": True,
        "help": "Select all that apply. Health/biometric data = higher risk"
    },
    {
        "id": "Q7",
        "text": "Do you use AI or automated decision-making?",
        "type": "yes_no",
        "maps_to": "uses_ai",
        "required": False,
        "help": "May trigger algorithmic due diligence for Significant Data Fiduciaries"
    },
    {
        "id": "Q8",
        "text": "What is your approximate annual revenue (INR)?",
        "type": "select",
        "options": [
            "< 1 crore",
            "1-10 crore",
            "10-50 crore",
            "50-100 crore",
            "> 100 crore"
        ],
        "maps_to": "annual_revenue",
        "required": False,
        "help": "Optional - helps understand business scale"
    },
    {
        "id": "Q9",
        "text": "Do you have contracts with Data Processors (vendors processing data on your behalf)?",
        "type": "yes_no",
        "maps_to": "has_processors",
        "required": True,
        "help": "Rule 6(1)(f) requires security safeguards in Data Processor contracts"
    },
    {
        "id": "Q10",
        "text": "What security measures do you currently have? (comma-separated)",
        "type": "multiselect",
        "options": [
            "encryption",
            "access_control",
            "logging",
            "backups",
            "none"
        ],
        "maps_to": "current_security",
        "required": True,
        "help": "Rule 6 requires minimum: encryption, access control, logging, backups"
    },
    {
        "id": "Q11",
        "text": "Do you have a documented breach response plan?",
        "type": "yes_no",
        "maps_to": "has_breach_plan",
        "required": True,
        "help": "Rule 7 requires 72-hour notification to Board - ₹200cr penalty"
    },
    {
        "id": "Q12",
        "text": "Do you track user behavior or use analytics?",
        "type": "yes_no",
        "maps_to": "tracks_behavior",
        "required": True,
        "help": "PROHIBITED for children under Rule 10"
    },
    {
        "id": "Q13",
        "text": "Do you do targeted advertising?",
        "type": "yes_no",
        "maps_to": "targeted_advertising",
        "required": True,
        "help": "PROHIBITED for children under Rule 10"
    },
    {
        "id": "Q14",
        "text": "Do you have a consent mechanism for users?",
        "type": "yes_no",
        "maps_to": "has_consent_mechanism",
        "required": True,
        "help": "Rule 3 (notice) and Section 6 (consent) - Required for ALL businesses"
    },
    {
        "id": "Q15",
        "text": "Do you have a grievance redressal system?",
        "type": "yes_no",
        "maps_to": "has_grievance_system",
        "required": True,
        "help": "Rule 14 requires 90-day response time - ₹50cr penalty"
    }
]


def display_question(question: Dict[str, Any], question_num: int, total: int) -> None:
    """Display a single question with formatting"""
    print(f"\n{'='*70}")
    print(f"Question {question_num}/{total}: {question['id']}")
    print(f"{'='*70}")
    print(f"\n{question['text']}")
    
    # Show options for select/multiselect
    if question['type'] in ['select', 'multiselect']:
        print("\nOptions:")
        for i, option in enumerate(question['options'], 1):
            print(f"  {i}. {option}")
    
    # Show help text
    if question.get('help'):
        print(f"\nℹ️  {question['help']}")
    
    # Show if required
    if question['required']:
        print("\n[Required]")
    else:
        print("\n[Optional - press Enter to skip]")


def validate_answer(question: Dict[str, Any], answer: str) -> tuple[bool, Any]:
    """
    Validate user answer based on question type
    
    Returns:
        (is_valid, processed_answer)
    """
    answer = answer.strip()
    
    # Handle optional questions
    if not question['required'] and answer == "":
        return True, None
    
    # Required questions cannot be empty
    if question['required'] and answer == "":
        return False, None
    
    # Type-specific validation
    if question['type'] == 'text':
        if len(answer) < 2:
            return False, None
        return True, answer
    
    elif question['type'] == 'number':
        try:
            num = int(answer.replace(',', '').replace('_', ''))
            if num < 0:
                return False, None
            return True, num
        except ValueError:
            return False, None
    
    elif question['type'] == 'yes_no':
        answer_lower = answer.lower()
        if answer_lower in ['y', 'yes', '1', 'true']:
            return True, True
        elif answer_lower in ['n', 'no', '0', 'false']:
            return True, False
        else:
            return False, None
    
    elif question['type'] == 'select':
        # Try by number
        try:
            idx = int(answer) - 1
            if 0 <= idx < len(question['options']):
                return True, question['options'][idx]
        except ValueError:
            pass
        
        # Try by text match
        answer_lower = answer.lower()
        for option in question['options']:
            if option.lower() == answer_lower:
                return True, option
        
        return False, None
    
    elif question['type'] == 'multiselect':
        # Parse comma-separated values
        selections = [s.strip() for s in answer.split(',')]
        validated = []
        
        for selection in selections:
            # Try by number
            try:
                idx = int(selection) - 1
                if 0 <= idx < len(question['options']):
                    validated.append(question['options'][idx])
                    continue
            except ValueError:
                pass
            
            # Try by text match
            selection_lower = selection.lower()
            for option in question['options']:
                if option.lower() == selection_lower:
                    validated.append(option)
                    break
        
        if validated:
            return True, validated
        else:
            return False, None
    
    return False, None


def ask_question(question: Dict[str, Any], question_num: int, total: int) -> Any:
    """
    Ask a question and get validated answer
    
    Returns:
        Validated answer
    """
    while True:
        display_question(question, question_num, total)
        
        # Get input based on type
        if question['type'] == 'yes_no':
            prompt = "\nYour answer (y/n): "
        elif question['type'] == 'multiselect':
            prompt = "\nYour answer (enter numbers or names, comma-separated): "
        elif question['type'] == 'select':
            prompt = "\nYour answer (enter number or name): "
        elif question['type'] == 'number':
            prompt = "\nYour answer (number): "
        else:
            prompt = "\nYour answer: "
        
        answer = input(prompt)
        
        # Validate
        is_valid, processed = validate_answer(question, answer)
        
        if is_valid:
            return processed
        else:
            print("\n❌ Invalid answer. Please try again.")
            if question['type'] == 'select':
                print("   Enter the number (1-{}) or exact option name".format(len(question['options'])))
            elif question['type'] == 'multiselect':
                print("   Enter numbers or names separated by commas (e.g., '1,3,5' or 'email,phone')")
            elif question['type'] == 'yes_no':
                print("   Enter 'y' or 'n'")
            elif question['type'] == 'number':
                print("   Enter a valid number (e.g., 1000000 or 1,000,000)")


def run_questionnaire() -> Dict[str, Any]:
    """
    Run complete questionnaire
    
    Returns:
        Dictionary of answers mapped to field names
    """
    print("\n" + "="*70)
    print("DPDPA COMPLIANCE ASSESSMENT - QUESTIONNAIRE")
    print("="*70)
    print("\nThis assessment has 15 questions about your business.")
    print("It will take approximately 5-10 minutes to complete.")
    print("\nYour answers will determine:")
    print("  • Which DPDP requirements apply to you")
    print("  • Your compliance gaps")
    print("  • Priority requirements")
    print("  • Maximum penalty exposure")
    print("\nPress Ctrl+C at any time to exit.")
    
    input("\nPress Enter to begin...")
    
    answers = {}
    total_questions = len(QUESTIONS)
    
    for i, question in enumerate(QUESTIONS, 1):
        try:
            answer = ask_question(question, i, total_questions)
            answers[question['maps_to']] = answer
        except KeyboardInterrupt:
            print("\n\n❌ Assessment cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    
    # Summary
    print("\n" + "="*70)
    print("QUESTIONNAIRE COMPLETE")
    print("="*70)
    print(f"\n✓ Collected {len(answers)} answers")
    
    # Show key profile info
    print("\nYour Profile Summary:")
    print(f"  Business: {answers.get('business_name', 'N/A')}")
    print(f"  Type: {answers.get('entity_type', 'N/A')}")
    print(f"  Users: {answers.get('user_count', 0):,}")
    print(f"  Children's Data: {'Yes' if answers.get('processes_children_data') else 'No'}")
    print(f"  Cross-Border: {'Yes' if answers.get('cross_border_transfers') else 'No'}")
    
    return answers


def save_questions_to_db():
    """
    Pre-populate assessment_questions table in database
    For use in Streamlit dashboard (Phase 4)
    """
    import sqlite3
    from config.config import DB_PATH
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clear existing questions
    cursor.execute("DELETE FROM assessment_questions")
    
    # Insert questions
    for i, q in enumerate(QUESTIONS, 1):
        cursor.execute("""
            INSERT INTO assessment_questions (
                question_text,
                question_type,
                options,
                maps_to_field,
                display_order
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            q['text'],
            q['type'],
            ','.join(q.get('options', [])),
            q['maps_to'],
            i
        ))
    
    conn.commit()
    conn.close()
    
    print(f"✓ Saved {len(QUESTIONS)} questions to database")


# For testing
if __name__ == "__main__":
    # Run questionnaire
    answers = run_questionnaire()
    
    print("\n" + "="*70)
    print("COLLECTED ANSWERS (for debugging)")
    print("="*70)
    for key, value in answers.items():
        print(f"{key:30s} = {value}")
    
    # Optionally save to database
    save_choice = input("\nSave questions to database? (y/n): ")
    if save_choice.lower() in ['y', 'yes']:
        save_questions_to_db()