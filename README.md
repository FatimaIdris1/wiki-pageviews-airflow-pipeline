# **Wikipedia Pageviews ETL Pipeline with Apache Airflow**

This project demonstrates an end-to-end ETL workflow orchestrated with **Apache Airflow**.
It downloads Wikipedia pageviews data for the specified date and time, extracts page-level metrics for defined technology companies, loads the results into a PostgreSQL database, and performs an analysis.

---

## **Project Architecture**

This workflow consists of the following stages:

1. **Download data** from Wikipedia’s public pageviews dump
2. **Extract and filter** pageviews for target company keywords:

   * Google
   * Amazon
   * Facebook
   * Apple
   * Microsoft
3. **Load** the extracted data into PostgreSQL
4. **Analyze** pageviews to determine the **Top 5 most-viewed pages**
5. **Notify** success or failure via Email
---

## **Project Directory Structure**
```bash
project/
├─ dags/
├─ pageviews_etl_dag.py
│   ├─ utilities/
│   │   ├─ keyword_config.py
│   │   └─ format_html.py
├─ scripts/
│   ├─ download_data.py
│   ├─ extract_data.py
│   └─ load_data.py
└─ README.md
```

---

## **Key Features**

### Dynamic Keyword Extraction

Keywords (Google, Amazon, etc.) are stored in `keyword_config.py` to ensure flexibility.

### Resilient Failure Handling

A `check_failure` task monitors previous task states.
If retries are exhausted, an **EmailOperator** sends a failure notification.

### Success Email Notification

On completion, a final task sends the final Top 5 ranking to the recipient.

### PostgreSQL Integration

A table is created (if missing) and data is loaded via SQLAlchemy.

---

## **Tech Stack**

| Component  | Usage         |
| ---------- | ------------- |
| Airflow    | Orchestration |
| Python     | ETL logic     |
| PostgreSQL | Storage       |
| SQLAlchemy | Database ORM  |
| Requests   | Data download |
| Pandas     | Processing    |

---

## **How It Works**

### **1. Download Wikipedia Data**

The `download_data` task retrieves a compressed pageviews dump for a **specific date** from:

```
https://dumps.wikimedia.org/other/pageviews/YYYY/YYYY-MM/
```

(*Replace date dynamically in the .env file*)

> Insert code snippet:

```python
load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR"))
TIMESTAMP = os.getenv("TIMESTAMP")

```
---

### **2. Extract Relevant Pageviews**

This task filters rows based on the keywords defined in your `keyword_config.py`.

> See code within the extract_companies.py

---

### **3. Create a table and Load into PostgreSQL**

A table is created if it does not exist:
```sql
DROP TABLE IF EXISTS pageviews;
            CREATE TABLE pageviews (
                project TEXT,
                page_title TEXT,
                count_views INT,
                total_response_size INT
            );
```

The records are then inserted via psycopg2:
> See code within the load_data.py

---

### **4. Perform Analysis**

A simple aggregation determines the **Top 5 most-viewed pages** for the day.

```sql
SELECT *
            FROM pageviews
            ORDER BY count_views DESC
            LIMIT 5;
```

---

### **5. Email Notifications (Success/Failure)**

* `send_failure` triggers when retries are exhausted
* `send_success` fires after analysis completes

Provide HTML output formatting from `format_html.py`.


##  **Email Output Example**

```
Subject: Pageviews DAG Completed Successfully

Top 5 Pages:
1. Google – 580,000 views
2. Amazon – 420,000 views
...
```

---

## **DAG Flow Visualization**

```
download_data
      ↓
extract_data
      ↓
load_data
      ↓
analyze_data
      ↓
send_success
```

<img width="1019" height="273" alt="oie_HnoYyiYIwfjM" src="https://github.com/user-attachments/assets/23872cb1-99e5-4f65-871d-cc546d617452" />

If failure occurs at any point:

```
Any Task → check_failure → send_failure
```

---

## **Prerequisites**

* Python 3.10+
* Docker & Docker Compose
* Airflow 2.7+
* PostgreSQL
* Email SMTP configuration

---

## **Run Instructions**

```bash
docker compose up -d
```

Then open Airflow:

```
http://localhost:8080
```
---

## **Logs & Monitoring**

Navigate to Airflow UI → Graph → Logs
Each task logs:

* Download start/end
* Filter counts
* Insert counts
* Analysis results
* Email status

---

## **Example Output Table**

Project | Page Title | Views | Response Size
--------|------------|-------|---------------
en      | Google     | 580000| 0
en      | Apple      | 410000| 0


---

## **Future Improvements**

To improve this pipeline any of the following steps can be taken:

* Integrate Great Expectations for data quality
* Push processed data to AWS S3 or GCS
* Add visualizations using Looker/Power BI
* Parameterize date via Airflow UI
* Automate table schema evolution
  
---
