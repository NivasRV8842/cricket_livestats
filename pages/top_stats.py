import requests

headers = {
    "X-RapidAPI-Key": "7e7d9423###################################b3a0960",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

# ---------------------------------
# Function to fetch rankings
# ---------------------------------

def fetch_rankings(url, title):
    response = requests.get(url, headers=headers)

    print(f"\n{title}")
    print("-" * 40)

    if response.status_code == 200:
        data = response.json()

        for player in data.get("rank", [])[:10]:
            name = player.get("name")
            country = player.get("country")
            rating = player.get("rating")

            print(f"{name} ({country}) - Rating: {rating}")

    else:
        print("API Error:", response.status_code)
        print(response.text)


# ---------------------------------
# Top Batting Rankings
# ---------------------------------

batting_url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen?formatType=odi"

fetch_rankings(batting_url, "🏏 Top ODI Batting Rankings")


# ---------------------------------
# Top Bowling Rankings
# ---------------------------------

bowling_url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/bowlers?formatType=odi"

fetch_rankings(bowling_url, "🎯 Top ODI Bowling Rankings")
