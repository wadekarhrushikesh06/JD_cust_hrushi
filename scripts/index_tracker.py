"""
Helper script to update tracker.csv and regenerate jobs/_INDEX.md.
Maintains two views: Grouped by Category and Grouped by Company.
"""

import os
import sys
import csv
import argparse
from collections import defaultdict

TRACKER_FILE = "tracker.csv"
INDEX_FILE = os.path.join("jobs", "_INDEX.md")

COLUMNS = [
    "date", "company", "role", "category", "tags",
    "resume_type", "fit_pct", "status", "folder_path", "job_link", "notes"
]

def load_tracker():
    if not os.path.exists(TRACKER_FILE):
        return []
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_tracker(rows):
    with open(TRACKER_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def rebuild_index():
    rows = load_tracker()
    os.makedirs("jobs", exist_ok=True)
    
    # 1. Group by category
    by_category = defaultdict(list)
    for r in rows:
        cat = r.get("category", "other")
        by_category[cat].append(r)

    # 2. Group by company
    by_company = defaultdict(list)
    for r in rows:
        comp = r.get("company", "Unknown")
        by_company[comp].append(r)

    lines = [
        "# Jobs Master Index",
        "",
        "*Auto-maintained master list of tailored resume packages and job applications.*",
        "",
        "## Summary",
        f"- **Total Applications Prepared:** {len(rows)}",
        f"- **Categories Active:** {len(by_category)}",
        "",
        "---",
        "",
        "## By Category",
        ""
    ]

    if not rows:
        lines.append("*No jobs logged yet.*")
        lines.append("")
    else:
        for cat in sorted(by_category.keys()):
            lines.append(f"### `{cat}`")
            lines.append("| Date | Company | Role | Fit % | Status | Resume Type | Folder | Link |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
            for item in sorted(by_category[cat], key=lambda x: x.get("date", ""), reverse=True):
                folder = item.get("folder_path", "").replace("\\", "/")
                folder_link = f"[{os.path.basename(folder)}](file:///{folder})" if folder else "—"
                jlink = f"[JD Link]({item['job_link']})" if item.get("job_link") and item["job_link"] != "—" else "—"
                lines.append(f"| {item.get('date', '')} | **{item.get('company', '')}** | {item.get('role', '')} | {item.get('fit_pct', '')}% | `{item.get('status', 'prepared')}` | {item.get('resume_type', '')} | {folder_link} | {jlink} |")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## By Company")
    lines.append("")

    if not rows:
        lines.append("*No jobs logged yet.*")
        lines.append("")
    else:
        lines.append("| Company | Role | Category | Date | Fit % | Status | Tags | Folder |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for comp in sorted(by_company.keys(), key=lambda s: s.lower()):
            for item in sorted(by_company[comp], key=lambda x: x.get("date", ""), reverse=True):
                folder = item.get("folder_path", "").replace("\\", "/")
                folder_link = f"[{os.path.basename(folder)}](file:///{folder})" if folder else "—"
                lines.append(f"| **{item.get('company', '')}** | {item.get('role', '')} | `{item.get('category', '')}` | {item.get('date', '')} | {item.get('fit_pct', '')}% | `{item.get('status', 'prepared')}` | {item.get('tags', '')} | {folder_link} |")
        lines.append("")

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Updated {INDEX_FILE}")

def add_entry(date, company, role, category, tags, resume_type, fit_pct, status, folder_path, job_link="—", notes=""):
    rows = load_tracker()
    
    # Check if duplicate exists (same company and role)
    for r in rows:
        if r["company"].strip().lower() == company.strip().lower() and r["role"].strip().lower() == role.strip().lower():
            # update existing or note duplicate
            pass

    new_row = {
        "date": date,
        "company": company,
        "role": role,
        "category": category,
        "tags": tags,
        "resume_type": resume_type,
        "fit_pct": str(fit_pct),
        "status": status,
        "folder_path": folder_path,
        "job_link": job_link,
        "notes": notes
    }
    rows.append(new_row)
    save_tracker(rows)
    print(f"Added entry for {company} - {role} to {TRACKER_FILE}")
    rebuild_index()

def delete_entry(company, role):
    rows = load_tracker()
    filtered = [r for r in rows if not (r["company"].strip().lower() == company.strip().lower() and r["role"].strip().lower() == role.strip().lower())]
    save_tracker(filtered)
    rebuild_index()
    print(f"Deleted entry for {company} - {role}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage tracker.csv and jobs/_INDEX.md")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild jobs/_INDEX.md from tracker.csv")
    parser.add_argument("--add", action="store_true", help="Add job entry")
    parser.add_argument("--delete", action="store_true", help="Delete job entry")
    parser.add_argument("--date", default="")
    parser.add_argument("--company", default="")
    parser.add_argument("--role", default="")
    parser.add_argument("--category", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--resume_type", default="")
    parser.add_argument("--fit_pct", default="")
    parser.add_argument("--status", default="prepared")
    parser.add_argument("--folder_path", default="")
    parser.add_argument("--job_link", default="—")
    parser.add_argument("--notes", default="")

    args = parser.parse_args()

    if args.add:
        add_entry(args.date, args.company, args.role, args.category, args.tags,
                  args.resume_type, args.fit_pct, args.status, args.folder_path,
                  args.job_link, args.notes)
    elif args.delete:
        delete_entry(args.company, args.role)
    elif args.rebuild:
        rebuild_index()
    else:
        parser.print_help()
