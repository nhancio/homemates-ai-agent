import psycopg2

DB_NAME = "real_estate_db"
DB_USER = "postgres"
DB_PASSWORD = "Fiitjee@mmar1410"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print(" Connected to PostgreSQL")

    cur = conn.cursor()

    # Test query
    cur.execute("SELECT * FROM real_estate_data LIMIT 5;")
    rows = cur.fetchall()

    print("\n Sample Data:")
    for row in rows:
        print(row)

    # Close connections
    cur.close()
    conn.close()

except Exception as e:
    print(f" Error: {e}")
