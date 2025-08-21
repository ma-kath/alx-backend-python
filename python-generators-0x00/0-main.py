import os
import pandas as pd

seed = __import__('seed')

connection = seed.connect_db()

if connection: 
    # seed.create_database(connection)
    # connection.close()
    # print(f"Connection successfully.")
    
    connection = seed.connect_to_prodev()
    if connection:
        seed.create_table(connection)
        print(f"Table created successfully.")
        # Loading data 
        if os.path.exists('user_data.csv'):
            data = pd.read_csv('user_data.csv')
            if not data.empty:
                seed.insert_data(connection, data)
                print(f"Data inserted successfully.")
            else:
                print(f"CSV file is empty.")
        else:
            print("user_data.csv file not found.")

        
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result: 
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()