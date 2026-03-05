import streamlit as st
import pandas as pd
from database_connection import get_connection
import requests
import plotly.express as px

st.title("🏏 Cricket Analytics Dashboard")

st.subheader("⚡ Fetch Live Matches from Cricbuzz API")

if st.button("Fetch Latest Matches", key="fetch_matches"):

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "X-RapidAPI-Key": "7e7d942397############################0960",
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

                    cursor.execute(insert_query,
                                   (match_id, team1, team2, venue, status))

    st.success("✅ Live matches updated!")

conn = get_connection()
cursor = conn.cursor()

# -----------------------------
# SECTION 1: Show Matches
# -----------------------------
st.subheader("📊 Matches Data")

matches_query = "SELECT * FROM matches"
matches_df = pd.read_sql(matches_query, conn)
st.dataframe(matches_df)

# -----------------------------
# SECTION 2: Add Player Form
# -----------------------------
st.subheader("➕ Add New Player")

player_id = st.text_input("Player ID")
player_name = st.text_input("Player Name")
team = st.text_input("Team")
role = st.text_input("Role")

if st.button("Add Player", key="add_player"):
    insert_query = """
    INSERT INTO players (player_id, player_name, team, role)
    VALUES (%s, %s, %s, %s)
    """
    values = (player_id, player_name, team, role)

    cursor.execute(insert_query, values)
    conn.commit()

    st.success("✅ Player Added Successfully!")

# -----------------------------
# SECTION 3: Show Players
# -----------------------------
st.subheader("👥 Players Data")

players_query = "SELECT * FROM players"
players_df = pd.read_sql(players_query, conn)
st.dataframe(players_df)

# -----------------------------
# SECTION 4: Delete Player
# -----------------------------
st.subheader("🗑 Delete Player")

delete_player_id = st.text_input("Enter Player ID to Delete")

if st.button("Delete Player", key="delete_player"):
    delete_query = "DELETE FROM players WHERE player_id = %s"
    cursor.execute(delete_query, (delete_player_id,))
    conn.commit()
    st.success("✅ Player Deleted Successfully!")

# -----------------------------
# SECTION 5: Update Player
# -----------------------------
st.subheader("✏ Update Player")

update_player_id = st.text_input("Player ID to Update")
new_team = st.text_input("New Team")
new_role = st.text_input("New Role")

if st.button("Update Player", key="update_player"):
    update_query = """
    UPDATE players
    SET team = %s, role = %s
    WHERE player_id = %s
    """
    cursor.execute(update_query, (new_team, new_role, update_player_id))
    conn.commit()
    st.success("✅ Player Updated Successfully!")

st.subheader("⚡ Update Live Matches")

# -----------------------------
# SECTION 6: Analytics Dashboard
# -----------------------------
st.subheader("📊 Cricket Analytics Dashboard")

# Load matches data
matches_df = pd.read_sql("SELECT * FROM matches", conn)

# ---------------------------------
# Chart 1: Matches by Team
# ---------------------------------

team_matches = pd.concat([
    matches_df["team1"],
    matches_df["team2"]
]).value_counts().reset_index()

team_matches.columns = ["Team", "Matches"]

fig1 = px.bar(
    team_matches,
    x="Team",
    y="Matches",
    title="Matches Played by Team"
)

st.plotly_chart(fig1)

# ---------------------------------
# Chart 2: Matches by Venue
# ---------------------------------

venue_matches = matches_df["venue"].value_counts().reset_index()
venue_matches.columns = ["Venue", "Matches"]

fig2 = px.bar(
    venue_matches,
    x="Venue",
    y="Matches",
    title="Matches by Venue"
)

st.plotly_chart(fig2)

# ---------------------------------
# Chart 3: Match Status Distribution
# ---------------------------------

status_counts = matches_df["status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

fig3 = px.pie(
    status_counts,
    names="Status",
    values="Count",
    title="Match Status Distribution"
)

st.plotly_chart(fig3)


conn.commit()
conn.close()
