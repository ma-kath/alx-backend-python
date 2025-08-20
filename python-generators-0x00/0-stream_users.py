seed = __import__('seed')

def stream_users():
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)  
    try:
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
    finally:
        cursor.close()
        conn.close() 