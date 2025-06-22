import psycopg2
from psycopg2 import sql
import os
import time

def create_table():
    conn = None
    for _ in range(5):
        try:
            conn = psycopg2.connect(
                dbname=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                host="postgres",
                port="5432"
            )
            break
        except psycopg2.OperationalError:
            time.sleep(1)

    if conn is None:
        print("Could not connect to the database.")
        return

    cur = conn.cursor()

    cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS resumes (
            id SERIAL PRIMARY KEY,
            filename TEXT,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT[],
            experience_years FLOAT,
            last_job_title TEXT,
            uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """))

    conn.commit()
    cur.close()
    conn.close()
    print("Table 'resumes' created successfully or already exists.")

if __name__ == "__main__":
    create_table()