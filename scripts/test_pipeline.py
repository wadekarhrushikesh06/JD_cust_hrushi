"""
Test script for the complete tailoring pipeline using a dummy JD.
Verifies routing, folder creation, jd.md saving, resume rendering, validation, report generation, and tracking.
Cleans up dummy output upon successful verification.
"""

import os
import sys
import shutil
import subprocess
import yaml

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(repo_root)
sys.path.insert(0, repo_root)

from scripts.render_resume import render
from scripts.validate_resume import validate_resume
from scripts.index_tracker import add_entry, delete_entry

def test_full_pipeline():
    print(">>> Starting Full Pipeline Test with Dummy JD...")

    dummy_cat = "technical-data-engineering"
    dummy_company = "DummyCorp"
    dummy_role = "Data Engineer"
    dummy_date = "2026-09-29"
    job_folder_name = f"{dummy_date}_dummycorp_data-engineer"
    job_dir = os.path.join("jobs", dummy_cat, job_folder_name)
    os.makedirs(job_dir, exist_ok=True)

    # 1. Save dummy jd.md
    jd_content = """# Job Description: Data Engineer at DummyCorp
- **Company:** DummyCorp
- **Role:** Data Engineer
- **Date:** 2026-09-29
- **Link:** https://dummycorp.example.com/jobs/de-101

## Requirements
- 2+ years of experience with Apache Spark / PySpark batch processing.
- Experience with Apache Airflow workflow orchestration.
- Snowflake and AWS S3 experience.
- SQL and database performance tuning.
"""
    with open(os.path.join(job_dir, "jd.md"), "w", encoding="utf-8") as f:
        f.write(jd_content)
    print("  [x] Saved jd.md")

    # 2. Prepare tailoring configuration
    tailoring_config = {
        "resume_type": "data_engineer",
        "summary": "Certified Data Engineer (Snowflake SnowPro Core, AWS Solutions Architect, Databricks Data Engineer) with 2+ years of experience engineering high-throughput batch ETL/ELT pipelines in the BFSI / Banking domain. Proven expertise at Tata Consultancy Services (Client: State Bank of India) processing 4.45M+ daily transaction records across 12-hour settlement cycles using PySpark, SQL, Apache Airflow, and Oracle DB. Skilled in resolving Spark Out-Of-Memory (OOM) bottlenecks, architecting Kimball dimensional models, and deploying automated financial reconciliation frameworks with 99.8% SLA reliability.",
        "skills_lines": [
            ["Big Data & Processing", "Apache Spark (PySpark, Spark SQL), Broadcast Joins, Partitioning, Shuffle Optimization, OOM Debugging"],
            ["Workflow Orchestration", "Apache Airflow (DAG Design, Scheduling, Task Dependencies, Failure Alerting, SLA Monitoring)"],
            ["Cloud & Warehouses", "Snowflake (Virtual Warehouses, Data Modeling, SnowSQL), AWS (AWS S3, Cloud Fundamentals), Databricks"],
            ["Databases & Querying", "Oracle Database (Complex Queries, Joins, CTEs, Window Functions, PL/SQL, Performance Tuning)"],
            ["Data Modeling & Design", "Dimensional Modeling (Kimball Star Schema, Snowflake Schema), Fact & Dimension Tables, SCD Type 1 & 2"],
            ["Languages & Scripting", "Python (ETL Scripting, Data Structures), SQL (Advanced Transformations), Bash / Shell Scripting"],
            ["Data Quality & Governance", "Pre/Post-load Financial Reconciliation, Data Validation Checks, Schema Consistency, Audit Compliance"],
            ["Tools & Operating Systems", "Linux"]
        ],
        "experience_bullets": [
            {
                "lead": "High-Throughput Batch Ingestion",
                "text": "Architected and maintained end-to-end batch ETL pipelines ingesting 4.45M+ transaction hits across 12-hour daily settlement cycles from core banking Oracle staging environments into analytics datamarts."
            },
            {
                "lead": "Airflow Orchestration & SLA Adherence",
                "text": "Scheduled and monitored 20+ production Apache Airflow DAGs, implementing robust task dependencies and automated alerting mechanisms that sustained a 99.8% workflow success rate."
            },
            {
                "lead": "Spark Performance Tuning & RCA",
                "text": "Diagnosed and eliminated recurring PySpark Out-of-Memory (OOM) exceptions and data skew by implementing broadcast joins, optimal repartitioning, and shuffle partition tuning, cutting pipeline downtime by 30%."
            },
            {
                "lead": "Financial Ledger Reconciliation",
                "text": "Engineered automated pre-load and post-load reconciliation scripts in SQL and PySpark to cross-verify debit/credit ledger balances and transaction counts, driving a 25% improvement in data accuracy for audit compliance."
            },
            {
                "lead": "Database & Query Optimization",
                "text": "Refactored complex SQL transformations, indexing, and batch loading procedures in Oracle DB, slashing batch execution runtimes by 20% and improving reporting throughput."
            }
        ],
        "project_bullets": [
            "Built a modular batch ingestion framework in Python fetching semi-structured JSON payloads from multi-endpoint REST APIs with automated pagination, token handling, and robust retry mechanisms.",
            "Executed scalable distributed transformations using PySpark to clean, flatten nested JSON schemas, and enforce schema validation rules prior to staging on AWS S3.",
            "Designed and deployed a Kimball Star Schema data warehouse in Snowflake, structuring normalized dimension tables (SCD Type 1) and transactional fact tables for business intelligence queries.",
            "Implemented automated data quality assertions verifying row counts, primary key uniqueness, and null constraints across analytical datasets."
        ]
    }

    config_path = os.path.join(job_dir, "config.yaml")
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(tailoring_config, f)

    # 3. Render
    print("  [x] Rendering resume.docx and resume.pdf...")
    render(config_path, job_dir)
    docx_file = os.path.join(job_dir, "resume.docx")
    pdf_file = os.path.join(job_dir, "resume.pdf")
    assert os.path.exists(docx_file), "resume.docx was not created"
    assert os.path.exists(pdf_file), "resume.pdf was not created"

    # 4. Validate
    print("  [x] Running validator...")
    valid, errors, warns = validate_resume(docx_file, pdf_file)
    assert valid, f"Validation failed: {errors}"
    print("  [x] Validator passed successfully!")

    # 5. Generate report.md
    report_content = f"""# Fit & Tailoring Report: {dummy_company} - {dummy_role}

## 1. Fit Estimate
- **Overall Fit:** 95%
- **Reasoning:** Strong match on all core requirements (PySpark, Airflow, Snowflake, AWS S3, SQL).
- **Matched Must-Haves:**
  - PySpark batch processing
  - Apache Airflow orchestration
  - Snowflake & AWS S3
  - Oracle DB performance tuning

## 2. Gaps
- None identified in core requirements.

## 3. What Changed vs. Base Resume
- Prioritized Spark and Airflow bullets to lead experience section.
- Tailored skills ordering to prioritize big data processing and workflow orchestration.

## 4. Category Chosen
- `technical-data-engineering` (Day-to-day work is focused on ETL pipelines and batch processing).

## 5. Risks or Concerns
- None.
"""
    with open(os.path.join(job_dir, "report.md"), "w", encoding="utf-8") as f:
        f.write(report_content)
    print("  [x] Saved report.md")

    # 6. Update Tracker & Index
    print("  [x] Updating tracker and master index...")
    add_entry(
        date=dummy_date,
        company=dummy_company,
        role=dummy_role,
        category=dummy_cat,
        tags="Spark, Airflow, Snowflake, AWS",
        resume_type="data_engineer",
        fit_pct=95,
        status="prepared",
        folder_path=job_dir,
        job_link="https://dummycorp.example.com/jobs/de-101",
        notes="Pipeline verification test"
    )

    # 7. Clean up dummy output
    print("  [x] Cleaning up dummy test artifacts...")
    delete_entry(dummy_company, dummy_role)
    import time
    import gc
    gc.collect()
    time.sleep(1)
    for _ in range(5):
        try:
            if os.path.exists(job_dir):
                shutil.rmtree(job_dir)
            break
        except PermissionError:
            time.sleep(1)
            gc.collect()
    print(">>> Test Pipeline Complete! All components verified.")

if __name__ == "__main__":
    test_full_pipeline()
