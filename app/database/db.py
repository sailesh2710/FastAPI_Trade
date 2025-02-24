import os
import psycopg2
from dotenv import load_dotenv

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables.")

# Function to establish a new database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise e  # Rethrow to prevent silent failures

# Test connection at startup
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    print("Database connected successfully!")
except Exception as e:
    print(f"Database connection failed at startup: {e}")
