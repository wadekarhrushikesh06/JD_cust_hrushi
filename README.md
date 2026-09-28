# Local Resume Tailoring Agent

A local, deterministic agentic pipeline designed to tailor software and data resumes strictly against an immutable **Source of Truth** (SOT) for specific Job Descriptions (JDs).

> [!IMPORTANT]
> **Privacy Notice:** This repository contains personal contact details, education history, and career credentials. It is strongly advised to keep this GitHub repository **Private**.

---

## 📌 Core Philosophy & Non-Negotiable Rules

1. **Source of Truth is Immutable:** Nothing is ever invented. No new skills, tools, employers, titles, dates, certifications, projects, or metrics.
2. **Numbers & Metrics are Read-Only:** Percentages, transaction volumes, SLA rates, and downtime improvements cannot be changed, rounded, or added to unquantified bullets.
3. **Reword, Reorder, and Select Only:** Bullets and skills are selected and reordered to highlight relevance to the target JD. Minor truthful mirroring of JD terms is permitted only when backed by SOT evidence.
4. **Skills Gaps are Kept in the Report:** Missing requirements are reported as gaps in `report.md`, never stuffed into the resume.
5. **Pixel-Perfect Single-Page Formatting:** Output strictly adheres to single-page, ATS-compliant formats matching the original DOCX/PDF styling.

---

## 📂 Repository Structure

```text
./
├── PROMPT_PACKET.md           # Master agent operating guidelines and rules
├── tracker.csv                # Application tracker (date, role, fit, status, links)
├── taxonomy.md                # Job categorization taxonomy and rules
├── requirements.txt           # Python dependencies
├── .gitignore                 # Standard git ignores (caches, temp files)
├── .gitattributes             # Line endings and binary file handling
├── source_of_truth/           # Canonical profile and experience data
│   ├── profile.yaml           # Personal details, employers, titles, dates, education
│   ├── skills.yaml            # Skills inventory with category and bullet evidence
│   ├── bullets_bank.yaml      # Verbatim bullets with locked metrics & domain tags
│   ├── certs_projects.yaml    # Industry certifications and technical projects
│   └── needs_confirmation.md  # Discrepancy logs & confirmed user decisions
├── templates/                 # Reusable single-page DOCX & reference PDFs
│   ├── data_engineer.docx     # Data Engineer template (A4 single-column)
│   ├── data_engineer.pdf
│   ├── oracle_dba.docx        # Oracle DBA template (Letter single-column)
│   └── oracle_dba.pdf
├── jobs/                      # All tailored application packages
│   ├── _INDEX.md              # Auto-maintained catalog (by Category & by Company)
│   └── <category>/
│       └── <YYYY-MM-DD>_<company>_<role>/
│           ├── jd.md          # Original job description
│           ├── resume.docx    # Tailored DOCX resume
│           ├── resume.pdf     # ATS-compliant rendered PDF
│           └── report.md      # Fit estimate, gap analysis, and changes summary
└── scripts/                   # Core pipeline automation
    ├── render_resume.py       # DOCX generator & Word COM PDF renderer
    ├── validate_resume.py     # Source of truth validator (anti-hallucination)
    ├── index_tracker.py       # Master tracker and jobs/_INDEX.md manager
    └── test_pipeline.py       # End-to-end integration test
```

---

## ⚙️ Prerequisites & Setup

### Prerequisites
- **Operating System:** Windows (utilizes native Microsoft Word COM automation via `docx2pdf` for typography-accurate PDF rendering).
- **Microsoft Office / Word:** Installed on the system.
- **Python:** Python 3.10+ (tested on Python 3.13).

### Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd JD_cust_hrushi
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the end-to-end pipeline test to verify setup:
   ```bash
   python scripts/test_pipeline.py
   ```

---

## 🚀 Workflow (Per-JD Tailoring)

When a new Job Description (JD) is provided, the agent executes the following steps:

1. **Parse:** Extracts company name, job title, location, required technologies, and seniority level.
2. **Route:** Selects the optimal track:
   - `data_engineer` for PySpark, Airflow, Snowflake, AWS, and Big Data roles.
   - `oracle_dba` for Oracle Database, RAC, GoldenGate, RMAN, and Data Guard roles.
3. **Categorize:** Files under `jobs/<category>/<YYYY-MM-DD>_<company>_<role>/` per [`taxonomy.md`](taxonomy.md).
4. **Save JD:** Stores raw JD details in `jd.md`.
5. **Tailor & Render:** Selects relevant bullets and reorders skills, generating `resume.docx` and `resume.pdf`.
6. **Validate:** Runs [`validate_resume.py`](scripts/validate_resume.py) to guarantee zero invented skills or numbers.
7. **Report:** Generates `report.md` detailing fit %, matched must-haves, missing skills/gaps, and change summary.
8. **Index:** Appends to [`tracker.csv`](tracker.csv) and updates [`jobs/_INDEX.md`](jobs/_INDEX.md).

---

## 🛠️ Helper Scripts Reference

- **`scripts/render_resume.py`**:
  ```bash
  python scripts/render_resume.py <tailoring_config.yaml> <output_directory>
  ```
- **`scripts/validate_resume.py`**:
  ```bash
  python scripts/validate_resume.py <resume.docx> [resume.pdf]
  ```
- **`scripts/index_tracker.py`**:
  ```bash
  # Rebuild jobs/_INDEX.md from tracker.csv
  python scripts/index_tracker.py --rebuild

  # Add job entry
  python scripts/index_tracker.py --add --date YYYY-MM-DD --company "Company" --role "Role" --category "technical-data-engineering" --fit_pct 90 --folder_path "jobs/..."
  ```
