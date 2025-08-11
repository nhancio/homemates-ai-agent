import psycopg2

def store_feedback(user_input):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",       
            user="postgres",        
            password="Fiitjee@mmar1410",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO feedback (user_input)
            VALUES (%s)
            """,
            (user_input,)
        )

        conn.commit()

        cursor.close()
        conn.close()

        print(" Feedback stored successfully!")

    except Exception as e:
        print(" Error storing feedback:", e)


store_feedback("This chatbot is awesome, but could be faster.")
