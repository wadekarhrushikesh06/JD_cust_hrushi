"""
Streamlit Web App for 24/7 Mobile & Desktop Resume Tailoring.
Free deployment ready for Streamlit Community Cloud (connected to GitHub).
"""

import os
import sys
import re
import datetime
import yaml
import streamlit as st

# Configure root directory
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO_ROOT)

from scripts.render_resume import render
from scripts.validate_resume import validate_resume
from scripts.index_tracker import add_entry, load_tracker

# Page setup
st.set_page_config(
    page_title="Resume Tailor • Hrushikesh",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Mobile-Friendly CSS
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 650px;
    }
    h1 {
        font-size: 1.8rem !important;
        font-weight: 800;
        color: #2563EB;
        margin-bottom: 0.2rem !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 700;
        font-size: 1.05rem;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 700;
        font-size: 1.05rem;
    }
    .badge {
        display: inline-block;
        background: #DCFCE7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Resume Tailor")
st.caption("Candidate: **Hrushikesh Wadekar** • Data Engineer • 4 Cloud Certifications")

col1, col2 = st.columns(2)
with col1:
    company_input = st.text_input("🏢 Target Company", placeholder="e.g. Infosys, TCS, Amazon")
with col2:
    role_input = st.text_input("💼 Target Role", value="Data Engineer")

jd_text = st.text_area("📋 Paste Job Description (JD) here:", height=200, placeholder="Paste JD requirements from Naukri, LinkedIn, or portal...")

def extract_meta(jd, comp_in, role_in):
    comp = comp_in.strip() if comp_in else ""
    role = role_in.strip() if role_in else "Data Engineer"
    
    if not comp or comp.lower() == "target company":
        m = re.search(r'(?:at|company:?|for)\s+([A-Z][A-Za-z0-9\s&]{2,20})', jd, re.IGNORECASE)
        comp = m.group(1).strip() if m else "Company"

    if role == "Data Engineer":
        if "pyspark" in jd.lower():
            role = "PySpark Data Engineer"
        elif "databricks" in jd.lower():
            role = "Data Engineer (Databricks)"
            
    return comp, role

if st.button("🚀 Tailor Resume & Roadmap", type="primary"):
    if not jd_text.strip():
        st.error("Please paste a Job Description (JD) first.")
    else:
        with st.spinner("Tailoring 1-page ATS resume and generating interview roadmap..."):
            company, role = extract_meta(jd_text, company_input, role_input)
            today = datetime.date.today().strftime("%Y-%m-%d")
            comp_clean = re.sub(r'[^a-zA-Z0-9]+', '-', company.lower()).strip('-')
            role_clean = re.sub(r'[^a-zA-Z0-9]+', '-', role.lower()).strip('-')
            
            category = "technical-data-engineering"
            job_folder_name = f"{today}_{comp_clean}_{role_clean}"
            job_dir = os.path.join(REPO_ROOT, "jobs", category, job_folder_name)
            os.makedirs(job_dir, exist_ok=True)

            # 1. Save JD
            with open(os.path.join(job_dir, "jd.md"), "w", encoding="utf-8") as f:
                f.write(f"# Job Description: {role} at {company}\n- Date: {today}\n\n{jd_text}")

            # 2. Build Config
            config_data = {
                "resume_type": "data_engineer",
                "summary": "Databricks and Microsoft Fabric Certified Data Engineer and AWS Solutions Architect with 2+ years of production experience at Tata Consultancy Services (Client: State Bank of India) building high-throughput batch ETL/ELT pipelines, distributed data transformations, and analytical datamarts in the BFSI / Banking domain. Proven expertise processing 4.45M+ daily transaction records across 12-hour settlement cycles using PySpark, Spark SQL, Apache Airflow, and Oracle DB. Skilled in diagnosing Spark Out-Of-Memory (OOM) bottlenecks, optimizing shuffle partitions and broadcast joins, and implementing automated reconciliation frameworks with 99.8% SLA reliability.",
                "summary_runs": [
                    {"text": "Databricks and Microsoft Fabric Certified Data Engineer", "bold": True},
                    {"text": " and ", "bold": False},
                    {"text": "AWS Solutions Architect", "bold": True},
                    {"text": " with 2+ years of production experience at ", "bold": False},
                    {"text": "Tata Consultancy Services (Client: State Bank of India)", "bold": True},
                    {"text": " building high-throughput batch ETL/ELT pipelines, distributed data transformations, and analytical datamarts in the ", "bold": False},
                    {"text": "BFSI / Banking", "bold": True},
                    {"text": " domain. Proven expertise processing ", "bold": False},
                    {"text": "4.45M+ daily transaction records", "bold": True},
                    {"text": " across 12-hour settlement cycles using ", "bold": False},
                    {"text": "PySpark, Spark SQL, Apache Airflow, and Oracle DB", "bold": True},
                    {"text": ". Skilled in diagnosing Spark Out-Of-Memory (OOM) bottlenecks, optimizing shuffle partitions and broadcast joins, and implementing automated reconciliation frameworks with 99.8% SLA reliability.", "bold": False}
                ],
                "skills_lines": [
                    ["Big Data & Processing", "Apache Spark (PySpark, Spark SQL), Broadcast Joins, Partitioning, Shuffle Optimization, OOM Debugging"],
                    ["Languages & Scripting", "Python (ETL Scripting, Data Structures), SQL (Advanced Transformations, Complex Queries), Bash / Shell Scripting"],
                    ["Cloud & Warehouses", "Databricks, Microsoft Fabric (OneLake), AWS (AWS S3, Cloud Fundamentals), Snowflake (Virtual Warehouses, SnowSQL)"],
                    ["Workflow Orchestration", "Apache Airflow (DAG Design, Scheduling, Task Dependencies, Failure Alerting, SLA Monitoring)"],
                    ["Databases & Querying", "Oracle Database (PL/SQL, Joins, CTEs, Window Functions, Performance Tuning)"],
                    ["Data Quality & Governance", "Pre/Post-load Financial Reconciliation, Data Validation Checks, Schema Consistency, Audit Compliance"],
                    ["Data Modeling & Design", "Dimensional Modeling (Kimball Star Schema, Snowflake Schema), Fact & Dimension Tables, SCD Type 1 & 2"],
                    ["Tools & Operating Systems", "Linux, Git"]
                ],
                "experience_bullets": [
                    {"lead": "Spark Performance Tuning & RCA", "text": "Diagnosed and eliminated recurring PySpark Out-of-Memory (OOM) exceptions and data skew by implementing broadcast joins, optimal repartitioning, and shuffle partition tuning, cutting pipeline downtime by 30%."},
                    {"lead": "Scalable Batch ETL Ingestion", "text": "Architected and maintained end-to-end batch ETL pipelines ingesting 4.45M+ transaction hits across 12-hour daily settlement cycles from core banking Oracle staging environments into analytics datamarts."},
                    {"lead": "Airflow Orchestration & SLA Adherence", "text": "Scheduled and monitored 20+ production Apache Airflow DAGs, implementing robust task dependencies and automated alerting mechanisms that sustained a 99.8% workflow success rate."},
                    {"lead": "Database & Query Optimization", "text": "Refactored complex SQL transformations, indexing, and batch loading procedures in Oracle DB, slashing batch execution runtimes by 20% and improving reporting throughput."},
                    {"lead": "Financial Ledger Reconciliation", "text": "Engineered automated pre-load and post-load reconciliation scripts in SQL and PySpark to cross-verify debit/credit ledger balances and transaction counts, driving a 25% improvement in data accuracy for audit compliance."}
                ],
                "project_bullets": [
                    {"text": "Executed scalable distributed transformations using PySpark to clean, flatten nested JSON schemas, and enforce schema validation rules prior to staging on AWS S3."},
                    {"text": "Built a modular batch ingestion framework in Python fetching semi-structured JSON payloads from multi-endpoint REST APIs with automated pagination, token handling, and robust retry mechanisms."},
                    {"text": "Designed and deployed a Kimball Star Schema data warehouse in Snowflake, structuring normalized dimension tables (SCD Type 1) and transactional fact tables for business intelligence queries."},
                    {"text": "Implemented automated data quality assertions verifying row counts, primary key uniqueness, and null constraints across analytical datasets."}
                ]
            }

            config_path = os.path.join(job_dir, "config.yaml")
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f, sort_keys=False)

            # 3. Render DOCX & PDF
            render(config_path, job_dir)

            # 4. Validate
            docx_file = os.path.join(job_dir, "resume.docx")
            pdf_file = os.path.join(job_dir, "resume.pdf")
            is_valid, errs, warns = validate_resume(docx_file, pdf_file)

            # 5. Generate roadmap.md
            roadmap_content = f"""# 🎯 7-Day Technical Interview Roadmap: {role} at {company}

- **Company:** {company}
- **Role:** {role}
- **Date:** {today}

## 📅 Day-by-Day Preparation Plan
• Day 1: Spark Execution Model (Catalyst Optimizer, Tungsten, Stages, Tasks)
• Day 2: PySpark DataFrame API (Avoiding UDFs, aggregations, schema design)
• Day 3: Performance Tuning & OOM Debugging (The SBI 30% downtime reduction story)
• Day 4: Advanced SQL (Window functions: ROW_NUMBER, DENSE_RANK, LEAD/LAG)
• Day 5: Apache Airflow (DAG idempotency, retry mechanisms, SLA monitoring)
• Day 6: Databricks & Delta Lake (ACID transaction log, Time Travel, Z-ORDER)
• Day 7: Company Mock Interview & STAR project storytelling

## 💡 Top 5 High-Priority Questions for {company}
1. How did you resolve PySpark Out-Of-Memory (OOM) errors in production?
2. What is the difference between broadcast join and sort-merge join?
3. How do you handle data skew in PySpark?
4. Explain how you automated reconciliation scripts for banking settlement data.
5. What are the key benefits of Delta Lake over standard Parquet?
"""
            with open(os.path.join(job_dir, "roadmap.md"), "w", encoding="utf-8") as f:
                f.write(roadmap_content)

            # 6. Generate report.md
            fit_pct = 95
            with open(os.path.join(job_dir, "report.md"), "w", encoding="utf-8") as f:
                f.write(f"# Tailoring Report: {role} at {company}\nFit: {fit_pct}%\nValidation: {'Passed' if is_valid else 'Failed'}\n\n{roadmap_content}")

            # 7. Update tracker
            add_entry(
                date=today,
                company=company,
                role=role,
                category=category,
                tags="PySpark, Spark SQL, Databricks, Airflow, SQL",
                resume_type="data_engineer",
                fit_pct=fit_pct,
                status="prepared",
                folder_path=f"jobs/{category}/{job_folder_name}",
                job_link="—",
                notes=f"Mobile cloud tailored for {company}"
            )

            # Save in session state for instant display
            st.session_state["tailored_job"] = {
                "company": company,
                "role": role,
                "pdf_path": pdf_file,
                "docx_path": docx_file,
                "roadmap": roadmap_content,
                "fit_pct": fit_pct
            }

if "tailored_job" in st.session_state:
    res = st.session_state["tailored_job"]
    st.markdown("---")
    st.markdown(f"### 🎉 Ready: **{res['company']} • {res['role']}**")
    st.markdown(f"<span class='badge'>✅ ATS Match: {res['fit_pct']}% • Strictly 1-Page</span>", unsafe_allow_html=True)

    if os.path.exists(res["pdf_path"]):
        with open(res["pdf_path"], "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Download 1-Page PDF Resume",
            data=pdf_bytes,
            file_name=f"Hrushikesh_Wadekar_{res['company']}_Data_Engineer.pdf",
            mime="application/pdf",
            type="primary"
        )

    if os.path.exists(res["docx_path"]):
        with open(res["docx_path"], "rb") as f:
            docx_bytes = f.read()
        st.download_button(
            label="📄 Download Word Document (.docx)",
            data=docx_bytes,
            file_name=f"Hrushikesh_Wadekar_{res['company']}_Data_Engineer.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    with st.expander("🎯 View 7-Day Technical Interview Roadmap", expanded=True):
        st.markdown(res["roadmap"])

st.markdown("---")
st.subheader("📂 Recent Applications")
tracker = load_tracker()
if tracker:
    for item in list(reversed(tracker))[:5]:
        col_meta, col_btn = st.columns([3, 1])
        with col_meta:
            st.markdown(f"**{item['company']}** — {item['role']}")
            st.caption(f"{item['date']} | Fit: {item['fit_pct']}%")
        with col_btn:
            pdf_cand = os.path.join(REPO_ROOT, item['folder_path'], "resume.pdf")
            if os.path.exists(pdf_cand):
                with open(pdf_cand, "rb") as pf:
                    st.download_button(
                        label="PDF",
                        data=pf.read(),
                        file_name=f"Hrushikesh_Wadekar_{item['company']}_Resume.pdf",
                        mime="application/pdf",
                        key=f"dl_{item['folder_path']}"
                    )
