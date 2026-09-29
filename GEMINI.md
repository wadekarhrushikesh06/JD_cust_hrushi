# Resume Tailoring & Job Application Rules

This workspace operates according to `PROMPT_PACKET.md` and the deterministic Source of Truth in `source_of_truth/`.

## Persistent Rule: JD & Skills Analysis + Preparation Material & Roadmap
Whenever reviewing or tailoring for a new Job Description (JD):
1. **Source of Truth Integrity**: Follow `PROMPT_PACKET.md` strictly (no invented facts, metrics, or tools in the resume).
2. **Skill Gap Analysis**: Any skills or tools required by the JD that are not in the Source of Truth must be highlighted as gaps in `report.md`, never added to the resume.
3. **Curated Preparation Material**: For all missing skills and key core requirements in the JD, provide targeted preparation materials (official documentation, essential concepts, and practical exercises).
4. **Structured Preparation Roadmap**: Provide a step-by-step roadmap (timeline, milestones, and focus areas) so the candidate can prepare for the interview and bridge identified gaps.
5. **Dedicated Standalone `roadmap.md`**: Always generate a dedicated `roadmap.md` file directly inside the job's company/role folder (`jobs/<category>/<job_folder>/roadmap.md`) containing the company-tailored technical roadmap, day-by-day study schedule, curated resources, and interview question bank.

## Quick Trigger Keyword
When the user types **`tailor`** (or **`hrushi`** or **`jd`**):
- Immediately execute the Phase 2 workflow in `C:\Users\admin\OneDrive\Desktop\JD_cust_hrushi`.
- Process the pasted Job Description directly.
- Output the tailored 1-page resume (DOCX + PDF), validation status, report.md, and dedicated roadmap.md in the job folder.
