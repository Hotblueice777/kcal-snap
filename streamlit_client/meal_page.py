import streamlit as st
import pandas as pd
from datetime import datetime

def render():
    st.title("🍽️ My Meal — Daily Summary")

    # --- 模拟数据（你之后可改为读取 CSV / DB）---
    meals = [
        {"time": "08:20", "name": "Toast + Egg", "cal": 250, "protein": 10, "fat": 8, "carb": 35},
        {"time": "13:10", "name": "Sushi", "cal": 252, "protein": 12.6, "fat": 7.2, "carb": 39.6},
    ]
    df = pd.DataFrame(meals)

    st.subheader("📆 Today's Meals")
    st.dataframe(df, use_container_width=True)

    total = df[["cal","protein","fat","carb"]].sum()
    st.markdown("### 🔢 Daily Totals")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calories (kcal)", f"{total['cal']:.0f}")
    c2.metric("Protein (g)", f"{total['protein']:.1f}")
    c3.metric("Fat (g)", f"{total['fat']:.1f}")
    c4.metric("Carbs (g)", f"{total['carb']:.1f}")

    st.markdown("---")

    # --- Voice Assistant Section ---
    st.subheader("🗣️ AI Health Assistant")

    user_input = st.text_input("Ask your question:", key="assistant_input")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("🎤 Speak"):
            st.info("Speech-to-Text API will be called here (Azure Speech)")
    with col2:
        if st.button("▶️ Reply by Voice"):
            st.info("Text-to-Speech API will be called here (Azure Speech)")

    if st.button("💬 Ask Assistant"):
        st.info("Here will call Azure Language QnA endpoint")

    st.caption("Connected to Azure Speech & Language APIs — integration pending.")
    st.markdown("---")
    st.button("⬅️ Back to Scan Page", on_click=lambda: switch_page("📷 Scan & Analyze"))


def switch_page(page_name):
    st.session_state["page"] = page_name
    st.rerun()