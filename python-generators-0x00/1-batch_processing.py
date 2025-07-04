import mysql.connector

def stream_users_in_batches(batch_size):
    """Yields batches of users from the DB, one batch at a time."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql_password",  
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch  # yield final smaller batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Processes and prints users over age 25 from each batch."""
    for batch in stream_users_in_batches(batch_size):  
        for user in batch:                             
            if int(user["age"]) > 25:                  
                yield user                             

