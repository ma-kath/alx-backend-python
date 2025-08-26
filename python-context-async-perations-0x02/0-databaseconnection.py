import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            
with DatabaseConnection('user_data.db') as conn:
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30))
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Fred', 41))
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Mireille', 65))
    conn.commit()
    
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print(users)