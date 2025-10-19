# app.py

import streamlit as st
import scan_page, meal_page

st.set_page_config(page_title="KcalSnap", layout="centered")

# 侧边栏导航
page = st.sidebar.radio("Go to", ["📷 Scan & Analyze", "🍽️ My Meal"])

# 页面切换
if page == "📷 Scan & Analyze":
    scan_page.render()
elif page == "🍽️ My Meal":
    meal_page.render()
