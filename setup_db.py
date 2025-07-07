import os
from dotenv import load_dotenv
import psycopg
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine, text
from urllib.parse import urlparse, urlunparse
from alembic.config import CommandLine
from alembic import command
from alembic.config import Config

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
PG_SUPERUSER = os.getenv("PG_SUPERUSER", "admin")  # or "postgres" depending on your setup
PG_SUPERUSER_PASSWORD = os.getenv("PG_SUPERUSER_PASSWORD", "admin1234!")

# Full app database URL
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Build superuser connection URL, connecting to "postgres" DB (which always exists)
def get_superuser_url():
    # Parse the app URL and replace database name with 'postgres'
    parsed = urlparse(DATABASE_URL)
    new_parsed = parsed._replace(
        path=f"/postgres",
        netloc=f"{PG_SUPERUSER}:{PG_SUPERUSER_PASSWORD}@{DB_HOST}:{DB_PORT}"
    )
    return urlunparse(new_parsed)


def create_database():
    try:
        # Connect as superuser to 'postgres' database
        with psycopg.connect(
            dbname="postgres",
            user=PG_SUPERUSER,
            password=PG_SUPERUSER_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            autocommit=True
        ) as conn:
            with conn.cursor() as cur:
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
    except Exception as e:
        print(f"Error creating database or user: {e}")


def run_migrations():
    alembic_cfg = Config("alembic.ini")  # or your path to alembic.ini
    command.upgrade(alembic_cfg, "head")


def create_admin_user():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Check if admin user exists
            result = conn.execute(text("SELECT id FROM staff WHERE email = :email"), {"email": "admin@example.com"})
            exists = result.first()
            if exists:
                print("Admin user already exists.")
                return
            
            # Hash password
            hashed_pw = generate_password_hash("admin1234!")

            # Insert admin user - adjust columns as per your schema
            conn.execute(text("""
                INSERT INTO staff (email, password, fname, lname)
                VALUES (:email, :password, :fname, :lname)
            """), {
                "email": "admin@example.com",
                "password": hashed_pw,
                "fname": "admin",
                "lname": "user",
            })
            print("Admin user created successfully.")
    except Exception as e:
        print(f"Error creating admin user: {e}")



if __name__ == "__main__":
    create_database()
    run_migrations()    # <-- create all tables
    create_admin_user()
