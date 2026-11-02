import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_client = None
if os.getenv("GROQ_API_KEY"):
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Cricket Stats", page_icon="🏏", layout="wide")

st.title("🏏 Cricket Stats Dashboard")

batting_data = {
    "Player": ["Virat Kohli", "Rohit Sharma", "Steve Smith", "Joe Root", "Kane Williamson",
               "Babar Azam", "David Warner", "Quinton de Kock", "Shakib Al Hasan", "Jos Buttler"],
    "Country": ["India", "India", "Australia", "England", "New Zealand",
                "Pakistan", "Australia", "South Africa", "Bangladesh", "England"],
    "Matches": [292, 262, 150, 170, 160, 120, 160, 140, 240, 180],
    "Runs": [13848, 10709, 9685, 12000, 8750, 6000, 6900, 6800, 7500, 5500],
    "Average": [58.67, 49.1, 55.4, 50.1, 47.3, 56.7, 45.2, 44.1, 36.5, 38.9],
    "StrikeRate": [93.2, 89.5, 53.5, 57.2, 82.1, 88.5, 95.0, 95.5, 81.0, 118.0],
    "Centuries": [50, 31, 32, 30, 27, 19, 20, 17, 14, 11],
    "Fifties": [72, 55, 31, 58, 33, 34, 33, 39, 51, 26],
}

bowling_data = {
    "Player": ["Jasprit Bumrah", "Pat Cummins", "Rashid Khan", "Trent Boult", "Ravichandran Ashwin",
               "Shaheen Afridi", "Kagiso Rabada", "Mitchell Starc", "Adil Rashid", "Mustafizur Rahman"],
    "Country": ["India", "Australia", "Afghanistan", "New Zealand", "India",
                "Pakistan", "South Africa", "Australia", "England", "Bangladesh"],
    "Matches": [89, 100, 150, 120, 100, 60, 90, 110, 120, 80],
    "Wickets": [159, 200, 350, 180, 250, 120, 180, 210, 160, 110],
    "Average": [20.8, 23.5, 21.2, 25.1, 25.3, 24.1, 22.8, 26.0, 28.5, 27.2],
    "Economy": [4.6, 5.1, 6.2, 5.0, 5.4, 5.3, 5.5, 5.4, 5.8, 5.6],
    "Best": ["6/19", "5/28", "7/18", "6/33", "7/59", "6/35", "6/16", "6/28", "5/27", "6/43"],
}

batting_df = pd.DataFrame(batting_data)
bowling_df = pd.DataFrame(bowling_data)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Batting", "Bowling", "Leaderboard", "Compare", "AI Assistant"])

with tab1:
    st.subheader("Batting Stats")
    country = st.selectbox("Filter by Country", ["All"] + sorted(batting_df["Country"].unique().tolist()))
    df = batting_df if country == "All" else batting_df[batting_df["Country"] == country]
    st.dataframe(df, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df, x="Player", y="Runs", color="Country", title="Runs by Player")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(df, x="Average", y="StrikeRate", text="Player", color="Country",
                         title="Average vs Strike Rate", size="Centuries")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Bowling Stats")
    country = st.selectbox("Filter by Country", ["All"] + sorted(bowling_df["Country"].unique().tolist()), key="b")
    df = bowling_df if country == "All" else bowling_df[bowling_df["Country"] == country]
    st.dataframe(df, use_container_width=True)
    fig = px.bar(df, x="Player", y="Wickets", color="Country", title="Wickets by Player")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Leaderboard")
    metric = st.selectbox("Rank by", ["Runs", "Average", "StrikeRate", "Centuries", "Wickets", "Economy"])
    if metric in batting_df.columns:
        lb = batting_df.sort_values(metric, ascending=False).reset_index(drop=True)
        lb.index += 1
        st.dataframe(lb, use_container_width=True)
        fig = px.bar(lb.head(10), x="Player", y=metric, color="Country", title=f"Top 10 by {metric}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        lb = bowling_df.sort_values(metric, ascending=(metric == "Economy")).reset_index(drop=True)
        lb.index += 1
        st.dataframe(lb, use_container_width=True)
        fig = px.bar(lb.head(10), x="Player", y=metric, color="Country", title=f"Top 10 by {metric}")
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Compare Players")
    players = st.multiselect("Select players", batting_df["Player"].tolist(), default=batting_df["Player"].tolist()[:2])
    if players:
        cmp_df = batting_df[batting_df["Player"].isin(players)]
        st.dataframe(cmp_df, use_container_width=True)
        fig = px.bar(cmp_df, x="Player", y=["Runs", "Centuries", "Fifties"], barmode="group", title="Comparison")
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("AI Assistant (Groq)")
    if not groq_client:
        st.warning("Set GROQ_API_KEY in a .env file to enable.")
    else:
        q = st.text_input("Ask about cricket stats")
        if q:
            context = f"Batting data:\n{batting_df.to_string(index=False)}\n\nBowling data:\n{bowling_df.to_string(index=False)}"
            resp = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a cricket stats assistant. Use the provided data."},
                    {"role": "user", "content": f"{context}\n\nQuestion: {q}"},
                ],
            )
            st.write(resp.choices[0].message.content)

st.sidebar.header("Player Lookup")
selected = st.sidebar.selectbox("Select Player", batting_df["Player"].tolist())
st.sidebar.dataframe(batting_df[batting_df["Player"] == selected].T)
