---
name: resume-tailor
description: >-
  Triggered when the user types "tailor", "jd", "hrushi", or pastes a Job Description to tailor Hrushikesh Wadekar's resume.
---

# Resume Tailoring Workflow

Whenever the user provides a Job Description with the trigger word `tailor`:
1. Target workspace: `C:\Users\admin\OneDrive\Desktop\JD_cust_hrushi`
2. Follow `PROMPT_PACKET.md` Phase 2 workflow strictly against `source_of_truth/`.
3. Route between `data_engineer` and `oracle_dba` tracks.
4. Render `resume.docx` and ATS-compliant `resume.pdf` (strictly 1 page).
5. Run anti-hallucination validation via `scripts/validate_resume.py`.
6. Generate `report.md` with fit score and gap analysis.
7. Generate dedicated `roadmap.md` in the job folder with company-specific 7-day preparation roadmap and interview questions.
8. Update `tracker.csv` and `jobs/_INDEX.md`.
