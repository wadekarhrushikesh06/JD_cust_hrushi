"""
Build base templates for Data Engineer and Oracle DBA resumes.
Recreates the exact visual layout, typography, colors, and margins from the source PDFs.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=0, bottom=0, left=0, right=0):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_bottom_border(paragraph, color_hex="1E293B", sz="12"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="{sz}" w:space="2" w:color="{color_hex}"/></w:pBdr>')
    pPr.append(pBdr)

def build_de_template(docx_path):
    doc = Document()
    
    # Page setup - A4
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.40)
    section.bottom_margin = Inches(0.35)
    section.left_margin = Inches(0.50)
    section.right_margin = Inches(0.50)
    
    primary_color = RGBColor(15, 23, 42) # Slate 900
    text_color = RGBColor(30, 41, 59)    # Slate 800
    muted_color = RGBColor(71, 85, 105)  # Slate 600

    # Header Name
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    p_name.paragraph_format.line_spacing = 1.0
    r_name = p_name.add_run("HRUSHIKESH WADEKAR")
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(18)
    r_name.font.bold = True
    r_name.font.color.rgb = primary_color

    # Header Contact
    p_contact = doc.add_paragraph()
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(8)
    p_contact.paragraph_format.line_spacing = 1.0
    r_contact = p_contact.add_run("Mumbai, Maharashtra, India  |  +91 7249224098  |  wadekarhrushikesh3@gmail.com  |  linkedin.com/in/hrushikeshwadekar")
    r_contact.font.name = "Calibri"
    r_contact.font.size = Pt(8.5)
    r_contact.font.color.rgb = muted_color

    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.0
        add_bottom_border(p, color_hex="1E293B", sz="8")
        r = p.add_run(title)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = primary_color
        return p

    # 1. PROFESSIONAL SUMMARY
    add_section_header("PROFESSIONAL SUMMARY")
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(1)
    p_sum.paragraph_format.space_after = Pt(4)
    p_sum.paragraph_format.line_spacing = 1.08
    
    # We can write runs with bolding
    runs_data = [
        ("Certified Data Engineer (", False),
        ("Snowflake SnowPro Core, AWS Solutions Architect, Databricks Data Engineer", True),
        (") with 2+ years of experience engineering high-throughput batch ETL/ELT pipelines in the ", False),
        ("BFSI / Banking", True),
        (" domain. Proven expertise at ", False),
        ("Tata Consultancy Services (Client: State Bank of India)", True),
        (" processing ", False),
        ("4.45M+ daily transaction records", True),
        (" across 12-hour settlement cycles using ", False),
        ("PySpark, SQL, Apache Airflow, and Oracle DB", True),
        (". Skilled in resolving Spark Out-Of-Memory (OOM) bottlenecks, architecting Kimball dimensional models, and deploying automated financial reconciliation frameworks with 99.8% SLA reliability.", False)
    ]
    for text, bold in runs_data:
        r = p_sum.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = bold
        r.font.color.rgb = text_color

    # 2. CERTIFICATIONS
    add_section_header("CERTIFICATIONS")
    certs = [
        ("Snowflake SnowPro Core Certification", "Snowflake Inc.", "Issued: Jul 2026", "ID: S159845-260728-COF"),
        ("AWS Certified Solutions Architect – Associate", "Amazon Web Services (AWS)", "Issued: Jun 2026", "ID: fd461ec57a104b2381260114d1a42bf1"),
        ("Databricks Certified Data Engineer Associate", "Databricks", "Issued: Sep 2026", "ID: 193994560")
    ]
    for name, issuer, date, cred_id in certs:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(1)
        p_c.paragraph_format.space_after = Pt(0)
        p_c.paragraph_format.line_spacing = 1.02
        p_c.paragraph_format.left_indent = Inches(0.18)
        
        # Bullet char
        r_b = p_c.add_run("•  ")
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(8.5)
        r_b.font.bold = True
        
        r_name = p_c.add_run(name)
        r_name.font.name = "Calibri"
        r_name.font.size = Pt(8.5)
        r_name.font.bold = True
        
        r_sep = p_c.add_run(" — ")
        r_sep.font.name = "Calibri"
        r_sep.font.size = Pt(8.5)
        
        r_iss = p_c.add_run(issuer)
        r_iss.font.name = "Calibri"
        r_iss.font.size = Pt(8.5)
        r_iss.font.italic = True
        
        # Right aligned date via tab or spaces
        r_sp = p_c.add_run(f"    ({date})")
        r_sp.font.name = "Calibri"
        r_sp.font.size = Pt(8.0)
        r_sp.font.color.rgb = muted_color

        # Credential ID
        p_id = doc.add_paragraph()
        p_id.paragraph_format.space_before = Pt(0)
        p_id.paragraph_format.space_after = Pt(1)
        p_id.paragraph_format.line_spacing = 1.0
        p_id.paragraph_format.left_indent = Inches(0.32)
        r_id = p_id.add_run(cred_id)
        r_id.font.name = "Consolas"
        r_id.font.size = Pt(7.5)
        r_id.font.color.rgb = muted_color

    # 3. TECHNICAL SKILLS
    add_section_header("TECHNICAL SKILLS")
    skills_lines = [
        ("Big Data & Processing", "Apache Spark (PySpark, Spark SQL), Broadcast Joins, Partitioning, Shuffle Optimization, OOM Debugging"),
        ("Workflow Orchestration", "Apache Airflow (DAG Design, Scheduling, Task Dependencies, Failure Alerting, SLA Monitoring)"),
        ("Cloud & Warehouses", "Snowflake (Virtual Warehouses, Data Modeling, SnowSQL), AWS (AWS S3, Cloud Fundamentals), Databricks"),
        ("Databases & Querying", "Oracle Database (Complex Queries, Joins, CTEs, Window Functions, PL/SQL, Performance Tuning)"),
        ("Data Modeling & Design", "Dimensional Modeling (Kimball Star Schema, Snowflake Schema), Fact & Dimension Tables, SCD Type 1 & 2"),
        ("Languages & Scripting", "Python (ETL Scripting, Data Structures), SQL (Advanced Transformations), Bash / Shell Scripting"),
        ("Data Quality & Governance", "Pre/Post-load Financial Reconciliation, Data Validation Checks, Schema Consistency, Audit Compliance"),
        ("Tools & Operating Systems", "Linux")
    ]
    for cat, items in skills_lines:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.space_before = Pt(0)
        p_s.paragraph_format.space_after = Pt(1)
        p_s.paragraph_format.line_spacing = 1.05
        p_s.paragraph_format.left_indent = Inches(0.0)
        
        r_cat = p_s.add_run(f"{cat}: ")
        r_cat.font.name = "Calibri"
        r_cat.font.size = Pt(8.5)
        r_cat.font.bold = True
        r_cat.font.color.rgb = primary_color
        
        r_it = p_s.add_run(items)
        r_it.font.name = "Calibri"
        r_it.font.size = Pt(8.5)
        r_it.font.color.rgb = text_color

    # 4. WORK EXPERIENCE
    add_section_header("WORK EXPERIENCE")
    
    # Role + Company header
    p_exp_hdr = doc.add_paragraph()
    p_exp_hdr.paragraph_format.space_before = Pt(2)
    p_exp_hdr.paragraph_format.space_after = Pt(0)
    p_exp_hdr.paragraph_format.line_spacing = 1.0
    
    r_role = p_exp_hdr.add_run("Data Engineer")
    r_role.font.name = "Calibri"
    r_role.font.size = Pt(9.0)
    r_role.font.bold = True
    
    r_sep = p_exp_hdr.add_run(" — ")
    r_sep.font.name = "Calibri"
    r_sep.font.size = Pt(9.0)
    
    r_comp = p_exp_hdr.add_run("Tata Consultancy Services (Client: State Bank of India)")
    r_comp.font.name = "Calibri"
    r_comp.font.size = Pt(9.0)
    r_comp.font.italic = True
    
    # Dates
    r_dt = p_exp_hdr.add_run("                       Apr 2024 – Present")
    r_dt.font.name = "Calibri"
    r_dt.font.size = Pt(8.5)
    r_dt.font.bold = True
    r_dt.font.color.rgb = primary_color

    # Sub-project line
    p_proj_sub = doc.add_paragraph()
    p_proj_sub.paragraph_format.space_before = Pt(0)
    p_proj_sub.paragraph_format.space_after = Pt(2)
    p_proj_sub.paragraph_format.line_spacing = 1.0
    
    r_p_sub = p_proj_sub.add_run("Project: Vendors Payment & Settlement System (VPS)")
    r_p_sub.font.name = "Calibri"
    r_p_sub.font.size = Pt(8.5)
    r_p_sub.font.bold = True
    
    r_loc = p_proj_sub.add_run("                                        Mumbai, India")
    r_loc.font.name = "Calibri"
    r_loc.font.size = Pt(8.0)
    r_loc.font.italic = True
    r_loc.font.color.rgb = muted_color

    exp_bullets = [
        ("High-Throughput Batch Ingestion:", " Architected and maintained end-to-end batch ETL pipelines ingesting 4.45M+ transaction hits across 12-hour daily settlement cycles from core banking Oracle staging environments into analytics datamarts."),
        ("Airflow Orchestration & SLA Adherence:", " Scheduled and monitored 20+ production Apache Airflow DAGs, implementing robust task dependencies and automated alerting mechanisms that sustained a 99.8% workflow success rate."),
        ("Spark Performance Tuning & RCA:", " Diagnosed and eliminated recurring PySpark Out-of-Memory (OOM) exceptions and data skew by implementing broadcast joins, optimal repartitioning, and shuffle partition tuning, cutting pipeline downtime by 30%."),
        ("Financial Ledger Reconciliation:", " Engineered automated pre-load and post-load reconciliation scripts in SQL and PySpark to cross-verify debit/credit ledger balances and transaction counts, driving a 25% improvement in data accuracy for audit compliance."),
        ("Database & Query Optimization:", " Refactored complex SQL transformations, indexing, and batch loading procedures in Oracle DB, slashing batch execution runtimes by 20% and improving reporting throughput.")
    ]
    for lead, text in exp_bullets:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_before = Pt(1)
        p_b.paragraph_format.space_after = Pt(1)
        p_b.paragraph_format.line_spacing = 1.06
        p_b.paragraph_format.left_indent = Inches(0.18)
        
        r_dot = p_b.add_run("•  ")
        r_dot.font.name = "Calibri"
        r_dot.font.size = Pt(8.5)
        
        r_ld = p_b.add_run(lead)
        r_ld.font.name = "Calibri"
        r_ld.font.size = Pt(8.5)
        r_ld.font.bold = True
        
        r_tx = p_b.add_run(text)
        r_tx.font.name = "Calibri"
        r_tx.font.size = Pt(8.5)
        r_tx.font.color.rgb = text_color

    # 5. TECHNICAL PROJECTS
    add_section_header("TECHNICAL PROJECTS")
    
    p_pr_title = doc.add_paragraph()
    p_pr_title.paragraph_format.space_before = Pt(2)
    p_pr_title.paragraph_format.space_after = Pt(0)
    p_pr_title.paragraph_format.line_spacing = 1.0
    r_prt = p_pr_title.add_run("Automated REST API Batch Ingestion & Dimensional Warehouse Pipeline")
    r_prt.font.name = "Calibri"
    r_prt.font.size = Pt(8.8)
    r_prt.font.bold = True

    p_pr_tech = doc.add_paragraph()
    p_pr_tech.paragraph_format.space_before = Pt(0)
    p_pr_tech.paragraph_format.space_after = Pt(2)
    p_pr_tech.paragraph_format.line_spacing = 1.0
    r_tech = p_pr_tech.add_run("Technologies: Python, PySpark, Snowflake, AWS S3, SQL, Dimensional Modeling (Star Schema)")
    r_tech.font.name = "Calibri"
    r_tech.font.size = Pt(7.8)
    r_tech.font.italic = True
    r_tech.font.color.rgb = muted_color

    proj_bullets = [
        "Built a modular batch ingestion framework in Python fetching semi-structured JSON payloads from multi-endpoint REST APIs with automated pagination, token handling, and robust retry mechanisms.",
        "Executed scalable distributed transformations using PySpark to clean, flatten nested JSON schemas, and enforce schema validation rules prior to staging on AWS S3.",
        "Designed and deployed a Kimball Star Schema data warehouse in Snowflake, structuring normalized dimension tables (SCD Type 1) and transactional fact tables for business intelligence queries.",
        "Implemented automated data quality assertions verifying row counts, primary key uniqueness, and null constraints across analytical datasets."
    ]
    for pb in proj_bullets:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_before = Pt(1)
        p_b.paragraph_format.space_after = Pt(1)
        p_b.paragraph_format.line_spacing = 1.05
        p_b.paragraph_format.left_indent = Inches(0.18)
        
        r_dot = p_b.add_run("•  ")
        r_dot.font.name = "Calibri"
        r_dot.font.size = Pt(8.5)
        
        r_tx = p_b.add_run(pb)
        r_tx.font.name = "Calibri"
        r_tx.font.size = Pt(8.5)
        r_tx.font.color.rgb = text_color

    # 6. EDUCATION
    add_section_header("EDUCATION")
    
    p_edu1 = doc.add_paragraph()
    p_edu1.paragraph_format.space_before = Pt(1)
    p_edu1.paragraph_format.space_after = Pt(0)
    p_edu1.paragraph_format.line_spacing = 1.0
    r_e1_d = p_edu1.add_run("Master of Computer Applications (MCA)")
    r_e1_d.font.name = "Calibri"
    r_e1_d.font.size = Pt(8.5)
    r_e1_d.font.bold = True
    r_e1_dt = p_edu1.add_run("                                                      2025 – 2027 (Pursuing)")
    r_e1_dt.font.name = "Calibri"
    r_e1_dt.font.size = Pt(8.5)
    r_e1_dt.font.bold = True

    p_edu1_inst = doc.add_paragraph()
    p_edu1_inst.paragraph_format.space_before = Pt(0)
    p_edu1_inst.paragraph_format.space_after = Pt(2)
    p_edu1_inst.paragraph_format.line_spacing = 1.0
    r_e1_in = p_edu1_inst.add_run("G. H. Raisoni College of Engineering and Management (KBC NMU), Jalgaon")
    r_e1_in.font.name = "Calibri"
    r_e1_in.font.size = Pt(8.0)
    r_e1_in.font.color.rgb = muted_color

    p_edu2 = doc.add_paragraph()
    p_edu2.paragraph_format.space_before = Pt(1)
    p_edu2.paragraph_format.space_after = Pt(0)
    p_edu2.paragraph_format.line_spacing = 1.0
    r_e2_d = p_edu2.add_run("Bachelor of Computer Applications (BCA)")
    r_e2_d.font.name = "Calibri"
    r_e2_d.font.size = Pt(8.5)
    r_e2_d.font.bold = True
    r_e2_dt = p_edu2.add_run("                                                      2020 – 2023")
    r_e2_dt.font.name = "Calibri"
    r_e2_dt.font.size = Pt(8.5)
    r_e2_dt.font.bold = True

    p_edu2_inst = doc.add_paragraph()
    p_edu2_inst.paragraph_format.space_before = Pt(0)
    p_edu2_inst.paragraph_format.space_after = Pt(2)
    p_edu2_inst.paragraph_format.line_spacing = 1.0
    r_e2_in = p_edu2_inst.add_run("R. C. Patel Arts, Commerce and Science College (KBC NMU), Shirpur  |  CGPA: 9.62 / 10.0")
    r_e2_in.font.name = "Calibri"
    r_e2_in.font.size = Pt(8.0)
    r_e2_in.font.color.rgb = muted_color

    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
    doc.save(docx_path)
    print(f"Saved {docx_path}")

def build_dba_template(docx_path):
    doc = Document()
    
    # Page setup - Letter
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.45)
    section.bottom_margin = Inches(0.40)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)

    primary_color = RGBColor(0, 0, 0)
    text_color = RGBColor(0, 0, 0)

    # Name (Left aligned, all caps, bold)
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    p_name.paragraph_format.line_spacing = 1.0
    r_name = p_name.add_run("HRUSHIKESH WADEKAR")
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(17)
    r_name.font.bold = True
    r_name.font.color.rgb = primary_color

    # Contact line
    p_contact = doc.add_paragraph()
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(6)
    p_contact.paragraph_format.line_spacing = 1.0
    r_contact = p_contact.add_run("+91 7249224098 | wadekarhrushikesh3@gmail.com | Mumbai, Maharashtra, India | linkedin.com/in/hrushikeshwadekar")
    r_contact.font.name = "Calibri"
    r_contact.font.size = Pt(9.0)
    r_contact.font.color.rgb = text_color

    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(title)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = primary_color
        return p

    # 1. PROFESSIONAL SUMMARY
    add_section_header("PROFESSIONAL SUMMARY")
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(1)
    p_sum.paragraph_format.space_after = Pt(3)
    p_sum.paragraph_format.line_spacing = 1.06
    r_sum = p_sum.add_run(
        "Oracle Database Administrator with 2+ years of experience supporting mission-critical production databases for the State Bank of India project at Tata Consultancy Services. Experienced in Oracle Database 19c/23ai, Grid Infrastructure, RAC, ASM, RMAN Backup & Recovery, Oracle Data Guard, Oracle GoldenGate Microservices, performance tuning, Linux administration, disaster recovery, patching, database security, and production support."
    )
    r_sum.font.name = "Calibri"
    r_sum.font.size = Pt(9.0)

    # 2. PROFESSIONAL EXPERIENCE
    add_section_header("PROFESSIONAL EXPERIENCE")
    
    p_job = doc.add_paragraph()
    p_job.paragraph_format.space_before = Pt(2)
    p_job.paragraph_format.space_after = Pt(0)
    p_job.paragraph_format.line_spacing = 1.0
    r_j = p_job.add_run("Tata Consultancy Services (TCS) | Database Administrator")
    r_j.font.name = "Calibri"
    r_j.font.size = Pt(9.5)
    r_j.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.line_spacing = 1.0
    r_sub = p_sub.add_run("Client: State Bank of India | Apr 2024 – Present")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.0)

    bullets = [
        "Installed and configured Oracle Grid Infrastructure and Oracle RAC environments.",
        "Installed, configured and administered Oracle Database 19c/23ai on Linux.",
        "Managed Oracle ASM disk groups and storage administration.",
        "Performed Oracle Home patching using OPatch and OPatchAuto in standalone and RAC environments.",
        "Configured and administered Oracle Data Guard, standby databases, switchover and DR drill activities.",
        "Installed and administered Oracle GoldenGate 23ai (Microservices Architecture).",
        "Configured Extract, Data Pump and Replicat processes, Distribution Paths and Receiver Paths.",
        "Monitored replication lag, trail files, checkpoint tables and resolved GoldenGate process failures.",
        "Performed RMAN full/incremental backups, restore, recovery, cloning and archive log management.",
        "Implemented Transparent Data Encryption (TDE) and managed database security.",
        "Analyzed AWR, ASH and ADDM reports for database performance tuning.",
        "Resolved blocking sessions, long-running SQLs, listener/TNS issues, FRA and archive log problems.",
        "Automated DBA health checks using Shell scripting and SQL scripts.",
        "Provided 24×7 production support while meeting SLA commitments."
    ]
    for b in bullets:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_before = Pt(0.5)
        p_b.paragraph_format.space_after = Pt(0.5)
        p_b.paragraph_format.line_spacing = 1.04
        p_b.paragraph_format.left_indent = Inches(0.18)
        
        r_dot = p_b.add_run("•  ")
        r_dot.font.name = "Calibri"
        r_dot.font.size = Pt(9.0)
        
        r_t = p_b.add_run(b)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(9.0)

    # 3. TECHNICAL SKILLS
    add_section_header("TECHNICAL SKILLS")
    skills = [
        ("Databases", "Oracle Database 19c, Oracle Database 23ai"),
        ("Grid & High Availability", "Oracle Grid Infrastructure, Oracle RAC, ASM, Oracle Data Guard"),
        ("Oracle GoldenGate", "Installation, Microservices, Service Manager, GGSCI, Admin Client, Extract, Data Pump, Replicat, Trail Files, Checkpoint Tables, Distribution Paths, Receiver Paths, Integrated Extract & Replicat, Replication Monitoring & Troubleshooting"),
        ("Backup & Recovery", "RMAN, Flashback Database, Restore & Recovery, Database Cloning"),
        ("Performance Tuning", "AWR, ASH, ADDM, SQL Tuning, SGA/PGA Tuning, Wait Event Analysis"),
        ("Security", "Transparent Data Encryption (TDE), Users, Roles, Profiles, Auditing"),
        ("Networking", "Oracle Net, Listener, TNS, SCAN Listener"),
        ("Languages", "SQL, PL/SQL, Shell Scripting"),
        ("Operating System", "RHEL Linux")
    ]
    for cat, text in skills:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.space_before = Pt(0.5)
        p_s.paragraph_format.space_after = Pt(0.5)
        p_s.paragraph_format.line_spacing = 1.04
        p_s.paragraph_format.left_indent = Inches(0.18)
        
        r_dot = p_s.add_run("•  ")
        r_dot.font.name = "Calibri"
        r_dot.font.size = Pt(9.0)
        
        r_cat = p_s.add_run(f"{cat}: ")
        r_cat.font.name = "Calibri"
        r_cat.font.size = Pt(9.0)
        r_cat.font.bold = True
        
        r_val = p_s.add_run(text)
        r_val.font.name = "Calibri"
        r_val.font.size = Pt(9.0)

    # 4. EDUCATION
    add_section_header("EDUCATION")
    
    # MCA
    p_edu1 = doc.add_paragraph()
    p_edu1.paragraph_format.space_before = Pt(1)
    p_edu1.paragraph_format.space_after = Pt(0)
    p_edu1.paragraph_format.line_spacing = 1.0
    r_e1_d = p_edu1.add_run("Master of Computer Applications (MCA) — ")
    r_e1_d.font.name = "Calibri"
    r_e1_d.font.size = Pt(9.0)
    r_e1_d.font.bold = True
    r_e1_i = p_edu1.add_run("G. H. Raisoni College of Engineering and Management (KBC NMU), Jalgaon")
    r_e1_i.font.name = "Calibri"
    r_e1_i.font.size = Pt(9.0)
    r_e1_dt = p_edu1.add_run("  (2025 – 2027 Pursuing)")
    r_e1_dt.font.name = "Calibri"
    r_e1_dt.font.size = Pt(8.5)
    r_e1_dt.font.italic = True

    # BCA
    p_edu2 = doc.add_paragraph()
    p_edu2.paragraph_format.space_before = Pt(0.5)
    p_edu2.paragraph_format.space_after = Pt(1)
    p_edu2.paragraph_format.line_spacing = 1.0
    r_e2_d = p_edu2.add_run("Bachelor of Computer Applications (BCA) — ")
    r_e2_d.font.name = "Calibri"
    r_e2_d.font.size = Pt(9.0)
    r_e2_d.font.bold = True
    r_e2_i = p_edu2.add_run("R. C. Patel Arts, Commerce and Science College (KBC NMU), Shirpur")
    r_e2_i.font.name = "Calibri"
    r_e2_i.font.size = Pt(9.0)
    r_e2_dt = p_edu2.add_run("  (2020 – 2023 | CGPA: 9.62 / 10.0)")
    r_e2_dt.font.name = "Calibri"
    r_e2_dt.font.size = Pt(8.5)
    r_e2_dt.font.italic = True

    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
    doc.save(docx_path)
    print(f"Saved {docx_path}")

if __name__ == "__main__":
    build_de_template("templates/data_engineer.docx")
    build_dba_template("templates/oracle_dba.docx")
