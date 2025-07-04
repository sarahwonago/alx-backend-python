import seed 

def stream_user_ages():
    """Generator that yields user ages one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    
    for (age,) in cursor:
        yield float(age)

    cursor.close()
    connection.close()


def compute_average_age():
    """Computes average age without loading all ages into memory."""
    total = 0
    count = 0
    for age in stream_user_ages():  # 1 loop here
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

