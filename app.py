import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cricket Stats", page_icon="🏏", layout="wide")

st.title("🏏 Cricket Stats Dashboard")

# Sample data
batting_data = {
    "Player": ["Virat Kohli", "Rohit Sharma", "Steve Smith", "Joe Root", "Kane Williamson"],
    "Matches": [292, 262, 150, 170, 160],
    "Runs": [13848, 10709, 9685, 12000, 8750],
    "Average": [58.67, 49.1, 55.4, 50.1, 47.3],
    "StrikeRate": [93.2, 89.5, 53.5, 57.2, 82.1],
    "Centuries": [50, 31, 32, 30, 27],
}

bowling_data = {
    "Player": ["Jasprit Bumrah", "Pat Cummins", "Rashid Khan", "Trent Boult", "Ravichandran Ashwin"],
    "Matches": [89, 100, 150, 120, 100],
    "Wickets": [159, 200, 350, 180, 250],
    "Average": [20.8, 23.5, 21.2, 25.1, 25.3],
    "Economy": [4.6, 5.1, 6.2, 5.0, 5.4],
    "Best": ["6/19", "5/28", "7/18", "6/33", "7/59"],
}

batting_df = pd.DataFrame(batting_data)
bowling_df = pd.DataFrame(bowling_data)

tab1, tab2 = st.tabs(["Batting", "Bowling"])

with tab1:
    st.subheader("Batting Stats")
    st.dataframe(batting_df, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(batting_df, x="Player", y="Runs", title="Runs by Player")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(batting_df, x="Average", y="StrikeRate", text="Player",
                         title="Average vs Strike Rate", size="Centuries")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Bowling Stats")
    st.dataframe(bowling_df, use_container_width=True)
    fig = px.bar(bowling_df, x="Player", y="Wickets", title="Wickets by Player")
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.header("Filters")
selected_player = st.sidebar.selectbox("Select Player", batting_df["Player"].tolist())
st.sidebar.write(batting_df[batting_df["Player"] == selected_player].T)
