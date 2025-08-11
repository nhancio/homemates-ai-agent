import psycopg2
import pandas as pd

DB_HOST = "localhost"
DB_NAME = "real_estate_db"
DB_USER = "postgres"
DB_PASSWORD = "Fiitjee@mmar1410"  

CSV_FILE_PATH = r"C:\Users\Dell\Downloads\House_Rent_Dataset.csv"
TABLE_NAME = "real_estate_data"

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL")

    df = pd.read_csv(CSV_FILE_PATH)
    print(f"📄 Loaded {len(df)} rows from CSV")

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            posted_on DATE,
            bhk INTEGER,
            rent INTEGER,
            size INTEGER,
            floor VARCHAR(255),
            area_type VARCHAR(255),
            area_locality VARCHAR(255),
            city VARCHAR(255),
            furnishing_status VARCHAR(255),
            tenant_preferred VARCHAR(255),
            bathroom INTEGER,
            point_of_contact VARCHAR(255)
        );
    """)
    print(f"🛠️ Table '{TABLE_NAME}' is ready.")

    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT INTO {TABLE_NAME} (
                posted_on, bhk, rent, size, floor, area_type, area_locality,
                city, furnishing_status, tenant_preferred, bathroom, point_of_contact
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            row['Posted On'], row['BHK'], row['Rent'], row['Size'], row['Floor'],
            row['Area Type'], row['Area Locality'], row['City'], row['Furnishing Status'],
            row['Tenant Preferred'], row['Bathroom'], row['Point of Contact']
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(" Data inserted successfully into PostgreSQL!")

except Exception as e:
    print(" Error:", e)

