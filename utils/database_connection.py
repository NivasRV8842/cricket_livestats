import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="N########2",
        database="cricket_db"
    )
    return connection


# Test connection
if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ Database Connected Successfully!")
        conn.close()
    except Exception as e:
        print("❌ Error:", e)
