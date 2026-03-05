from database_connection import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    insert_player = """
    INSERT INTO players (player_id, player_name, team, role)
    VALUES (%s, %s, %s, %s)
    """

    values = ("P001", "Virat Kohli", "India", "Batsman")

    cursor.execute(insert_player, values)
    conn.commit()

    print("✅ Player inserted successfully!")

except Exception as e:
    print("❌ Error:", e)

finally:
    cursor.close()
    conn.close()
