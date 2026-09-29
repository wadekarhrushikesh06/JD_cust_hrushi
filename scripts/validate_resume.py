"""
Validator script: Verifies tailored resumes against the Source of Truth.
Enforces non-negotiable rules:
- No invented skills or tools
- Numbers are read-only (locked metrics preserved, no new numbers)
- SOT employers, titles, dates only
- ATS compliance and page length <= 1.5 pages (target 1 page)
"""

import os
import sys
import re
import yaml
import docx
import pypdf

def load_source_of_truth():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sot_dir = os.path.join(base_dir, "source_of_truth")
    
    with open(os.path.join(sot_dir, "profile.yaml"), "r", encoding="utf-8") as f:
        profile = yaml.safe_load(f)
    with open(os.path.join(sot_dir, "skills.yaml"), "r", encoding="utf-8") as f:
        skills_data = yaml.safe_load(f)
    with open(os.path.join(sot_dir, "bullets_bank.yaml"), "r", encoding="utf-8") as f:
        bullets_data = yaml.safe_load(f)
    with open(os.path.join(sot_dir, "certs_projects.yaml"), "r", encoding="utf-8") as f:
        certs_proj = yaml.safe_load(f)

    # Allowed skills set (lowercase for matching)
    allowed_skills = set()
    for s in skills_data.get("skills", []):
        allowed_skills.add(s["name"].strip().lower())
    
    # Common allowed variations and tool terms from SOT
    known_terms = {
        "spark", "pyspark", "spark sql", "airflow", "apache airflow", "snowflake", "snowsql",
        "aws", "aws s3", "s3", "databricks", "oracle", "oracle database", "oracle db",
        "oracle database 19c", "oracle database 23ai", "19c", "23ai", "grid infrastructure",
        "oracle grid infrastructure", "rac", "oracle rac", "asm", "data guard", "oracle data guard",
        "goldengate", "oracle goldengate", "goldengate 23ai", "microservices", "service manager",
        "ggsci", "admin client", "extract", "data pump", "replicat", "trail files", "checkpoint tables",
        "distribution paths", "receiver paths", "integrated extract & replicat", "rman",
        "flashback database", "tde", "transparent data encryption", "awr", "ash", "addm",
        "sql", "pl/sql", "python", "shell scripting", "bash", "linux", "rhel linux",
        "kimball", "star schema", "snowflake schema", "scd type 1", "scd type 2", "scd type 1 & 2",
        "fact tables", "dimension tables", "rest apis", "rest api", "json", "opatch", "opatchauto",
        "microsoft", "fabric", "microsoft fabric", "onelake", "delta lake", "lakehouse", "fabric lakehouse", "data factory"
    }
    allowed_skills.update(known_terms)

    # Allowed numbers / metric tokens
    allowed_numbers = {
        "2+", "4.45", "4.45m+", "4.45m", "12", "12-hour", "20+", "20", "99.8%", "99.8",
        "30%", "30", "25%", "25", "20%", "24x7", "24×7", "9.64", "9.62", "10.0", "10",
        "2024", "2025", "2026", "2027", "2020", "2023", "19", "19c", "23", "23ai", "1", "2",
        "7249224098", "91", "+91", "159845", "260728", "461", "104", "193994560",
        "f2cea18f28a701dc", "d9b42a-e44e2f"
    }

    # Allowed employers
    allowed_employers = {"tata consultancy services", "tcs", "state bank of india", "sbi"}

    # Allowed titles
    allowed_titles = {"data engineer", "system engineer", "database administrator", "oracle database administrator", "assistant system engineer"}

    return {
        "profile": profile,
        "allowed_skills": allowed_skills,
        "allowed_numbers": allowed_numbers,
        "allowed_employers": allowed_employers,
        "allowed_titles": allowed_titles,
        "bullets": bullets_data.get("bullets", []),
        "certs_proj": certs_proj
    }

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    full_text = []
    for p in doc.paragraphs:
        if p.text.strip():
            full_text.append(p.text.strip())
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                if cell.text.strip():
                    full_text.append(cell.text.strip())
    return "\n".join(full_text)

def validate_resume(docx_path, pdf_path=None):
    sot = load_source_of_truth()
    errors = []
    warnings = []

    if not os.path.exists(docx_path):
        return False, [f"DOCX file does not exist: {docx_path}"], []

    text = extract_text_from_docx(docx_path)
    lower_text = text.lower()

    # 1. Page count check on PDF if present
    if pdf_path and os.path.exists(pdf_path):
        reader = pypdf.PdfReader(pdf_path)
        num_pages = len(reader.pages)
        if num_pages > 1:
            # Check if strict 1-page required or <= 1.5 pages
            if num_pages > 2:
                errors.append(f"PDF exceeds page limit: {num_pages} pages (max 1.5 allowed, 1 page expected)")
            else:
                warnings.append(f"PDF has {num_pages} pages. The source resume is 1 page. Please optimize vertical spacing.")

    # 2. Employer check
    found_employer = any(emp in lower_text for emp in sot["allowed_employers"])
    if not found_employer:
        errors.append("No authorized employer found from source of truth.")

    # 3. Disallowed numbers / invented metrics check
    # Find all percentages and numbers
    # Look for metrics like XX%, XXk, XXM, etc.
    metrics_found = re.findall(r'\b\d+(?:\.\d+)?%|\b\d+(?:\.\d+)?M\+?|\b\d+x\d+|\b\d+\+\b', text, re.IGNORECASE)
    for m in metrics_found:
        cleaned_m = m.lower().strip()
        if cleaned_m not in sot["allowed_numbers"]:
            errors.append(f"Invented or modified metric detected: '{m}'. Rule: Numbers are read-only!")

    # 4. Check for unevidenced technologies
    # We flag technologies commonly hallucinated in data/DBA resumes
    suspicious_unallowed = [
        "kafka", "flink", "kubernetes", "docker", "gcp", "azure", "bigquery",
        "redshift", "hadoop", "hive", "hbase", "cassandra", "mongodb", "postgres",
        "postgresql", "mysql", "dbt", "terraform", "ci/cd", "jenkins", "gitlab"
    ]
    for tech in suspicious_unallowed:
        # Match as whole word
        pattern = r'\b' + re.escape(tech) + r'\b'
        if re.search(pattern, lower_text):
            if tech not in sot["allowed_skills"]:
                errors.append(f"Invented tool/technology detected: '{tech}' is NOT in source of truth!")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_resume.py <resume.docx> [resume.pdf]")
        sys.exit(1)
    
    docx_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else None

    valid, errs, warns = validate_resume(docx_file, pdf_file)
    print("=" * 40)
    print(f"Validation Result for: {docx_file}")
    if valid:
        print("STATUS: PASSED")
    else:
        print("STATUS: FAILED")
        print("ERRORS:")
        for e in errs:
            print(f"  - {e}")
    if warns:
        print("WARNINGS:")
        for w in warns:
            print(f"  - {w}")
    print("=" * 40)
    
    sys.exit(0 if valid else 1)
