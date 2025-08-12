import mysql.connector
import pandas as pd
import uuid
import os

# Connect to MYSQL db server
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='makath',
            password='up99d@sh'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create db ALX_prodev INE
def create_database(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()
    
# Connect to the ALX_prodev database
def connect_to_prodev():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='makath',
            password='up99d@sh',
            database='ALX_prodev'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create user_data INE
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL,
            INDEX (user_id)
        )
    """)
    cursor.close()

# Insert data into the user_data table
def insert_data(conn, data):
    cursor = conn.cursor()
    for index, row in data.iterrows():
        user_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
        """, 
        (user_id, row['name'], row['email'], row['age']))
        conn.commit()
        cursor.close()