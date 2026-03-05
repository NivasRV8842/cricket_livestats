import requests
from database_connection import get_connection

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

headers = {
    "X-RapidAPI-Key": "7e7d9423###################################b3a0960",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data = response.json()

conn = get_connection()
cursor = conn.cursor()

for type_match in data.get("typeMatches", []):
    for series in type_match.get("seriesMatches", []):
        if "seriesAdWrapper" in series:
            matches = series["seriesAdWrapper"]["matches"]

            for match in matches:
                info = match["matchInfo"]

                match_id = str(info["matchId"])
                team1 = info["team1"]["teamName"]
                team2 = info["team2"]["teamName"]
                status = info["status"]
                venue = info["venueInfo"]["ground"]

                insert_query = """
                INSERT IGNORE INTO matches
                (match_id, team1, team2, match_date, venue, status)
                VALUES (%s, %s, %s, CURDATE(), %s, %s)
                """

                cursor.execute(insert_query, (match_id, team1, team2, venue, status))

conn.commit()

cursor.close()
conn.close()

print("✅ Matches inserted into database successfully!")
import requests
from database_connection import get_connection

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

headers = {
    "X-RapidAPI-Key": "7e7d942397mshff10e4be84d2253p1bf3f2jsn54346b3a0960",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data = response.json()

conn = get_connection()
cursor = conn.cursor()

for type_match in data.get("typeMatches", []):
    for series in type_match.get("seriesMatches", []):
        if "seriesAdWrapper" in series:
            matches = series["seriesAdWrapper"]["matches"]

            for match in matches:
                info = match["matchInfo"]

                match_id = str(info["matchId"])
                team1 = info["team1"]["teamName"]
                team2 = info["team2"]["teamName"]
                status = info["status"]
                venue = info["venueInfo"]["ground"]

                insert_query = """
                INSERT IGNORE INTO matches
                (match_id, team1, team2, match_date, venue, status)
                VALUES (%s, %s, %s, CURDATE(), %s, %s)
                """

                cursor.execute(insert_query, (match_id, team1, team2, venue, status))

conn.commit()

cursor.close()
conn.close()

print("✅ Matches inserted into database successfully!")
