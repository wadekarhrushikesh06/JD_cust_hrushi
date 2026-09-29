# Tailoring & Fit Report: PySpark Data Engineer at Infosys

- **Company:** Infosys
- **Role:** PySpark Data Engineer
- **Experience Required:** 2 - 5 years
- **Location:** Pune, Hyderabad, Bengaluru (Hybrid)
- **Date Processed:** 2026-09-29
- **Selected Track:** `data_engineer`
- **Category:** `technical-data-engineering`
- **Estimated Fit Percentage:** **95% (Strong Match)**

---

## 1. Fit Analysis & Requirements Matrix

| JD Requirement | Candidate SOT Status | Fit Analysis |
| :--- | :---: | :--- |
| **2–5 years Data Engineering experience** | ✅ **Match** | 2+ years of production experience at TCS (State Bank of India client project). |
| **Strong PySpark & Apache Spark skills** | ✅ **Match** | Core daily stack: high-throughput batch ETL, broadcast joins, repartitioning, shuffle tuning, and resolving OOM exceptions. |
| **Python programming & ETL solutions** | ✅ **Match** | Python batch ingestion, semi-structured JSON parsing, REST API extractors, and transformation scripts. |
| **SQL & Spark SQL for processing** | ✅ **Match** | Complex analytical queries, CTEs, Window functions, PL/SQL, and query plan optimization. |
| **Performance Tuning & Troubleshooting** | ✅ **Match** | Eliminated Spark OOM bottlenecks cutting downtime by 30%; slashed query runtimes by 20%. |
| **Data Quality & Reliability** | ✅ **Match** | Pre/post-load financial ledger reconciliation in PySpark/SQL with 99.8% SLA adherence. |
| **Exposure to Databricks (Preferred)** | 🌟 **Exceeds** | **Databricks Certified Data Engineer Associate** credential verified in SOT. |
| **Exposure to Microsoft Fabric (Bonus)** | 🌟 **Exceeds** | **Microsoft Certified: Fabric Data Engineer Associate** credential verified in SOT. |
| **Hadoop / Hive (Preferred)** | ⚠️ **Gap** | Direct Spark/Hive catalog interactions understood; native Hadoop/HDFS cluster administration is logged as a gap (not on resume). |
| **Unstructured Data Processing** | ⚠️ **Gap** | SOT focuses on high-throughput structured and semi-structured JSON banking datasets; NLP/unstructured text pipelines not present. |

---

## 2. Summary of Resume Changes

* **Professional Summary**: Tailored to lead with Databricks, Fabric, and AWS credentials, highlighting 2+ years processing 4.45M+ daily transaction records using PySpark, Spark SQL, and Airflow for SBI banking workflows.
* **Certifications Section**: Showcases all 4 verified credentials:
  1. Databricks Certified Data Engineer Associate
  2. Microsoft Certified: Fabric Data Engineer Associate
  3. AWS Certified Solutions Architect – Associate
  4. Snowflake SnowPro Core Certification
* **Experience Bullets**:
  * **Bullet #1**: Spark Performance Tuning & RCA (eliminating OOM exceptions, data skew, broadcast joins, 30% downtime reduction).
  * **Bullet #2**: Scalable Batch ETL Ingestion (4.45M+ transaction hits, 12-hour settlement cycles).
  * **Bullet #3**: Airflow Orchestration & SLA Adherence (20+ DAGs, 99.8% SLA).
  * **Bullet #4**: Financial Ledger Reconciliation (25% data accuracy improvement for audit compliance).
  * **Bullet #5**: Database & Query Optimization (slashing batch runtimes by 20%).
* **Skills Ordering**: Prioritized `Big Data & Processing` (Apache Spark, PySpark, Spark SQL), followed by `Languages & Scripting`, `Cloud & Warehouses`, and `Workflow Orchestration`.

---

## 3. Curated Preparation Material (Per Permanent Workspace Rule)

### Core PySpark & Apache Spark Topics
1. **Spark Architecture & Execution Model**:
   * *Core Concepts*: Driver, Cluster Manager (YARN/K8s/Standalone), Worker Nodes, Executors, Tasks, CPU Cores/Slots.
   * *Execution Flow*: User Code $\rightarrow$ Catalyst Logical Plan $\rightarrow$ Physical Plan $\rightarrow$ DAG of Stages (split across wide dependencies/shuffles) $\rightarrow$ Tasks assigned to executor slots.
   * *Reference*: [Apache Spark Cluster Overview](https://spark.apache.org/docs/latest/cluster-overview.html)
2. **Shuffle Tuning & Skew Mitigation**:
   * *Core Concepts*: Shuffle Read/Write, `spark.sql.shuffle.partitions` (default 200, tuning formula: target 100–200 MB per partition).
   * *Data Skew Strategies*: Salting join keys with random integer prefixes; Broadcast Hash Join (`broadcast(df)`) when smaller table $< 10$ MB (or tuned `spark.sql.autoBroadcastJoinThreshold`).
   * *Interview Story*: Be ready to detail your State Bank of India experience mitigating skew during peak 12-hour settlement batches.
3. **Memory Management & OOM Debugging**:
   * *Core Concepts*: Unified Memory Manager (Execution Memory for shuffles/joins, Storage Memory for caching/broadcasts).
   * *Failure Patterns*:
     * `OutOfMemoryError: Java heap space` (Executor OOM): skewed partitions, large broadcast, insufficient executor memory.
     * Driver OOM: Calling `.collect()` or `.toPandas()` on large distributed DataFrames.
4. **Spark SQL Optimization**:
   * *Core Concepts*: Catalyst Optimizer (Analysis, Logical Optimization, Physical Planning, Code Generation). Predicate pushdown, projection pruning, and constant folding.

---

## 4. 7-Day Interview Preparation Roadmap

```mermaid
flowchart LR
    P1["Days 1-2: Spark Internals & Execution"] --> P2["Days 3-4: Performance Tuning & OOM Scenarios"]
    P2 --> P3["Days 5-6: Advanced SQL & Airflow Pipelines"]
    P3 --> P4["Day 7: Infosys Mock Interview & Storytelling"]
```

* **Days 1–2: Spark Fundamentals & Internals**
  * Review DataFrame transformations vs. actions; Narrow vs. Wide dependencies.
  * Practice writing PySpark DataFrame API transformations without using Python loops (`udf` avoidance, native built-in functions in `pyspark.sql.functions`).
* **Days 3–4: Troubleshooting, OOM & Real-World Scenarios**
  * Walk through the Spark UI: Jobs, Stages, Tasks, Event Timeline, Executors Tab, and GC pauses.
  * Rehearse answering: *"How did you diagnose and resolve Out-Of-Memory exceptions at TCS for the State Bank of India project?"*
* **Days 5–6: SQL, Databricks & Workflow Orchestration**
  * Practice advanced SQL: Window functions (`ROW_NUMBER`, `DENSE_RANK`, `LEAD`, `LAG`), CTEs, and cumulative sums.
  * Review Airflow: DAG design, idempotency, retry mechanisms, and SLAs.
  * Review Databricks Delta Lake: ACID logs, Time Travel, and Medallion architecture.
* **Day 7: Behavioral & Final Mock QA**
  * Practice the STAR method (Situation, Task, Action, Result) for all resume bullet metrics (4.45M+ records, 30% downtime reduction, 99.8% SLA).

---

## 5. Quality Checklist & Verification

- [x] Every skill, number, company, and date matches `source_of_truth/`
- [x] Verified zero invented tools or unbacked numbers
- [x] Output strictly formatted to **1 page** ATS-compliant PDF
- [x] Missing requirements (Hadoop/Hive cluster ops) kept in report, not injected into resume
- [x] Generated DOCX and PDF both present in folder
- [x] Master tracker updated
