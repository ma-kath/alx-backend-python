import mysql.connector

# Database configuration
config = {
    'user': 'root',
    'password': 'm1ss@m0',
    'host': 'localhost',
    'database': 'ALX_prodev'
}

def stream_users():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)  
    try:
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
    finally:
        cursor.close()
        conn.close() 