# Job Taxonomy & Categorization Rules

This taxonomy defines the primary job categories for filing job applications and tailored resumes.

## Primary Categories

1. **`technical-data-engineering`**
   - **Scope:** Roles focusing on ETL/ELT pipelines, data warehousing, big data processing (Spark/PySpark), workflow orchestration (Airflow), data modeling (Kimball star schema), cloud data platforms (Snowflake, Databricks, AWS).
   - **Default Resume Template:** `data_engineer`

2. **`technical-dba-database`**
   - **Scope:** Database administration, high availability, clustering (Oracle RAC, Grid Infrastructure), replication (Oracle GoldenGate), backup and recovery (RMAN), disaster recovery (Data Guard), performance tuning (AWR/ASH/ADDM), storage (ASM).
   - **Default Resume Template:** `oracle_dba`

3. **`development`**
   - **Scope:** Software engineering, backend development, API engineering, Python development, SQL development, data application engineering.
   - **Default Resume Template:** `data_engineer` (or adapted based on stack)

4. **`product`**
   - **Scope:** Technical product management, data product management, technical business analysis with heavy data focus.
   - **Default Resume Template:** Determined per JD requirements

5. **`management`**
   - **Scope:** Engineering management, data team lead, project management, technical lead roles.
   - **Default Resume Template:** Determined per JD requirements

6. **`support-operations`**
   - **Scope:** Production support, L2/L3 application/database support, site reliability, IT operations, 24x7 infrastructure monitoring.
   - **Default Resume Template:** `oracle_dba` (or `data_engineer` if data platform support)

7. **`other`**
   - **Scope:** Roles that do not cleanly align with the above technical categories.

---

## Categorization & Routing Rules

1. **Primary Category Rule:**
   - Every job must be assigned to exactly **one** primary category based on the core day-to-day technical function, not the company or industry.
2. **Category Creation Rule:**
   - Create a new category only when 3 or more JDs do not fit existing categories.
   - Any new category must be documented in this file with rationales before use. Existing folders must never be renamed or moved without explicit user consent.
3. **Template Routing:**
   - If the role focuses on Data Engineering, PySpark, Airflow, Snowflake, AWS, or Big Data, route to `data_engineer`.
   - If the role focuses on Oracle DBA, RAC, GoldenGate, RMAN, Data Guard, or Database Administration, route to `oracle_dba`.
   - For hybrid roles (e.g. Database / Data Engineer), select the closer template based on primary weight of responsibilities and justify in `report.md`.
4. **Folder Naming Convention:**
   - `jobs/<category>/<YYYY-MM-DD>_<company>_<role>/`
   - Lowercase, hyphens instead of spaces, no special characters.
   - If an identical company and role already exists, create `v2` within the same folder or note variant.
