import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warehouses (
            id SERIAL PRIMARY KEY,
            warehouse_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            coefficient FLOAT NOT NULL
        );
    """)
    cursor.execute("""
        ALTER TABLE warehouses
        ADD CONSTRAINT unique_warehouse_id UNIQUE (warehouse_id);
    """)
    conn.commit()
    conn.close()

