
# DPDPA Compliance Dashboard

**Automated compliance assessment tool for India's Digital Personal Data Protection Act, 2023**

![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.40.2-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

---

## Overview

India's Digital Personal Data Protection Act, 2023 mandates full compliance by  **May 13, 2027** . Non-compliance carries penalties up to **Rs. 250 crore** per violation. Most Indian startups and SMBs lack the resources to hire expensive law firms (Rs. 5-10 lakhs typical consulting fees) for compliance assessment.

The **DPDPA Compliance Dashboard** democratizes access to compliance assessment by:

* Extracting 47+ requirements directly from official DPDP Rules 2025 and Act 2023
* Providing instant gap analysis based on your specific business profile
* Generating prioritized action plans with penalty exposure calculations
* Operating entirely offline on your local machine - **zero data leaves your system**

### What This Dashboard Does

**Immediate Value:**

* 5-minute assessment replacing weeks of legal research
* Identifies exactly which of 47 requirements apply to YOUR business type
* Calculates total penalty exposure (often Rs. 450-5,200 crore for non-compliant businesses)
* Generates downloadable Excel reports with implementation roadmaps

**What This Dashboard Does NOT Do:**

* Provide legal advice or guarantee compliance
* Replace consultation with qualified data protection lawyers
* Monitor ongoing compliance or provide automated updates
* Submit any data to external servers or third parties

### Privacy-First Architecture

**Your data never leaves your computer:**

* 100% local SQLite database (no cloud, no external APIs)
* No telemetry, analytics, or tracking
* No user accounts or authentication required
* All assessments stored only on your local machine
* Can run completely offline after initial setup

This privacy-first design reflects the core principle of the DPDP Act itself:  **data minimization and purpose limitation** .

---

## Quick Start - Local Installation

### System Requirements

* **Operating System:** Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
* **Python:** 3.13 or higher ([Download here](https://www.python.org/downloads/))
* **Disk Space:** 150 MB minimum
* **RAM:** 2 GB minimum
* **Internet:** Required only for initial package installation

### Step-by-Step Installation

#### 1. Install Python 3.13

**Windows:**

```powershell
# Download from https://www.python.org/downloads/
# During installation, CHECK "Add Python to PATH"
# Verify installation:
python --version
```

**macOS:**

```bash
# Using Homebrew
brew install python@3.13

# Verify installation
python3.13 --version
```

**Linux (Ubuntu/Debian):**

```bash
# Add deadsnakes PPA for Python 3.13
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv

# Verify installation
python3.13 --version
```

#### 2. Download the Project

**Option A: Using Git (Recommended)**

```bash
git clone https://github.com/Tushar-9802/DPDPA.git
cd DPDPA
```

**Option B: Manual Download**

1. Go to https://github.com/Tushar-9802/DPDPA
2. Click "Code" → "Download ZIP"
3. Extract to your desired location
4. Open terminal/command prompt in extracted folder

#### 3. Create Virtual Environment

**Windows (PowerShell):**

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verify activation (you should see (venv) in prompt)
```

**macOS/Linux:**

```bash
# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (you should see (venv) in prompt)
```

#### 4. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected packages:**

* streamlit==1.40.2
* pandas==2.2.3
* plotly==5.24.1
* openpyxl==3.1.5
* PyMuPDF==1.24.13

#### 5. Initialize Database

```bash
# Create database with all 47 requirements
python src/extraction/init_db.py
python src/extraction/extract_requirements.py

# Verify database creation
python -c "import sqlite3; c=sqlite3.connect('data/processed/dpdpa_compliance.db'); print('Requirements:', c.execute('SELECT COUNT(*) FROM requirements').fetchone()[0])"

# Expected output: Requirements: 47
```

#### 6. Launch Dashboard

```bash
streamlit run app.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

**Troubleshooting:**

* If port 8501 is busy: `streamlit run app.py --server.port 8502`
* If browser doesn't open: Manually navigate to `http://localhost:8501`
* If you see database errors: Re-run steps in section 5

---

## How This Dashboard Uses the DPDP Act

### Legal Framework Integration

This dashboard is built on a foundation of official Indian government regulations:

**Primary Sources:**

1. **Digital Personal Data Protection Act, 2023** (Enacted August 11, 2023)
   * Section 6: Obligations of Data Fiduciaries
   * Section 9: Additional obligations for children's data
   * Section 33: Penalty schedule (Rs. 10,000 to Rs. 250 crore)
2. **DPDP Rules, 2025** (Notified November 13, 2025)
   * Rule 3: Notice and Consent requirements
   * Rule 6: Reasonable Security Safeguards (encryption, access control, logging, backups)
   * Rule 7: Breach Notification (72-hour timeline to Data Protection Board)
   * Rule 8: Data Retention and Erasure
   * Rule 9: Contact Information Publication
   * Rule 10: Children's Data Protection (verifiable parental consent, no tracking/advertising)
   * Rule 13: Significant Data Fiduciary (SDF) obligations
   * Rule 14: Data Principal Rights (grievance redressal within 90 days)
   * Rule 15: Cross-border Data Transfers
   * Third Schedule: Data retention requirements (varies by business type)

### Requirement Extraction Process

**Phase 1: PDF Text Extraction**

* Used PyMuPDF to extract text from 200+ page official government PDFs
* Implemented regex patterns to identify rule structures: "Rule X(Y)(Z)"
* Filtered substantive requirements (>50 characters, meaningful content)
* Avoided contamination from schedules and annexures

**Phase 2: Categorization**
Each requirement tagged with:

* `obligation_type`: notice, security, breach, retention, children, rights, sdf, general
* `penalty_category`: Mapped to Section 33 penalty schedule
* `is_sdf_specific`: Boolean flag for Significant Data Fiduciary requirements
* `implementation_complexity`: Low/Medium/High based on technical requirements

**Phase 3: Business Applicability Logic**
Requirements matched based on:

* **Entity Type:** E-commerce, social media, gaming, fintech, healthcare, edtech
* **User Count:** Third Schedule thresholds (20M for e-commerce/social media, 5M for gaming)
* **Data Processing:** Children's data, cross-border transfers, use of processors
* **Current Status:** Inferred from 15-question assessment

### Penalty Mapping (Section 33)

| Violation                               | Penalty (Rs. Crore) | Mapped Rules                 |
| --------------------------------------- | ------------------- | ---------------------------- |
| Security breach (Section 8)             | 250                 | Rule 6 (all 8 requirements)  |
| Breach notification failure (Section 8) | 200                 | Rule 7 (all 13 requirements) |
| Children's data violations (Section 9)  | 200                 | Rule 10 (all 7 requirements) |
| Notice/Consent failures (Section 6)     | 50                  | Rule 3 (all 5 requirements)  |
| Rights violations (Section 11)          | 50                  | Rule 14 (all 6 requirements) |
| General violations                      | 10                  | Other rules                  |

### Compliance Scoring Algorithm

**Gap Analysis Logic:**

```python
# Universal requirements (applies to ALL businesses)
- Rule 3 (Notice): 5 requirements
- Rule 6 (Security): 8 requirements
- Rule 7 (Breach): 13 requirements
- Rule 9 (Contact): 1 requirement
- Rule 14 (Rights): 6 requirements
Total Universal: 33 requirements

# Conditional requirements
- Third Schedule (large platforms): 3 requirements
- Rule 10 (Children): 7 requirements
- Rule 15 (Cross-border): ~3 requirements
- Rule 13 (SDF): 5 requirements
Total Possible: 47 requirements

# Completion inference from questionnaire
IF has_consent_mechanism = True → Rule 3 complete (5/5)
IF all 4 security measures present → Rule 6 complete (8/8)
IF has_breach_plan = True → Rule 7 complete (13/13)
IF has_grievance_system = True → Rule 14 complete (6/6)

# Score = (Completed / Total Applicable) × 100
```

**Priority Scoring (0-100):**

```python
priority_score = (
    0.40 × (penalty_amount / max_penalty) +      # 40% weight on financial risk
    0.30 × (days_remaining / total_days) +        # 30% weight on urgency
    0.30 × (implementation_complexity / 10)       # 30% weight on effort
)
```

---

## Dashboard Features

### 1. Home Page

**Past Assessments View:**

* Lists all previous assessments stored locally
* Quick comparison of compliance scores over time
* Click to view full historical reports
* Delete functionality for outdated assessments

**FAQ Section:**

* Common questions about DPDP Act
* Clarification on penalties and timelines
* Links to official government resources

**Privacy Notice:**

* Explains local-only data storage
* No external data transmission
* User control over all stored data

### 2. Assessment Page

**15-Question Interactive Form:**

**Section 1: Business Information**

1. Business name (legal entity name)
2. Entity type (startup/SMB/e-commerce/social media/fintech/healthcare/edtech/gaming)
3. Registered user count in India (triggers Third Schedule thresholds)

**Section 2: Data Processing Activities**
4. Processing children's data (under 18 years)
5. Cross-border data transfers
6. Types of personal data processed (name, email, phone, payment, health, biometric, etc.)
7. Use of AI or automated decision-making
8. Annual revenue (optional, for context)

**Section 3: Current Compliance Status**
9. Contracts with Data Processors (vendors)
10. Security measures in place (encryption, access control, logging, backups)
11. Documented breach response plan
12. User behavior tracking or analytics
13. Targeted advertising
14. Consent mechanism for users
15. Grievance redressal system

**Demo Mode:**

* "Try Demo" button pre-fills form with sample data
* Instant experience without manual data entry
* Sample: TechStartup Pvt Ltd (15k users, full compliance)

**Validation:**

* Real-time field validation
* Mandatory field checks (marked with *)
* Illegal activity detection (children + tracking/ads)
* Error messages with specific guidance

**Loading States:**

* Progress bar during analysis (25% → 50% → 75% → 100%)
* Status updates: "Creating profile..." → "Matching requirements..." → "Analyzing gaps..."
* Smooth user experience (no frozen screens)

### 3. Results Page

**Key Metrics Dashboard:**

* Compliance Score (0-100%)
* Max Single Penalty (Rs. X crore)
* Total Penalty Exposure (Rs. X crore)
* Days to Deadline (countdown to May 13, 2027)

**Requirements Breakdown:**

* Pie chart: Requirements by type (notice, security, breach, children, rights, etc.)
* Gauge chart: Compliance progress visualization
* Statistics: Total/Completed/Pending requirements

**Penalty Exposure Analysis:**

* Bar chart: Penalty exposure by requirement type
* Color-coded by risk level
* Hover for detailed breakdowns

**Top 10 Priority Requirements:**

* Sortable table with priority scores (0-100)
* Rule numbers and penalty amounts
* Days remaining until deadline
* Brief descriptions

**Dynamic Personalized Action Plan:**

* Generated based on YOUR actual gaps (not generic)
* Conditional steps (only shows what YOU need to fix)
* Specific action items with checkboxes
* Timeline estimates (immediate/2-4 weeks/1-2 months)
* Effort estimates (1-2 weeks/3-4 weeks/ongoing)
* Penalty exposure per category

**Example Action Plans:**

*For Healthcare (97% compliant, 1 security gap):*

```
1. CRITICAL: Implement Security Safeguards (Rule 6)
   Penalty Exposure: Rs. 250 crore
   Missing: 1 security requirement
   
   Required Actions:
   - Implement data encryption
   - Setup access control
   - Enable logging
   - Implement backups
   
   Timeline: Start immediately
   Estimated Effort: 4-8 weeks
```

*For Gaming with children (22% compliant, multiple gaps):*

```
1. HIGH PRIORITY: Children's Data Protection (Rule 10)
   Penalty Exposure: Rs. 400 crore
   Missing: 2 children data requirements
   
   Required Actions:
   - IMMEDIATELY disable behavioral tracking
   - IMMEDIATELY disable targeted advertising
   - Implement parental consent
   - Add age verification
   
   Timeline: Immediate action required
   Estimated Effort: 1-2 weeks (urgent)

2. CRITICAL: Implement Security Safeguards (Rule 6)
   Penalty Exposure: Rs. 1,750 crore
   Missing: 7 security requirements
   ...
```

**Deadline Urgency Warnings:**

* Red alert if <180 days remaining (final 6 months)
* Orange warning if <365 days remaining (final 12 months)
* Blue info if >365 days (good timing)

**Download Options:**

* Excel report with full analysis
* Tabs: Executive Summary, Requirements, Gaps, Priorities, Implementation Roadmap
* Formatted for printing and sharing with stakeholders

### 4. DPDPA Reference Page

**Comprehensive Act & Rules Reference:**

**Tab 1: Key Sections**

* Section 6: Data Fiduciary obligations
* Section 9: Children's data special protections
* Section 11: Data Principal rights
* Section 33: Penalty schedule

**Tab 2: Critical Rules**

* Rule 3: Notice requirements (clear, plain language)
* Rule 6: Security safeguards (encryption, access control, logging, backups)
* Rule 7: Breach notification (72-hour timeline)
* Rule 10: Children protection (no tracking, no ads)
* Rule 14: Grievance redressal (90-day response)

**Tab 3: Third Schedule**

* E-commerce/Social Media: 20M users threshold
* Gaming: 5M users threshold
* Data retention requirements by business type

**Tab 4: Penalties**

* Visual penalty matrix
* Examples of violations and corresponding fines
* Cumulative penalty calculations

**Tab 5: Resources**

* Links to MEITY website
* Data Protection Board portal
* Official government notifications
* Industry guidance documents

### 5. About Page

**Project Information:**

* Methodology explanation
* Data sources and extraction process
* Technical architecture overview
* Development timeline

**Contact & Support:**

* GitHub repository link
* Issue reporting
* Feature requests
* Community discussions

---

## Use Cases

### For Startups (Pre-Seed to Series A)

**Problem:** Limited budget (Rs. 5-10 lakhs for consultants), tight deadlines, technical team but no legal expertise.

**Solution:**

1. Run initial assessment (5 minutes)
2. Identify critical gaps (usually Rule 6, 7, 10)
3. Download Excel roadmap
4. Implement technical requirements in-house (encryption, logging, etc.)
5. Consult lawyer only for complex items (privacy notice, DPO appointment)
6. Re-assess every quarter until 100% compliance

**Cost Savings:** Rs. 3-7 lakhs (self-implementation of 70-80% of requirements)

### For SMBs (Established Businesses, 10-100 employees)

**Problem:** Existing systems, legacy tech debt, multiple vendors, uncertain which rules apply.

**Solution:**

1. Assessment reveals conditional requirements (Third Schedule, processors, cross-border)
2. Priority scoring focuses on high-penalty items first
3. Phased implementation over 12-18 months
4. Vendor contract reviews (Rule 6 security obligations)
5. Employee training on new processes

**Cost Savings:** Rs. 5-10 lakhs (reduced consulting hours through self-assessment)

### For Consultants & Law Firms

**Problem:** Manual compliance assessments take 40-80 hours, prone to human error, difficult to scale.

**Solution:**

1. Use dashboard for initial client screening
2. Generate baseline reports in 5 minutes vs 2 weeks
3. Focus consulting hours on complex implementation, not basic gap analysis
4. Scale to 10x more clients with same team size
5. White-label potential (customize dashboard for client-facing use)

**Value Add:** Rs. 2-5 lakhs per client saved in junior associate hours

### For In-House Compliance Teams

**Problem:** Manual spreadsheet tracking, outdated checklists, no automated updates.

**Solution:**

1. Quarterly re-assessments track progress
2. Automated priority recalculation as deadline approaches
3. Excel exports for board presentations
4. Historical comparison shows improvement trajectory
5. Internal audit preparation

**Efficiency Gain:** 20-30 hours per quarter saved on manual reporting

---

## Legal Disclaimers

### Limitation of Liability

**THIS TOOL IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.**

**The DPDPA Compliance Dashboard:**

* Is a software tool, not a law firm or legal service provider
* Does NOT provide legal advice or create attorney-client relationships
* Does NOT guarantee compliance with the DPDP Act, 2023
* Does NOT monitor ongoing compliance or provide real-time updates
* Does NOT submit filings or registrations to any government authority

**The developers, contributors, and distributors of this tool:**

* Make no representations about the accuracy, completeness, or timeliness of information
* Are not responsible for any penalties, fines, or legal consequences resulting from use of this tool
* Assume no liability for errors, omissions, or outdated information
* Do not warrant that the tool is error-free or will operate without interruption

### Professional Legal Advice Required

**You MUST consult with qualified professionals for:**

* Legal interpretation of the DPDP Act and Rules
* Compliance strategy tailored to your specific business
* Drafting of privacy notices, consent forms, and policies
* Negotiation of Data Processor agreements
* Response to Data Protection Board inquiries
* Representation in enforcement proceedings

**This tool does NOT replace:**

* Data protection lawyers admitted to practice in India
* Compliance consultants with domain expertise
* Technical security auditors
* Chartered accountants for financial assessments

### Regulatory Changes

**The DPDP Act and Rules may change:**

* The Data Protection Board may issue new guidance or notifications
* Parliament may amend the Act
* MEITY may update the Rules
* Court decisions may affect interpretation

**This tool is based on:**

* DPDP Act, 2023 (as enacted August 11, 2023)
* DPDP Rules, 2025 (as notified November 13, 2025)

**Users are responsible for:**

* Monitoring MEITY website (https://www.meity.gov.in/) for updates
* Subscribing to official government notifications
* Re-assessing compliance if laws change
* Updating processes to reflect new requirements

### Data Accuracy

**While every effort has been made to extract requirements accurately:**

* The extraction process used automated text parsing
* Some nuances may be lost in summarization
* Complex nested sub-rules may require manual interpretation
* Cross-references between rules may not be fully captured

**Users should:**

* Read the full text of the DPDP Act and Rules
* Cross-verify critical requirements with official sources
* Treat this tool as a starting point, not a definitive authority

### No Endorsement

**This tool is NOT:**

* Endorsed by the Government of India
* Affiliated with the Ministry of Electronics and Information Technology (MEITY)
* Approved by the Data Protection Board of India
* Certified by any regulatory authority

**Use of this tool does NOT constitute:**

* Official compliance certification
* Government approval of your data practices
* Immunity from penalties or enforcement actions

### Modification and Updates

**This tool may be modified at any time:**

* The developers reserve the right to update, modify, or discontinue the tool
* No guarantee of backward compatibility
* Users are responsible for maintaining their own copies and data

**Updates are provided on a best-effort basis:**

* No timeline guaranteed for incorporating legal changes
* No warranty that the tool will remain current with regulations

### Jurisdiction

**This tool is designed for Indian businesses subject to the DPDP Act, 2023:**

* If you operate in multiple jurisdictions, additional laws may apply (GDPR, CCPA, etc.)
* This tool does NOT address non-Indian privacy laws
* Cross-border compliance requires separate analysis

### User Responsibility

**By using this tool, you acknowledge that:**

* You are responsible for the accuracy of information you input
* You will verify all outputs against official sources
* You will seek professional advice before making compliance decisions
* You will not rely solely on this tool for legal compliance
* You accept all risks associated with use of this tool

### Contact for Legal Issues

**For legal inquiries, contact:**

* Your organization's legal counsel
* A qualified data protection lawyer in India
* The Data Protection Board of India (https://www.dpb.gov.in/)
* MEITY (https://www.meity.gov.in/)

**Do NOT contact the tool developers for legal advice.**

---

## Privacy & Data Handling

### What Data This Dashboard Collects

**During Assessment:**

* Business name (text string)
* Entity type (categorical selection)
* User count (integer)
* Data processing activities (boolean flags)
* Current compliance status (multiple choice answers)

**Stored Locally:**

* Assessment results (compliance scores, gap analysis)
* Historical assessments (for progress tracking)
* Generated Excel reports (if downloaded)

### What Data This Dashboard Does NOT Collect

* No personal identifying information about YOU (the user)
* No actual customer data from your business
* No payment information
* No authentication credentials
* No telemetry or usage analytics
* No IP addresses or device fingerprints

### Where Your Data Is Stored

**Local SQLite Database:**

* File location: `data/processed/dpdpa_compliance.db`
* Stored on YOUR computer only
* Not synchronized to any cloud service
* Not accessible to anyone but you

**No External Transmission:**

* Zero network calls during assessment (except initial package installation)
* No data sent to external APIs
* No tracking pixels or analytics
* Can run completely offline after setup

### Your Data Rights (DPDP Act Compliance)

**As the tool's user, you have the right to:**

* Access: View all your stored assessments at any time
* Correction: Edit assessment data if errors occur
* Erasure: Delete individual assessments or entire database
* Portability: Export all data to Excel format

**How to exercise your rights:**

```bash
# View all assessments (access)
sqlite3 data/processed/dpdpa_compliance.db "SELECT * FROM business_profiles;"

# Delete specific assessment (erasure)
sqlite3 data/processed/dpdpa_compliance.db "DELETE FROM business_profiles WHERE business_id='XXXX';"

# Delete entire database (complete erasure)
rm data/processed/dpdpa_compliance.db

# Export to Excel (portability)
# Use dashboard's "Download Excel Report" button
```

### Security Measures

**This tool implements:**

* Local-only storage (data never leaves your machine)
* No authentication required (no password vulnerabilities)
* No network exposure (no remote attack surface)
* Open source code (auditable by security experts)

**You should implement:**

* Disk encryption on your computer (BitLocker/FileVault)
* Regular backups of assessment data (if valuable)
* Access control to your computer (password protection)
* Antivirus/antimalware software

### Third-Party Dependencies

**This tool uses open-source Python packages:**

* streamlit (web framework)
* pandas (data processing)
* plotly (visualizations)
* openpyxl (Excel export)
* PyMuPDF (PDF parsing)

**These packages may:**

* Have their own privacy policies
* Collect telemetry (check individual package documentation)
* Contact package repositories for updates

**To minimize external contact:**

```bash
# Install packages once, then run offline
pip install -r requirements.txt
# Disconnect internet
streamlit run app.py --server.enableCORS=false
```

### Deletion Instructions

**To completely remove all data:**

```bash
# Stop the dashboard
# Press Ctrl+C in terminal

# Delete database
rm data/processed/dpdpa_compliance.db

# Delete downloaded Excel reports (if any)
rm -rf data/processed/assessment_results/

# Uninstall tool
cd ..
rm -rf DPDPA/

# Delete virtual environment
rm -rf venv/
```

---

## Technical Architecture

### System Design

**Technology Stack:**

* **Backend:** Python 3.13
* **Web Framework:** Streamlit 1.40.2
* **Database:** SQLite 3.x (local, file-based)
* **Data Processing:** Pandas 2.2.3
* **Visualization:** Plotly 5.24.1
* **Export:** openpyxl 3.1.5
* **PDF Parsing:** PyMuPDF 1.24.13

**Architecture Pattern:**

```
┌─────────────────────────────────────────┐
│     Web UI (Streamlit Pages)           │
│  Home | Assessment | Results | About    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     Assessment Engine (Core Logic)      │
│  Profiler | Matcher | Analyzer | Report │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     Database Layer (SQLite)             │
│  Requirements | Penalties | Profiles    │
└─────────────────────────────────────────┘
```

### Database Schema

**9 Tables:**

1. **requirements** (47 rows)
   * requirement_id (PK)
   * rule_number (e.g., "Rule 6(1)(a)")
   * requirement_text (extracted verbatim)
   * obligation_type (notice/security/breach/etc.)
   * penalty_category_id (FK)
   * is_sdf_specific (boolean)
   * implementation_complexity (Low/Medium/High)
2. **penalties** (6 rows)
   * penalty_category_id (PK)
   * category_name (security_breach, breach_notification, etc.)
   * amount_inr (Rs. 10,000 to Rs. 2,50,00,00,000)
   * act_reference (Section 33)
3. **business_profiles** (grows with usage)
   * business_id (PK, UUID)
   * business_name
   * entity_type
   * user_count
   * created_at (timestamp)
   * extended_data (JSON blob for 15 answers)
4. **compliance_status** (junction table)
   * status_id (PK)
   * business_id (FK)
   * requirement_id (FK)
   * is_completed (boolean, inferred)
   * completion_date (nullable)
5. **schedule_references** (Third Schedule thresholds)
   * schedule_id (PK)
   * entity_type
   * threshold_users
   * retention_requirements
6. **assessments** (audit trail)
   * assessment_id (PK)
   * business_id (FK)
   * assessment_date
   * compliance_score
   * total_penalty_exposure
7. **implementation_templates** (future use)
   * template_id (PK)
   * requirement_id (FK)
   * template_text (privacy notice templates, etc.)
8. **audit_logs** (future use)
   * log_id (PK)
   * business_id (FK)
   * action (assessment, export, etc.)
   * timestamp
9. **notifications** (future use)
   * notification_id (PK)
   * business_id (FK)
   * message
   * priority

### Core Algorithms

**Requirement Matching:**

```python
def match_requirements(business_profile):
    applicable = []
  
    # Universal (ALL businesses)
    applicable += get_universal_requirements()  # Rules 3, 6, 7, 9, 14
  
    # Conditional
    if business_profile['user_count'] >= threshold:
        applicable += get_third_schedule_requirements()
  
    if business_profile['processes_children_data']:
        applicable += get_children_requirements()  # Rule 10
  
    if business_profile['cross_border_transfers']:
        applicable += get_cross_border_requirements()  # Rule 15
  
    if business_profile['has_processors']:
        applicable += get_processor_requirements()  # Rule 6(1)(f)
  
    # SDF (pending government notification)
    if is_significant_data_fiduciary(business_profile):
        applicable += get_sdf_requirements()  # Rule 13
  
    return applicable
```

**Gap Analysis:**

```python
def analyze_gaps(business_id, applicable_requirements, answers):
    completed = []
    gaps = []
  
    for req in applicable_requirements:
        is_complete = infer_completion(req, answers)
      
        if is_complete:
            completed.append(req)
        else:
            gaps.append(req)
  
    compliance_score = len(completed) / len(applicable_requirements) * 100
  
    # Priority scoring
    for gap in gaps:
        gap['priority_score'] = calculate_priority(
            penalty_amount=gap['penalty_amount'],
            days_remaining=(DEADLINE - today).days,
            complexity=gap['implementation_complexity']
        )
  
    gaps.sort(key=lambda x: x['priority_score'], reverse=True)
  
    return {
        'compliance_score': compliance_score,
        'completed': completed,
        'gaps': gaps,
        'total_penalty_exposure': sum(g['penalty_amount'] for g in gaps)
    }
```

**Completion Inference:**

```python
def infer_completion(requirement, answers):
    # Rule 3 (Notice)
    if requirement['rule_number'].startswith('Rule 3'):
        return answers['has_consent_mechanism']
  
    # Rule 6 (Security) - ALL 4 measures required
    if requirement['rule_number'].startswith('Rule 6'):
        required = {'encryption', 'access_control', 'logging', 'backups'}
        return required.issubset(set(answers['current_security']))
  
    # Rule 7 (Breach)
    if requirement['rule_number'].startswith('Rule 7'):
        return answers['has_breach_plan']
  
    # Rule 10 (Children) - reverse logic
    if requirement['rule_number'].startswith('Rule 10'):
        if not answers['processes_children_data']:
            return True  # N/A
        return not (answers['tracks_behavior'] or answers['targeted_advertising'])
  
    # Rule 14 (Rights)
    if requirement['rule_number'].startswith('Rule 14'):
        return answers['has_grievance_system']
  
    # Default: incomplete
    return False
```

### Performance Considerations

**Database Queries:**

* All queries use indexed columns (requirement_id, business_id)
* No N+1 query problems (proper JOINs)
* Query results cached in session state

**Memory Usage:**

* Full database loads into memory (~5 MB)
* Excel exports use streaming write (no memory spikes)
* Plotly charts render on client-side (no server memory)

**Response Times:**

* Initial load: <2 seconds
* Assessment processing: <1 second (47 requirements, ~1000 calculations)
* Excel export: <3 seconds (5 tabs, 100+ rows)

---

## Deployment Options

### Option 1: Local Use (Recommended for Privacy)

**Advantages:**

* Complete data privacy (nothing leaves your machine)
* No dependency on external services
* Free forever
* Can run offline

**Disadvantages:**

* Must install Python and dependencies
* Only accessible from your computer
* No team collaboration features

**Instructions:** See "Quick Start - Local Installation" above

### Option 2: Streamlit Cloud (Free Hosting)

**Advantages:**

* Free hosting (no server costs)
* Accessible from any device with internet
* Automatic HTTPS
* Easy updates via git push

**Disadvantages:**

* Data stored on Streamlit's servers (less private)
* Subject to Streamlit's terms of service
* Resource limits (1 GB RAM, 1 CPU core)

**Instructions:**

1. Create free account at https://share.streamlit.io/
2. Connect your GitHub repository
3. Select branch: `main`
4. Set main file: `app.py`
5. Click "Deploy"
6. Your dashboard will be live at: `https://share.streamlit.io/yourusername/DPDPA`

**Privacy note:** Assessments stored on Streamlit Cloud (US-based servers). Not recommended for sensitive business data.

### Option 3: Self-Hosted Server (Full Control)

**Advantages:**

* Complete control over infrastructure
* Can enable authentication and multi-user
* Scalable to unlimited users
* Keep data in India for compliance

**Disadvantages:**

* Requires server administration skills
* Monthly hosting costs (Rs. 500-5000)
* Must manage security updates

**Instructions (AWS/DigitalOcean/Linode):**

```bash
# On your server (Ubuntu 20.04+)
# Install Python 3.13
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv

# Clone repo
git clone https://github.com/Tushar-9802/DPDPA.git
cd DPDPA

# Setup
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/extraction/init_db.py
python src/extraction/extract_requirements.py

# Run with production settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Optional: Setup systemd service for auto-restart
sudo nano /etc/systemd/system/dpdpa-dashboard.service
```

**Docker option:**

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python src/extraction/init_db.py && \
    python src/extraction/extract_requirements.py

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t dpdpa-dashboard .
docker run -p 8501:8501 -v $(pwd)/data:/app/data dpdpa-dashboard
```

---

## Troubleshooting

### Common Issues

**1. "ModuleNotFoundError: No module named 'streamlit'"**

```bash
# Solution: Virtual environment not activated
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Then reinstall:
pip install -r requirements.txt
```

**2. "Database file not found"**

```bash
# Solution: Database not initialized
python src/extraction/init_db.py
python src/extraction/extract_requirements.py

# Verify:
ls data/processed/dpdpa_compliance.db
```

**3. "Port 8501 is already in use"**

```bash
# Solution: Change port
streamlit run app.py --server.port 8502

# Or kill existing process:
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
# macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

**4. "Requirements count is wrong (73 instead of 47)"**

```bash
# Solution: Database accumulated duplicates (old bug)
rm data/processed/dpdpa_compliance.db
python src/extraction/init_db.py
python src/extraction/extract_requirements.py

# Verify:
python -c "import sqlite3; c=sqlite3.connect('data/processed/dpdpa_compliance.db'); print('Requirements:', c.execute('SELECT COUNT(*) FROM requirements').fetchone()[0])"
# Should print: Requirements: 47
```

**5. "Penalties are 10x too high (Rs. 2,500 crore)"**

```bash
# Solution: Old penalty bug
sqlite3 data/processed/dpdpa_compliance.db "UPDATE penalties SET amount_inr = amount_inr / 10"

# Verify:
sqlite3 data/processed/dpdpa_compliance.db "SELECT category_name, amount_inr/10000000 as crore FROM penalties ORDER BY amount_inr DESC"
# Should show: security_breach | 250.0
```

**6. "Excel export fails"**

```bash
# Solution: Missing openpyxl
pip install openpyxl==3.1.5

# Or reinstall all:
pip install -r requirements.txt
```

**7. "Charts not displaying (dark mode issue)"**

```bash
# Solution: Clear Streamlit cache
streamlit cache clear
# Then restart:
streamlit run app.py
```

---

## Contributing

### How to Contribute

Contributions are welcome! This is an open-source project aimed at helping Indian businesses achieve DPDP compliance.

**Ways to contribute:**

1. Report bugs or issues
2. Suggest new features
3. Improve documentation
4. Add new requirement extraction logic
5. Enhance UI/UX
6. Translate to regional languages

**Contribution Guidelines:**

1. **Fork the repository**
   ```bash
   # On GitHub, click "Fork"
   git clone https://github.com/yourusername/DPDPA.git
   cd DPDPA
   ```
2. **Create feature branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. **Make changes**
   * Follow PEP 8 style guide
   * Add comments for complex logic
   * Update README if needed
4. **Test your changes**
   ```bash
   # Run full assessment flow
   streamlit run app.py
   # Test with various business profiles
   ```
5. **Commit with clear messages**
   ```bash
   git commit -m "feat: Add SDF obligation checker"
   # Or:
   git commit -m "fix: Correct Third Schedule threshold for gaming"
   # Or:
   git commit -m "docs: Update installation instructions for macOS"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/YourFeatureName
   ```
7. **Open Pull Request**
   * Go to original repository
   * Click "New Pull Request"
   * Select your branch
   * Describe your changes
   * Wait for review

### Development Setup

```bash
# Clone repo
git clone https://github.com/Tushar-9802/DPDPA.git
cd DPDPA

# Create dev environment
python3.13 -m venv venv-dev
source venv-dev/bin/activate

# Install dev dependencies (including testing tools)
pip install -r requirements.txt
pip install pytest black flake8

# Run linter
flake8 src/ --max-line-length=120

# Format code
black src/ --line-length=120

# Run tests (when added)
pytest tests/
```

### Feature Requests

Open an issue on GitHub with:

* Clear description of the feature
* Use case (why it's valuable)
* Proposed implementation (if you have ideas)
* Screenshots/mockups (if UI-related)

### Bug Reports

Open an issue on GitHub with:

* Steps to reproduce
* Expected behavior
* Actual behavior
* Screenshots/error messages
* Python version, OS, browser

---

## Acknowledgments

This project exists thanks to:

**Legal Framework:**

* Ministry of Electronics and Information Technology (MEITY) for publishing DPDP Act and Rules
* Parliament of India for enacting the Digital Personal Data Protection Act, 2023
* Data Protection Board of India (to be constituted)

**Technical Infrastructure:**

* Streamlit team for the excellent web framework
* Python Software Foundation for Python 3.13
* pandas, plotly, PyMuPDF, and other open-source library maintainers

**Inspiration:**

* Indian startup ecosystem's need for accessible compliance tools
* High cost of legal consulting (Rs. 5-10 lakhs) creating barrier to entry
* Complexity of 200+ page regulations requiring technical extraction

**Community:**

* Early testers who provided feedback
* Legal professionals who validated requirement extraction
* Developers who contributed code and documentation

---

## License

MIT License

Copyright (c) 2024 Tushar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**Note:** The DPDP Act, 2023 and DPDP Rules, 2025 are government publications and are in the public domain in India.

---

## Support & Contact

**GitHub Repository:**
https://github.com/Tushar-9802/DPDPA

**Report Issues:**
https://github.com/Tushar-9802/DPDPA/issues

**Discussions:**
https://github.com/Tushar-9802/DPDPA/discussions

**For business inquiries or collaboration:**
[Your professional email or LinkedIn]

**For legal questions:**
Please consult a qualified data protection lawyer. The tool developers cannot provide legal advice.

---

## Citation

If you use this tool in academic research, business reports, or publications, please cite:

```
DPDPA Compliance Dashboard
Automated Assessment Tool for India's Digital Personal Data Protection Act, 2023
Tushar (2024)
https://github.com/Tushar-9802/DPDPA
```

---

## Roadmap

### Completed (v1.0)

* [X] PDF requirement extraction (47 requirements from 200+ pages)
* [X] SQLite database with full schema (9 tables)
* [X] 15-question assessment form
* [X] Requirement matching logic (universal + conditional)
* [X] Gap analysis with compliance scoring
* [X] Priority scoring algorithm (penalty + urgency + complexity)
* [X] Excel export with 5-tab reports
* [X] Interactive Streamlit dashboard (5 pages)
* [X] Penalty exposure calculations
* [X] Illegal activity detection (children violations)
* [X] Past assessments view
* [X] Demo mode for instant testing
* [X] Dynamic personalized action plans
* [X] Plotly charts (pie, gauge, bar)
* [X] Dark mode toggle
* [X] DPDP reference page

### Planned (v1.1) - Q1 2025

* [ ] Loading spinners during analysis
* [ ] Better empty states with CTAs
* [ ] Tooltips on all questions
* [ ] Score explainers ("What does 78% mean?")
* [ ] Link requirements to DPDP reference page
* [ ] Error boundaries for graceful failures
* [ ] Mobile-responsive CSS
* [ ] Performance optimizations (caching, lazy loading)
* [ ] Deployment config for Streamlit Cloud
* [ ] Automated testing script

### Future (v2.0) - Mid 2025

**If Open Source Route:**

* [ ] AI-powered implementation suggestions
* [ ] PDF export (in addition to Excel)
* [ ] Timeline view (Gantt chart for implementation)
* [ ] Multi-language support (Hindi, Tamil, Bengali)
* [ ] Requirement details page (full text + examples)
* [ ] Template library (privacy notices, consent forms)

**If Commercial Route:**

* [ ] Multi-tenant architecture
* [ ] User authentication and teams
* [ ] Progress tracking and reminders
* [ ] License key system
* [ ] Automated update notifications
* [ ] Integration with legal document generators
* [ ] API access for consultants

**Enterprise Features:**

* [ ] SAML/SSO integration
* [ ] Role-based access control
* [ ] Audit logging and compliance reports
* [ ] Custom branding (white-label)
* [ ] On-premise deployment option

---

## Appendix

### Useful Links

**Official Government Resources:**

* MEITY Website: https://www.meity.gov.in/
* DPDP Act 2023 Full Text: https://www.meity.gov.in/writereaddata/files/Digital%20Personal%20Data%20Protection%20Act%202023.pdf
* DPDP Rules 2025: https://www.meity.gov.in/writereaddata/files/DPDP%20Rules%202025.pdf
* Data Protection Board: https://www.dpb.gov.in/ (to be launched)

**Industry Resources:**

* Internet and Mobile Association of India (IAMAI): https://www.iamai.in/
* nasscom Privacy Initiative: https://nasscom.in/knowledge-center/publications/data-privacy
* DSCI (Data Security Council of India): https://www.dsci.in/

**International Comparisons:**

* EU GDPR Official Site: https://gdpr.eu/
* California CCPA: https://oag.ca.gov/privacy/ccpa
* UK Data Protection Act: https://www.gov.uk/data-protection

### Compliance Checklist

**Before May 13, 2027, ALL Indian businesses must:**

**Universal Requirements (Applies to Everyone):**

* [ ] Publish privacy notice in clear, plain language (Rule 3)
* [ ] Obtain free, specific, informed, unconditional, unambiguous consent (Section 6)
* [ ] Implement data encryption (in transit and at rest) (Rule 6)
* [ ] Implement access control mechanisms (Rule 6)
* [ ] Enable comprehensive logging (retain 1 year minimum) (Rule 6)
* [ ] Implement backup and recovery procedures (Rule 6)
* [ ] Document breach response plan (Rule 7)
* [ ] Enable 72-hour notification to Data Protection Board (Rule 7)
* [ ] Notify affected Data Principals of breaches (Rule 7)
* [ ] Publish contact information (name, address, email) (Rule 9)
* [ ] Implement data retention schedules (Rule 8)
* [ ] Provide 48-hour warning before data deletion (Rule 8)
* [ ] Setup grievance redressal system (Rule 14)
* [ ] Respond to grievances within 90 days (Rule 14)
* [ ] Enable Data Principal rights (access, correction, erasure, nomination) (Section 11)

**Conditional Requirements:**

**If you process children's data (under 18):**

* [ ] Obtain verifiable parental consent (Rule 10)
* [ ] PROHIBIT behavioral tracking of children (Rule 10)
* [ ] PROHIBIT targeted advertising to children (Rule 10)
* [ ] Implement age verification mechanism (Rule 10)

**If you have >20M users (e-commerce/social media) or >5M users (gaming):**

* [ ] Comply with Third Schedule data retention requirements
* [ ] Implement enhanced security for large datasets
* [ ] Prepare for potential SDF designation

**If you use Data Processors (vendors):**

* [ ] Update contracts with security safeguards (Rule 6)
* [ ] Ensure processors comply with DPDP Act
* [ ] Verify processors' security measures

**If designated as Significant Data Fiduciary (pending notification):**

* [ ] Appoint Data Protection Officer (DPO) based in India (Rule 13)
* [ ] Conduct annual Data Protection Impact Assessment (DPIA) (Rule 13)
* [ ] Conduct annual independent audit (Rule 13)
* [ ] Perform algorithmic due diligence for AI systems (Rule 13)
* [ ] Publish annual transparency report (Rule 13)

**If you transfer data outside India:**

* [ ] Monitor MEITY notifications for restricted countries (Rule 15)
* [ ] Ensure adequate safeguards in destination country (Rule 15)

### Penalty Calculator

Use this formula to estimate your maximum penalty exposure:

```
Total Exposure = Σ (Penalty per Violation × Number of Violations)

Example 1: Startup with no security measures
- Rule 6 (8 violations × Rs. 250 Cr) = Rs. 2,000 Cr
- Rule 7 (13 violations × Rs. 200 Cr) = Rs. 2,600 Cr
- Rule 3 (5 violations × Rs. 50 Cr) = Rs. 250 Cr
- Rule 14 (6 violations × Rs. 50 Cr) = Rs. 300 Cr
TOTAL = Rs. 5,150 Cr maximum exposure

Example 2: Compliant startup (only 1 security gap)
- Rule 6 (1 violation × Rs. 250 Cr) = Rs. 250 Cr
TOTAL = Rs. 250 Cr maximum exposure

Reduction through compliance:
Rs. 5,150 Cr - Rs. 250 Cr = Rs. 4,900 Cr risk reduction (95% improvement)
```

### Implementation Timeline Suggestions

**18 months before deadline (November 2025):**

* Complete initial assessment
* Budget for compliance (Rs. 2-10 lakhs)
* Hire consultant or assign internal team

**15 months before deadline (February 2026):**

* Implement Rule 6 (security measures) - highest priority
* Draft privacy notice (Rule 3)
* Begin procurement of security tools

**12 months before deadline (May 2026):**

* Implement Rule 7 (breach response plan)
* Setup grievance system (Rule 14)
* Train employees on DPDP requirements

**9 months before deadline (August 2026):**

* Implement children's data protections (Rule 10) if applicable
* Review and update all vendor contracts (processors)
* Begin internal audit

**6 months before deadline (November 2026):**

* Re-assess compliance score (target: 90%+)
* Fix remaining gaps
* Document all measures for audit trail

**3 months before deadline (February 2027):**

* Final compliance check (target: 100%)
* Legal review of all documentation
* Employee training refresher

**1 month before deadline (April 2027):**

* Final readiness verification
* Backup all compliance documentation
* Prepare for Data Protection Board registration (if required)

**Deadline (May 13, 2027):**

* Full compliance achieved
* Ongoing monitoring and maintenance

---

**Last Updated:** December 22, 2024

**Version:** 1.0.2 (Production Ready)

**Days to Deadline:** 510

**Built with care for the Indian startup ecosystem**
