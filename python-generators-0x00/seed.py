import mysql.connector
import csv
import uuid

# 1. Connect to MySQL Server (no database yet)
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password"  
            )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 2. Create the ALX_prodev database
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

# 3. Connect to ALX_prodev database
def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password",
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 4. Create the user_data table
def create_table(connection):
    cursor = connection.cursor()
    create_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    );
    """
    cursor.execute(create_query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

# 5. Insert data from CSV (if not already in)
def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = row['age']
            cursor.execute(
                "SELECT * FROM user_data WHERE name=%s AND email=%s AND age=%s",
                (name, email, age)
            )
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
    connection.commit()
    cursor.close()

def stream_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()

