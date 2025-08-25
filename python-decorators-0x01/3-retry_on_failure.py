import time
import sqlite3 
import functools

#### paste your with_db_decorator here

def with_db_connection(func): 
    @functools.wraps(func) 
    def wrapper(*args, **kwargs): 
        conn = sqlite3.connect('users.db') 
        try: 
            result = func(conn, *args, **kwargs) 
        finally: 
            conn.close() 
        return result 
    return wrapper

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kargs)
                except Exception as e:
                    if attempt == retries - 1:
                        print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries} attempts failed.")
                        raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
        
#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)