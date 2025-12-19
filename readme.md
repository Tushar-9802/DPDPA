# DPDPA Compliance Dashboard

> Automated compliance assessment tool for India's Digital Personal Data Protection Act, 2023

![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.40.2-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

---

## Overview

The **DPDPA Compliance Dashboard** helps Indian startups and SMBs navigate the complex requirements of the Digital Personal Data Protection Act, 2023. Get instant compliance assessments, identify gaps, and receive a prioritized roadmap to meet the **May 13, 2027** deadline.

### Key Features

* **15-Question Assessment** - Quick compliance evaluation in under 5 minutes
* **Intelligent Gap Analysis** - Identifies exactly which of 50+ requirements apply to your business
* **Priority Scoring** - Focus on high-penalty items first (up to Rs. 250 crore per violation)
* **Automated Reports** - Downloadable Excel reports with detailed roadmaps
* **Illegal Activity Detection** - Warns about DPDP Act Section 9(3) violations
* **Real-time Calculations** - Penalty exposure and compliance score instantly

---

## Quick Start

### Prerequisites

* Python 3.13 or higher
* Windows, macOS, or Linux
* 100 MB free disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dpdpa-dashboard.git
cd dpdpa-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## Usage

### 1. Start New Assessment

Click **"New Assessment"** in the sidebar and answer 15 questions about your business:

* Business information (name, type, user count)
* Data processing activities (children's data, cross-border transfers)
* Current compliance status (security measures, breach plan, consent mechanism)

### 2. View Results

Get instant feedback on:

* **Compliance Score** (0-100%)
* **Total Penalty Exposure** (in Rs. crores)
* **Applicable Requirements** (categorized by type)
* **Top 10 Priority Items** (sorted by risk)

### 3. Download Report

Export detailed Excel report with:

* Executive summary
* Full requirement list
* Gap analysis
* Implementation roadmap

### 4. Track Progress

Return to view past assessments and track compliance improvements over time.

---

## Project Structure

```
DPDPA/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                # UI theme configuration
├── config/
│   └── config.py                  # Project configuration
├── src/
│   ├── assessment/                # Core assessment engine
│   │   ├── questionnaire.py       # 15-question form logic
│   │   ├── business_profiler.py   # Business profile creation
│   │   ├── requirement_matcher.py # Requirement matching logic
│   │   ├── gap_analyzer.py        # Gap analysis & scoring
│   │   └── report_generator.py    # Excel export
│   ├── dashboard/                 # Web UI pages
│   │   └── pages/
│   │       ├── home.py           # Landing page
│   │       ├── assessment.py     # Assessment form
│   │       ├── results.py        # Results dashboard
│   │       └── about.py          # Project information
│   └── data_extraction/          # PDF extraction (Phase 1)
│       ├── parse_rules.py        # PDF text extraction
│       ├── extract_requirements.py # Requirement mining
│       └── init_db.py            # Database initialization
├── data/
│   ├── raw/                      # Original DPDP PDFs
│   │   ├── DPDP_Act_2023.pdf
│   │   └── DPDP_Rules_2025.pdf
│   └── processed/
│       └── dpdpa_compliance.db   # SQLite database
└── README.md                     # This file
```

---

## Technical Architecture

### Database Schema

**9 Tables:**

* `requirements` - 50+ extracted requirements from DPDP Rules 2025
* `penalties` - 6 penalty categories (Rs. 10,000 to Rs. 250 crore)
* `business_profiles` - Stored assessment data
* `compliance_status` - Requirement completion tracking
* `schedule_references` - Third Schedule thresholds
* Others: `assessments`, `implementation_templates`, `audit_logs`, `notifications`

### Assessment Engine

1. **Requirement Matching** - Identifies applicable requirements based on:
   * Business entity type (e-commerce, gaming, fintech, etc.)
   * User count (Third Schedule thresholds)
   * Data processing activities (children, cross-border, processors)
2. **Gap Analysis** - Infers completion from questionnaire answers:
   * Security (Rule 6): All 4 measures → 9 requirements complete
   * Breach (Rule 7): Has plan → 14 requirements complete
   * Notice (Rule 3): Has consent → 6 requirements complete
   * Rights (Rule 14): Has grievance → 7 requirements complete
3. **Priority Scoring** - Weighted formula (0-100):
   * 40% Penalty amount
   * 30% Deadline urgency
   * 30% Implementation complexity

### Data Sources

All requirements extracted from official government documents:

* **DPDP Act 2023** (Enacted August 11, 2023)
* **DPDP Rules 2025** (Notified November 13, 2025)
* **Section 33 Penalty Schedule**
* **Third Schedule** (Data retention requirements)

---

## Deployment

### Streamlit Cloud (Recommended - Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with GitHub
4. Click "New app"
5. Select repository and set main file: `app.py`
6. Click "Deploy"

Your app will be live at: `https://share.streamlit.io/yourusername/dpdpa-dashboard`

### Docker (Optional)

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t dpdpa-dashboard .
docker run -p 8501:8501 dpdpa-dashboard
```

---

## Configuration

### Environment Variables

Create `.env` file (optional):

```env
DB_PATH=data/processed/dpdpa_compliance.db
FULL_COMPLIANCE_DEADLINE=2027-05-13
```

### Streamlit Configuration

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

---

## Testing

### Run Test Suite

```bash
# Test gap analyzer
python src/assessment/gap_analyzer.py

# Test requirement matcher
python src/assessment/requirement_matcher.py

# Test business profiler
python src/assessment/business_profiler.py
```

### Manual Testing

Use these test cases to verify functionality:

**Perfect Compliance (Expected: ~97%)**

```
Business: Perfect Corp
Type: startup
Users: 50,000
Children: No
Security: encryption, access_control, logging, backups
Breach Plan: Yes
Consent: Yes
Grievance: Yes
```

**Poor Compliance (Expected: ~0%)**

```
Business: StartupX
Type: ecommerce
Users: 500,000
Children: No
Security: encryption, access_control
Breach Plan: No
Consent: No
Grievance: No
```

---

## Legal Disclaimer

**IMPORTANT:** This tool provides automated guidance only.

* This is NOT a substitute for professional legal advice
* Consult a qualified data protection lawyer for compliance strategy
* Laws and rules may change - monitor MEITY website for updates
* Final compliance responsibility lies with your organization

---

## Roadmap

### Phase 1: Data Extraction ✅

* [X] PDF parsing (DPDP Act & Rules)
* [X] Requirement extraction (50+ rules)
* [X] Database schema design
* [X] Penalty mapping

### Phase 2: Assessment Engine ✅

* [X] Questionnaire design (15 questions)
* [X] Business profiling logic
* [X] Requirement matching algorithm
* [X] Gap analysis & scoring
* [X] Excel report generation

### Phase 3: Bug Fixes ✅

* [X] Fix compliance scoring (was always 0%)
* [X] Fix penalty calculations (10x error)
* [X] Fix Rule 9 categorization
* [X] Add illegal activity detection

### Phase 4: Dashboard ✅

* [X] Streamlit web interface
* [X] Home page with past assessments
* [X] Interactive assessment form
* [X] Results dashboard
* [X] About page

### Phase 5: Polish (Planned)

* [ ] Add data visualizations (charts, gauges)
* [ ] PDF export functionality
* [ ] Requirement details page
* [ ] Timeline/roadmap view
* [ ] Dark mode support

### Phase 6: Advanced Features (Future)

* [ ] Multi-user support
* [ ] Team collaboration
* [ ] Template library (privacy notices, policies)
* [ ] Automated monitoring
* [ ] Email notifications

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Acknowledgments

* **Data Source:** Ministry of Electronics and Information Technology (MEITY)
* **Legal Framework:** Digital Personal Data Protection Act, 2023
* **Built for:** Indian Startup Ecosystem
* **Inspired by:** Need for accessible compliance tools for SMBs

---

## Support

* **Issues:** [GitHub Issues](https://github.com/yourusername/dpdpa-dashboard/issues)
* **Discussions:** [GitHub Discussions](https://github.com/yourusername/dpdpa-dashboard/discussions)
* **Email:** your.email@example.com

---

## License

This project is licensed under the MIT License - see the [LICENSE](https://claude.ai/chat/LICENSE) file for details.

---

## Citation

If you use this tool in your research or business, please cite:

```
DPDPA Compliance Dashboard
Digital Personal Data Protection Act 2023 Assessment Tool
https://github.com/yourusername/dpdpa-dashboard
2024
```

---

**Built for Indian Startups & SMBs**

**Compliance Deadline:** May 13, 2027 | **Days Remaining:** 509

---

## Appendix

### Compliance Checklist

**Universal Requirements (All Businesses):**

* [ ] Privacy notice published (Rule 3)
* [ ] Security measures implemented (Rule 6)
  * [ ] Encryption
  * [ ] Access control
  * [ ] Logging
  * [ ] Backups
* [ ] Breach response plan (Rule 7)
* [ ] Contact information published (Rule 9)
* [ ] Grievance redressal system (Rule 14)

**Conditional Requirements:**

* [ ] Third Schedule compliance (if >20M users for e-commerce/social media, >5M for gaming)
* [ ] Children's data requirements (if processing data of persons under 18)
* [ ] Cross-border transfer compliance (if transferring data outside India)
* [ ] Data Processor contracts (if using third-party processors)

### Useful Links

* [DPDP Act 2023 Official Text](https://www.meity.gov.in/dpdpa)
* [DPDP Rules 2025](https://www.meity.gov.in/dpdpa-rules)
* [Data Protection Board](https://www.dpb.gov.in/)
* [MEITY Website](https://www.meity.gov.in/)

---

*Last Updated: December 2024*
*Version: 1.0.0 (Phase 4 Complete)*
