import psycopg2

def load_pageviews():
    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    with open('/opt/airflow/dags/Data/filtered_pageviews.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(' ')
            if len(parts) == 4:
                cur.execute(
                    "INSERT INTO pageviews (project, page_title, count_views, total_response_size) VALUES (%s, %s, %s, %s)",
                    (parts[0], parts[1], int(parts[2]), int(parts[3]))
                )

    conn.commit()
    cur.close()
    conn.close()
