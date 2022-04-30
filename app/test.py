import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(
        host='localhost',
        database='fast-api',
        user='postgres',
        password='',
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print('Database connection failed')
    print(error)
