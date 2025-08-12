import sqlite3
import pandas as pd
import uuid
import os

# Connect to SQLite database
def connect_db():
    try:
        conn = sqlite3.connect('ALX_prodev.db')
        return conn
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return None

# Create user_data INE
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON user_data (user_id)")
    conn.commit()
    cursor.close()

# Insert data into the user_data table
def insert_data(conn, data):
    cursor = conn.cursor()
    for index, row in data.iterrows():
        user_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (?, ?, ?, ?)
        """,
        (user_id, row['name'], row['email'], row['age'])
        )
        conn.commit()
        cursor.close()