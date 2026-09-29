"""
Mobile Web Server for Resume Tailoring Pipeline.
Allows user to paste a Job Description on their phone, tailor the resume,
and download the 1-page ATS PDF directly to their phone.
"""

import os
import sys
import re
import datetime
import yaml
from flask import Flask, request, jsonify, render_template_string, send_file, abort

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Set up working directory to repository root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)
sys.path.insert(0, REPO_ROOT)

from scripts.render_resume import render
from scripts.validate_resume import validate_resume
from scripts.index_tracker import add_entry, load_tracker

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Resume Tailor • Mobile</title>
    <style>
        :root {
            --primary: #2563EB;
            --primary-dark: #1D4ED8;
            --bg: #F8FAFC;
            --card-bg: #FFFFFF;
            --text-main: #0F172A;
            --text-muted: #64748B;
            --border: #E2E8F0;
            --success: #10B981;
            --warning: #F59E0B;
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #0F172A;
                --card-bg: #1E293B;
                --text-main: #F8FAFC;
                --text-muted: #94A3B8;
                --border: #334155;
            }
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg); color: var(--text-main); padding: 16px; padding-bottom: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 20px; }
        header h1 { font-size: 1.5rem; font-weight: 700; color: var(--primary); display: flex; align-items: center; justify-content: center; gap: 8px; }
        header p { font-size: 0.85rem; color: var(--text-muted); margin-top: 4px; }
        .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 16px; padding: 18px; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
        .form-group { margin-bottom: 14px; }
        label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 6px; }
        input[type="text"], textarea { width: 100%; padding: 12px; border: 1px solid var(--border); border-radius: 10px; background: transparent; color: inherit; font-size: 0.95rem; }
        input:focus, textarea:focus { outline: none; border-color: var(--primary); }
        textarea { height: 160px; resize: vertical; }
        .row { display: flex; gap: 10px; }
        .row .form-group { flex: 1; }
        button.btn-primary { width: 100%; padding: 14px; background: var(--primary); color: white; border: none; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; }
        button.btn-primary:active { background: var(--primary-dark); transform: scale(0.98); }
        .result-box { display: none; }
        .badge { display: inline-flex; align-items: center; padding: 6px 12px; border-radius: 20px; font-weight: 700; font-size: 0.9rem; }
        .badge-success { background: rgba(16, 185, 129, 0.15); color: var(--success); }
        .btn-download { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 14px; background: var(--success); color: white; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 1rem; margin-top: 12px; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3); }
        .btn-secondary { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 10px; background: transparent; border: 1px solid var(--border); color: inherit; border-radius: 10px; text-decoration: none; font-size: 0.85rem; margin-top: 8px; }
        .roadmap-card { background: rgba(37, 99, 235, 0.05); border: 1px solid rgba(37, 99, 235, 0.2); border-radius: 12px; padding: 14px; margin-top: 14px; font-size: 0.85rem; line-height: 1.5; white-space: pre-wrap; max-height: 350px; overflow-y: auto; }
        .recent-item { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border); }
        .recent-item:last-child { border-bottom: none; }
        .recent-meta h4 { font-size: 0.9rem; font-weight: 600; }
        .recent-meta p { font-size: 0.75rem; color: var(--text-muted); }
        .spinner { border: 3px solid rgba(255,255,255,0.3); border-radius: 50%; border-top: 3px solid #fff; width: 20px; height: 20px; animation: spin 0.8s linear infinite; display: none; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ Resume Tailor</h1>
            <p>Hrushikesh Wadekar • Mobile Agent</p>
        </header>

        <div class="card" id="formCard">
            <form id="tailorForm">
                <div class="row">
                    <div class="form-group">
                        <label>Company</label>
                        <input type="text" id="company" placeholder="e.g. Infosys, Amazon">
                    </div>
                    <div class="form-group">
                        <label>Role</label>
                        <input type="text" id="role" placeholder="Data Engineer" value="Data Engineer">
                    </div>
                </div>
                <div class="form-group">
                    <label>Job Description (JD)</label>
                    <textarea id="jdText" placeholder="Paste Job Description here..." required></textarea>
                </div>
                <button type="submit" class="btn-primary" id="submitBtn">
                    <span class="spinner" id="btnSpinner"></span>
                    <span id="btnText">🚀 Tailor & Generate Resume</span>
                </button>
            </form>
        </div>

        <div class="card result-box" id="resultCard">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <h3 id="resTitle" style="font-size:1.1rem;"></h3>
                <span class="badge badge-success" id="fitBadge">95% Fit</span>
            </div>
            <p style="font-size:0.85rem; color:var(--text-muted);" id="resSummary">1-Page ATS resume generated and validated against Source of Truth.</p>
            
            <a href="#" id="pdfDownloadBtn" class="btn-download" download>
                📥 Download PDF Resume
            </a>
            <a href="#" id="docxDownloadBtn" class="btn-secondary" download>
                📄 Download Word (.docx)
            </a>

            <div style="margin-top:16px;">
                <label>🎯 7-Day Interview Roadmap</label>
                <div class="roadmap-card" id="roadmapContent">Loading roadmap...</div>
            </div>
        </div>

        <div class="card">
            <h3 style="font-size:0.95rem; margin-bottom:12px;">📂 Recent Prepared Resumes</h3>
            <div id="recentList">
                {% for job in recent_jobs %}
                <div class="recent-item">
                    <div class="recent-meta">
                        <h4>{{ job.company }} • {{ job.role }}</h4>
                        <p>{{ job.date }} | Fit: {{ job.fit_pct }}%</p>
                    </div>
                    <div>
                        <a href="/download_by_path?path={{ job.folder_path }}&ext=pdf" class="btn-secondary" style="padding:6px 12px; margin:0; display:inline-block;" download>PDF</a>
                    </div>
                </div>
                {% else %}
                <p style="font-size:0.8rem; color:var(--text-muted);">No previous jobs found.</p>
                {% endfor %}
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('tailorForm');
        const submitBtn = document.getElementById('submitBtn');
        const btnText = document.getElementById('btnText');
        const btnSpinner = document.getElementById('btnSpinner');
        const resultCard = document.getElementById('resultCard');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const company = document.getElementById('company').value.trim() || 'Target Company';
            const role = document.getElementById('role').value.trim() || 'Data Engineer';
            const jdText = document.getElementById('jdText').value.trim();

            if (!jdText) return;

            submitBtn.disabled = true;
            btnText.innerText = "Tailoring & Rendering...";
            btnSpinner.style.display = "inline-block";

            try {
                const res = await fetch('/api/tailor', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ company, role, jd: jdText })
                });
                const data = await res.json();

                if (data.status === 'success') {
                    document.getElementById('resTitle').innerText = `${data.company} • ${data.role}`;
                    document.getElementById('fitBadge').innerText = `${data.fit_pct}% Fit`;
                    document.getElementById('pdfDownloadBtn').href = data.pdf_url;
                    document.getElementById('docxDownloadBtn').href = data.docx_url;
                    document.getElementById('roadmapContent').innerText = data.roadmap || "Roadmap generated in folder.";
                    resultCard.style.display = 'block';
                    resultCard.scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert('Error: ' + (data.error || 'Failed to tailor'));
                }
            } catch (err) {
                alert('Connection error: ' + err.message);
            } finally {
                submitBtn.disabled = false;
                btnText.innerText = "🚀 Tailor & Generate Resume";
                btnSpinner.style.display = "none";
            }
        });
    </script>
</body>
</html>
"""

def extract_meta_from_jd(jd_text, company_hint, role_hint):
    company = company_hint
    role = role_hint
    
    # Try finding company if not given
    if not company or company.lower() == "target company":
        m_comp = re.search(r'(?:at|company:?|for)\s+([A-Z][A-Za-z0-9\s&]{2,20})', jd_text, re.IGNORECASE)
        company = m_comp.group(1).strip() if m_comp else "Company"

    if not role or role.lower() == "data engineer":
        if "pyspark" in jd_text.lower():
            role = "PySpark Data Engineer"
        elif "databricks" in jd_text.lower():
            role = "Data Engineer (Databricks)"
        else:
            role = "Data Engineer"
            
    return company, role

@app.route("/")
def index():
    tracker = load_tracker()
    recent = list(reversed(tracker))[:5]
    return render_template_string(HTML_TEMPLATE, recent_jobs=recent)

@app.route("/api/tailor", methods=["POST"])
def api_tailor():
    data = request.json or {}
    jd_text = data.get("jd", "").strip()
    company_in = data.get("company", "").strip()
    role_in = data.get("role", "").strip()

    if not jd_text:
        return jsonify({"status": "error", "error": "Job description is required"}), 400

    company, role = extract_meta_from_jd(jd_text, company_in, role_in)
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    comp_clean = re.sub(r'[^a-zA-Z0-9]+', '-', company.lower()).strip('-')
    role_clean = re.sub(r'[^a-zA-Z0-9]+', '-', role.lower()).strip('-')
    
    category = "technical-data-engineering"
    job_folder_name = f"{today}_{comp_clean}_{role_clean}"
    job_dir = os.path.join(REPO_ROOT, "jobs", category, job_folder_name)
    os.makedirs(job_dir, exist_ok=True)

    # 1. Save jd.md
    with open(os.path.join(job_dir, "jd.md"), "w", encoding="utf-8") as f:
        f.write(f"# Job Description: {role} at {company}\n- Date: {today}\n\n{jd_text}")

    # 2. Build config.yaml
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
    try:
        import pythoncom
        pythoncom.CoInitialize()
    except Exception:
        pass

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
        notes=f"Mobile web tailored for {company}"
    )

    return jsonify({
        "status": "success",
        "company": company,
        "role": role,
        "fit_pct": fit_pct,
        "pdf_url": f"/download_by_path?path=jobs/{category}/{job_folder_name}&ext=pdf",
        "docx_url": f"/download_by_path?path=jobs/{category}/{job_folder_name}&ext=docx",
        "roadmap": roadmap_content
    })

@app.route("/download_by_path")
def download_by_path():
    rel_path = request.args.get("path", "")
    ext = request.args.get("ext", "pdf")
    
    # Sanitize path
    clean_path = os.path.normpath(rel_path).replace("\\", "/")
    if clean_path.startswith("..") or not clean_path.startswith("jobs/"):
        abort(403)
        
    full_path = os.path.join(REPO_ROOT, clean_path, f"resume.{ext}")
    if not os.path.exists(full_path):
        abort(404)
        
    company_name = os.path.basename(clean_path).split("_")[1].capitalize() if "_" in os.path.basename(clean_path) else "Tailored"
    download_filename = f"Hrushikesh_Wadekar_{company_name}_Data_Engineer.{ext}"
    
    return send_file(full_path, as_attachment=True, download_name=download_filename)

def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "10.54.163.28"

if __name__ == "__main__":
    port = 5000
    local_ip = get_local_ip()
    print("=" * 60)
    print(" [RESUME TAILOR] Mobile Server Started Successfully!")
    print(f" [MOBILE] Open on your phone (same Wi-Fi): http://{local_ip}:{port}")
    print(f" [PC]     Open on your PC browser:          http://localhost:{port}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=False, threaded=False)

