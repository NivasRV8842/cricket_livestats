from database_connection import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM matches"
    cursor.execute(query)

    results = cursor.fetchall()

    print("📊 Matches Table Data:")
    for row in results:
        print(row)

except Exception as e:
    print("❌ Error:", e)

finally:
    cursor.close()
    conn.close()
