import requests
from database_connection import get_connection

# --- API Config ---
url = "https://cricbuzz-cricket.p.rapidapi.com/matches"
headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

# --- Fetch Data ---
response = requests.get(url, headers=headers)
data = response.json()

conn = get_connection()
cursor = conn.cursor()

# --- Parse & Insert ---
for group in data.get("typeMatches", []):
    for match in group.get("seriesMatches", []):
        for info in match.get("matches", []):
            match_id = str(info.get("matchId", "NA"))
            t1 = info.get("team1", {}).get("teamName", "Unknown")
            t2 = info.get("team2", {}).get("teamName", "Unknown")
            status = info.get("status", "NA")
            venue = info.get("venue", {}).get("ground", "Unknown")

            insert_query = """
            INSERT IGNORE INTO matches 
            (match_id, team1, team2, match_date, venue, status)
            VALUES (%s, %s, %s, CURDATE(), %s, %s)
            """
            values = (match_id, t1, t2, venue, status)

            cursor.execute(insert_query, values)

conn.commit()
cursor.close()
conn.close()

print("✅ Matches saved to database!")
