from decimal import Decimal

seed = __import__('seed')

def stream_user_ages():
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        if 'age' in row and isinstance(row['age'], Decimal):
            yield int(row['age'])
    cursor.close()
    conn.close()
    
def avg_age():
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    return total_age / count

if __name__ == "__main__":
    average_age = avg_age()
    print(f"Average age of users: {average_age:.2f}")  