seed = __import__('seed')

def stream_users_in_batches(batch_size):
    conn = seed.connect_to_prodev()
    if conn: 
        print(f"Connected to the database successfully.")
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield from batch
    finally:
        cursor.close()
        conn.close()
   
    
def batch_processing(batch_size):
    """Process users in batches and filter by age."""
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 25]
        for user in filtered_users:
            yield user