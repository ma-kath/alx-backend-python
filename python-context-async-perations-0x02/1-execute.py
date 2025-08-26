import sqlite3

class ExcuteQuery:
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = sqlite3.connect('user_data.db')
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            
    def execute(self):
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()
        
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExcuteQuery(query, params) as executor:
        results = executor.execute()
        for row in results:
            print(row)