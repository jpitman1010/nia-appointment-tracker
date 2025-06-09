import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_NAME = "nia_appointment_tracker"
DB_USER = "admin"
DB_PASSWORD = "admin1234!"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_database():
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='', host=DB_HOST)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Create user
        cur.execute(f"DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{DB_USER}') THEN CREATE ROLE {DB_USER} LOGIN PASSWORD '{DB_PASSWORD}'; END IF; END $$;")

        # Create database
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER};")
            print(f"Database {DB_NAME} created.")
        else:
            print(f"Database {DB_NAME} already exists.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database or user: {e}")

if __name__ == "__main__":
    create_database()
