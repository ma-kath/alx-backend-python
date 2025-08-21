from decimal import Decimal

seed = __import__('seed')

def stream_users_in_batches(batch_size):
    conn = seed.connect_to_prodev()
    if conn: 
        print(f"Connected to the database successfully.")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
            
            # Convert age from Decimal to int for all users in the batch
        for user in batch:
            if 'age' in user and isinstance(user['age'], Decimal):
                user['age'] = int(user['age'])
            
        yield batch

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size): 
        
        filtered_users = [user for user in batch if user['age'] > 25]
        
        for user in filtered_users:  
            yield user 
            print(user)
