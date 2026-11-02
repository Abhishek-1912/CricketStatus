import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None

st.set_page_config(page_title="Cricket Stats", page_icon="🏏", layout="wide")
st.title("🏏 Cricket Stats Dashboard")

uploaded = st.file_uploader("Upload CSV file", type="csv")
if uploaded is None:
    st.info("Please upload a CSV file to view stats.")
    st.stop()

df = pd.read_csv(uploaded)
st.subheader("Data")
st.dataframe(df, use_container_width=True)

st.subheader("Stats Summary")
st.write(df.describe(include="all"))

numeric = df.select_dtypes(include="number").columns.tolist()
if numeric:
    col = st.selectbox("Chart column", numeric)
    fig = px.bar(df, y=col, title=f"{col} distribution")
    st.plotly_chart(fig, use_container_width=True)

with st.popover("🤖 AI", help="Chat with cricket stats AI"):
    if not groq_client:
        st.warning("Set GROQ_API_KEY in .env")
    else:
        if "chat" not in st.session_state:
            st.session_state.chat = []
        for m in st.session_state.chat:
            with st.chat_message(m["role"]):
                st.write(m["content"])
        q = st.chat_input("Ask about this data")
        if q:
            st.session_state.chat.append({"role": "user", "content": q})
            with st.chat_message("user"):
                st.write(q)
            context = df.to_string(index=False)
            msgs = [{"role": "system", "content": "You are a cricket stats assistant. Use the provided data."}] + st.session_state.chat
            msgs[0]["content"] += "\n\n" + context
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full = ""
                stream = groq_client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, stream=True)
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    full += delta
                    placeholder.write(full)
            st.session_state.chat.append({"role": "assistant", "content": full})
