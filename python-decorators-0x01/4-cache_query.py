import time
import sqlite3
import functools

query_cache = {}

# with_db_connection decorator
def with_db_connection(func):
    """Decorator that opens and closes the database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# cache_query decorator
def cache_query(func):
    """Decorator that caches query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get the SQL query from kwargs or args
        query = kwargs.get('query')
        if query is None and len(args) > 1:
            query = args[1]

        # Return cached result if available
        if query in query_cache:
            return query_cache[query]

        # Execute the function and cache the result
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

