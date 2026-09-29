"""
Interactive & Automated Setup Script for New Candidate Replication.
Configures profile, skills, and clears sample job folders for a new user.
"""

import os
import sys
import yaml
import shutil
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOT_DIR = os.path.join(REPO_ROOT, "source_of_truth")

def prompt(msg, default=""):
    val = input(f"{msg} [{default}]: ").strip()
    return val if val else default

def setup_candidate():
    print("=" * 65)
    print("   🚀 RESUME TAILOR - NEW CANDIDATE CONFIGURATION WIZARD")
    print("=" * 65)
    print("This wizard configures your Source of Truth for automatic")
    print("ATS-tailored resumes, 1-page PDF rendering, and 24/7 mobile cloud deployment.\n")

    # 1. Profile Information
    name = prompt("1. Full Name", "Jane Doe")
    email = prompt("2. Email Address", "janedoe@example.com")
    phone = prompt("3. Phone Number", "+91 9876543210")
    location = prompt("4. Current Location (City, State, Country)", "Mumbai, Maharashtra, India")
    linkedin = prompt("5. LinkedIn profile handle/URL", "linkedin.com/in/janedoe")

    # 2. Employment
    company = prompt("6. Current / Most Recent Company", "Tata Consultancy Services")
    designation = prompt("7. Official Designation", "Assistant System Engineer")
    functional_title = prompt("8. Functional Resume Title (e.g. Data Engineer)", "Data Engineer")
    client = prompt("9. Client / Project Name (optional)", "State Bank of India")
    domain = prompt("10. Industry / Domain (e.g. BFSI, E-commerce, Healthcare)", "BFSI / Banking")

    profile_data = {
        "name": name.upper(),
        "contact": {
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "location_de": location,
            "location_dba": location,
            "linkedin_de": linkedin,
            "linkedin_dba": linkedin
        },
        "employers": [
            {
                "company": company,
                "official_designation": designation,
                "titles": {
                    "de": functional_title,
                    "dba": "Database Administrator"
                },
                "client": client,
                "project_de": f"{client} Data Platform" if client else "Enterprise Data Platform",
                "project_dba": f"{client} Database Operations" if client else "Database Operations",
                "location": location.split(",")[0].strip() + ", India"
            }
        ],
        "domain": domain
    }

    with open(os.path.join(SOT_DIR, "profile.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(profile_data, f, sort_keys=False)

    print("\n✅ Saved: source_of_truth/profile.yaml")

    # 3. Clean tracker for new user
    clean_tracker = prompt("Reset application tracker for new user? (y/n)", "y").lower() == "y"
    if clean_tracker:
        tracker_file = os.path.join(REPO_ROOT, "tracker.csv")
        with open(tracker_file, "w", encoding="utf-8") as f:
            f.write("date,company,role,category,tags,resume_type,fit_pct,status,folder_path,job_link,notes\n")
        
        index_file = os.path.join(REPO_ROOT, "jobs", "_INDEX.md")
        with open(index_file, "w", encoding="utf-8") as f:
            f.write("# Job Applications Index\n\nNo applications logged yet.\n")
        print("✅ Reset tracker.csv and jobs/_INDEX.md")

    print("\n" + "=" * 65)
    print("🎉 SETUP COMPLETE!")
    print("Next steps:")
    print("1. Review/edit your skills in: source_of_truth/skills.yaml")
    print("2. Review/edit your certs in:  source_of_truth/certs_projects.yaml")
    print("3. Test pipeline:              python scripts/test_pipeline.py")
    print("4. Push to your GitHub:        git push origin main")
    print("5. Deploy on Streamlit Cloud:  https://share.streamlit.io")
    print("=" * 65)

if __name__ == "__main__":
    setup_candidate()
