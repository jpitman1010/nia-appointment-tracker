import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables from .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

PG_SUPERUSER = os.getenv("PG_SUPERUSER", "postgres")
PG_SUPERUSER_PASSWORD = os.getenv("PG_SUPERUSER_PASSWORD", "")

def create_database():
    try:
        # Connect as superuser
        conn = psycopg2.connect(
            dbname='postgres', 
            user=PG_SUPERUSER, 
            password=PG_SUPERUSER_PASSWORD, 
            host=DB_HOST
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Create user if not exists
        cur.execute(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT FROM pg_catalog.pg_roles WHERE rolname = '{DB_USER}'
                ) THEN
                    CREATE ROLE {DB_USER} LOGIN PASSWORD '{DB_PASSWORD}';
                END IF;
            END
            $$;
        """)

        # Create database if not exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
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