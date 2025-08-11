

import psycopg2
from get_llm_response import get_llm_response

DB_HOST = "localhost"
DB_NAME = "real_estate_db"
DB_USER = "postgres"
DB_PASSWORD = "Fiitjee@mmar1410"

def get_connection():
    """Open a fresh PostgreSQL connection."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def generate_sql_query(user_input):
    """Ask the LLM to generate a SQL query from a natural language prompt."""
    prompt = f"""
You are an expert in SQL.
You are given a natural language question and you need to write a SQL query for PostgreSQL.
The table is named real_estate_data and has columns:
id, posted_on, bhk, rent, size, floor, area_type, area_locality, city,
furnishing_status, tenant_preferred, bathroom, point_of_contact.


User Question:
"{user_input}"

Write only the SQL query without explanation.
"""
    sql_query = get_llm_response(prompt).strip()
    return sql_query

def execute_query(sql_query):
    """Run a SQL query and return results."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()
        return results
    finally:
        conn.close()

def get_property_data(user_input):
    """Main function to convert user input → SQL → execute → results."""
    sql_query = generate_sql_query(user_input)
    print("Generated SQL:", sql_query)
    results = execute_query(sql_query)
    return results

if __name__ == "__main__":
    user_input = input("Ask a property question: ")
    data = get_property_data(user_input)
    print("Results:", data)


