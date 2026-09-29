"""
Script to generate the comprehensive Architecture & Deployment Guide as a professional PDF.
Outputs to:
  - C:\\Users\\admin\\OneDrive\\Desktop\\Resume_Tailor_Architecture_and_Deployment_Guide.pdf
  - C:\\Users\\admin\\OneDrive\\Desktop\\JD_cust_hrushi\\Resume_Tailor_Architecture_and_Deployment_Guide.pdf
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)
from scripts.render_resume import convert_to_pdf

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, text_runs, bg_hex="F1F5F9", border_color="2563EB"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    for run_text, is_bold in text_runs:
        r = p.add_run(run_text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = is_bold
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_documentation_docx(out_docx):
    doc = Document()
    
    # Page Margins
    for sec in doc.sections:
        sec.top_margin = Inches(0.7)
        sec.bottom_margin = Inches(0.7)
        sec.left_margin = Inches(0.75)
        sec.right_margin = Inches(0.75)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("Resume Tailor Engine: Architecture & Cloud Deployment")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A) # Deep Navy Blue

    # Subtitle / Metadata
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Complete End-to-End System Documentation, Guardrail Design, and Streamlit Cloud Deployment Guide\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    r_meta = p_sub.add_run("Author: Hrushikesh Wadekar | Role: Data Engineer | Date: September 2026 | Deployment: Streamlit Community Cloud (24/7 Free)")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9.0)
    r_meta.font.bold = True
    r_meta.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        # Bottom border
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="3" w:color="2563EB"/></w:pBdr>')
        pPr.append(pBdr)

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    def add_p(text, bold_prefix=None, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(10.0)
            rb.font.bold = True
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10.0)
        r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    def add_bullet(lead, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.12
        r_lead = p.add_run(lead + ": ")
        r_lead.font.name = "Calibri"
        r_lead.font.size = Pt(9.5)
        r_lead.font.bold = True
        r_lead.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        r_body = p.add_run(text)
        r_body.font.name = "Calibri"
        r_body.font.size = Pt(9.5)
        r_body.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # 1. Executive Summary
    add_h1("1. Executive Summary")
    add_p("The Resume Tailor system is an enterprise-grade, deterministic resume customization and technical interview preparation engine. Built specifically for high-throughput technical recruitment (Data Engineering, Big Data, Cloud Architecture), the system bridges the gap between applicant tracking systems (ATS) and human technical screeners by solving three fundamental problems:")
    add_bullet("Anti-Hallucination Guarantee", "Unlike standard LLM-based resume builders that invent false experiences, tools, or dates, this system strictly isolates the candidate's career data inside an immutable Source of Truth (SOT). Only verified credentials and production metrics are permitted.")
    add_bullet("Strict 1-Page Layout Engineering", "Human recruiters spend 6 to 8 seconds scanning resumes. The auto-fitting typography engine calculates layout geometry and guarantees every generated PDF fits on strictly 1 single page without awkward bottom whitespace or two-page spillovers.")
    add_bullet("24/7 Mobile Cloud Access", "Deployed to Streamlit Community Cloud (connected to GitHub), the platform allows the candidate to copy any Job Description (JD) on a smartphone, generate a tailored ATS resume in 5 seconds, download the PDF, and apply directly via mobile portals with zero laptop dependency.")

    # 2. Architecture & Components
    add_h1("2. Core Architecture & Pipeline Components")
    add_callout(doc, [
        ("Pipeline Flow: ", True),
        ("Job Description (JD) → NLP Keyword Extraction & SOT Matcher → Config Synthesis → Deterministic ATS Validator → Auto-Fitting Word/PDF Renderer → 7-Day Technical Interview Roadmap → Tracker & Cloud Sync.", False)
    ])

    add_h2("A. Source of Truth (SOT) Data Layer")
    add_p("Located in the source_of_truth/ directory, this layer acts as the single source of verified career records:")
    add_bullet("profile.yaml", "Stores verified candidate identity, contact information, employer records (TCS / State Bank of India), client projects (Vendors Payment & Settlement System), and official titles.")
    add_bullet("skills.yaml", "Exhaustive taxonomy of technical proficiencies across 8 distinct categories (Big Data, Languages, Cloud & Warehouses, Orchestration, Databases, Data Quality, Modeling, Tools) tagged with certification associations.")
    add_bullet("certs_projects.yaml", "Maintains real verified certifications (Databricks Data Engineer Associate, AWS Solutions Architect Associate, AWS Cloud Practitioner, and Microsoft Certified: Fabric Data Engineer Associate ID: F2CEA18F28A701DC) and production projects.")
    add_bullet("bullets_bank.yaml", "Pre-approved STAR-format metric bullets (Situation, Task, Action, Result) capturing real impact: 4.45M+ daily transaction hits, 12-hour settlement cycles, 30% pipeline downtime cut, and 99.8% SLA adherence.")

    add_h2("B. Deterministic ATS Validation Engine (scripts/validate_resume.py)")
    add_p("Before any resume is exported, an automated validator executes strict integrity assertions:")
    add_bullet("SOT Keyword Whitelist", "Every single bullet, company, and skill is matched against the SOT. If an unapproved keyword or fabricated metric appears, validation fails immediately.")
    add_bullet("Certification Verifiers", "Ensures credential IDs, issuance dates, and expiration dates match official certifying authority records.")
    add_bullet("Banned Buzzwords Guardrail", "Rejects non-actionable fluff phrases (e.g. 'results-driven team player') in favor of concrete engineering terminology.")

    # 3. Typography & 1-Page Engineering
    add_h1("3. Auto-Fitting Typography & Single-Page Engineering")
    add_p("One of the most technically complex challenges in automated resume generation is ensuring the output fills exactly one page regardless of bullet variations. Our custom rendering engine in scripts/render_resume.py implements several innovations:")
    add_bullet("Native Right-Aligned Tab Stops", "Replaced brittle space-padded alignment with native Word tab stops (WD_TAB_ALIGNMENT.RIGHT at Inches(7.27) with tab characters). Dates and locations remain perfectly flush against the right margin across all devices.")
    add_bullet("Dual-Profile Typography Engine", "Includes 'spacious' (19pt name, 10pt headers, 9.0pt body, 1.08-1.10 line spacing) and 'compact' (17pt name, 9.5pt headers, 8.5pt body, 1.02 line spacing) calibrated profiles.")
    add_bullet("Automated Page-Count Feedback Loop", "After rendering, pypdf programmatically inspects the output PDF. If page count > 1, the engine automatically rolls back, selects the compact profile, and re-renders to guarantee a strict 1-page fit.")
    add_bullet("Cross-Platform Converter (convert_to_pdf)", "Uses Microsoft Word COM automation via docx2pdf on Windows local machines, and automatically falls back to headless LibreOffice (libreoffice --headless --convert-to pdf) on Linux cloud environments.")

    # 4. Roadmap Engine
    add_h1("4. Dedicated 7-Day Technical Interview Roadmap Engine")
    add_p("Generating a resume is only half the battle; the candidate must clear the technical interview. Every tailoring execution automatically generates a dedicated roadmap.md inside the job directory containing:")
    add_bullet("Day 1 - Spark Architecture", "Deep dive into Catalyst Optimizer, Tungsten execution engine, DAG scheduling, Stages, and Tasks.")
    add_bullet("Day 2 - PySpark DataFrame API", "Transformation patterns, avoidance of Python UDFs, broadcast joins, and partitioned data loading.")
    add_bullet("Day 3 - Performance Tuning & OOM Debugging", "The core SBI production story: diagnosing Out-Of-Memory exceptions, tuning spark.sql.shuffle.partitions, and eliminating data skew.")
    add_bullet("Day 4 - Advanced SQL Transformations", "Analytical window functions (ROW_NUMBER, DENSE_RANK, LEAD/LAG), CTEs, and Oracle PL/SQL optimization.")
    add_bullet("Day 5 - Orchestration & Resiliency", "Apache Airflow DAG design, idempotency, failure retries, and SLA alerting.")
    add_bullet("Day 6 - Cloud Lakehouse & Delta Architecture", "Databricks & Microsoft Fabric, ACID transaction log, time travel, and Z-ORDER indexing.")
    add_bullet("Day 7 - Company Mock Interview", "STAR-format project walkthrough and company-specific question drills.")

    # 5. Cloud Deployment Guide
    add_h1("5. 100% Free 24/7 Cloud Deployment on Streamlit Cloud")
    add_p("To eliminate laptop dependency when applying on mobile, the system is deployed to Streamlit Community Cloud (backed by Snowflake) connected directly to GitHub (wadekarhrushikesh06/JD_cust_hrushi):")

    tbl_cloud = doc.add_table(rows=5, cols=2)
    tbl_cloud.alignment = WD_TABLE_ALIGNMENT.CENTER
    cloud_rows = [
        ("Deployment Attribute", "Implementation Detail"),
        ("Cloud Platform", "Streamlit Community Cloud (Free Tier, 24/7 Hosting, Zero Cost Forever)"),
        ("Billing / Card Required?", "None. 100% Free for GitHub developers (Zero credit/debit card needed)"),
        ("Linux Headless Packages", "packages.txt specifies libreoffice, fonts-liberation, fonts-dejavu for cloud PDF rendering"),
        ("Application Entry Point", "app.py provides a touch-friendly mobile interface with 1-click PDF download & roadmap preview")
    ]
    for idx, (c1, c2) in enumerate(cloud_rows):
        row = tbl_cloud.rows[idx]
        cell_a, cell_b = row.cells[0], row.cells[1]
        cell_a.text = c1
        cell_b.text = c2
        if idx == 0:
            set_cell_background(cell_a, "1E3A8A")
            set_cell_background(cell_b, "1E3A8A")
            cell_a.paragraphs[0].runs[0].font.bold = True
            cell_a.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            cell_b.paragraphs[0].runs[0].font.bold = True
            cell_b.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        else:
            set_cell_background(cell_a, "F8FAFC" if idx % 2 == 0 else "FFFFFF")
            set_cell_background(cell_b, "F8FAFC" if idx % 2 == 0 else "FFFFFF")
            cell_a.paragraphs[0].runs[0].font.size = Pt(9.0)
            cell_b.paragraphs[0].runs[0].font.size = Pt(9.0)
            cell_a.paragraphs[0].runs[0].font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 6. Step-by-Step Replication
    add_h1("6. Universal Setup & Replication for Any Candidate")
    add_p("To configure this exact platform for a new candidate or different machine, follow this 4-step sequence:")
    add_bullet("1. Clone Repository", "git clone https://github.com/wadekarhrushikesh06/JD_cust_hrushi.git && cd JD_cust_hrushi")
    add_bullet("2. Install Dependencies", "pip install -r requirements.txt")
    add_bullet("3. Run Interactive Setup", "python scripts/setup_new_user.py (prompts for candidate name, contact, employer, and title)")
    add_bullet("4. Deploy to Streamlit Cloud", "Push to personal GitHub repository, open share.streamlit.io, click 'Create app', and select app.py.")

    os.makedirs(os.path.dirname(out_docx), exist_ok=True)
    doc.save(out_docx)
    print(f"Generated DOCX: {out_docx}")

if __name__ == "__main__":
    out_docx = os.path.join(REPO_ROOT, "Resume_Tailor_Architecture_and_Deployment_Guide.docx")
    out_pdf = os.path.join(REPO_ROOT, "Resume_Tailor_Architecture_and_Deployment_Guide.pdf")
    desktop_pdf = r"C:\Users\admin\OneDrive\Desktop\Resume_Tailor_Architecture_and_Deployment_Guide.pdf"
    
    build_documentation_docx(out_docx)
    convert_to_pdf(out_docx, out_pdf)
    
    import shutil
    shutil.copyfile(out_pdf, desktop_pdf)
    print(f"Generated Desktop PDF: {desktop_pdf}")
