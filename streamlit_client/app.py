# app.py

import streamlit as st
import scan_page, meal_page, assistant_page

st.set_page_config(page_title="KcalSnap", layout="centered")

st.markdown("""
        <style>
        /* 全局修改 Streamlit 提示框样式 */
        div.stAlert {
            background-color: #F7F5FA !important;  /* 柔和灰紫底 */
            border: 1px solid #E0DAEB !important;  /* 微边框 */
            color: #6E5B8B !important;             /* 暗紫灰文字 */
            border-radius: 10px !important;
            padding: 12px 16px !important;
        }

        /* success / info / warning / error 的图标也统一紫灰色 */
        div.stAlert [data-testid="stMarkdownContainer"] p,
        div.stAlert svg {
            color: #6E5B8B !important;
            fill: #6E5B8B !important;
        }
        </style>
        """, unsafe_allow_html=True)

# 侧边栏导航
page = st.sidebar.radio("KcalSnap", ["Scan & Analyze", "My Meal", "AI Assistant"])

st.markdown("""
        <style>
        /* --- 💜 Sidebar modern purple style --- */

        /* 整体sidebar背景 */
        section[data-testid="stSidebar"] {
            background-color: #F9F9F9 !important;
            padding-top: 50px !important;
        }

        /* 隐藏圆点 */
        div[data-testid="stSidebar"] [data-baseweb="radio"] svg {
            display: none !important;
        }

        /* 每个选项块基础样式 */
        div[data-testid="stSidebar"] label[data-baseweb="radio"] {
            padding: 8px 14px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease-in-out;
        }

        /* hover 状态：淡紫色背景 */
        div[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
            background-color: rgba(155, 93, 229, 0.08) !important;
        }

        /* 选中项：紫色背景更深一点 */
        div[data-testid="stSidebar"] label[data-baseweb="radio"][aria-checked="true"] {
            background-color: rgba(155, 93, 229, 0.20) !important;
        }

        /* 选中文字：加深加粗 */
        div[data-testid="stSidebar"] label[data-baseweb="radio"][aria-checked="true"] p {
            color: #5A2D9D !important;
            font-weight: 600 !important;
        }
        </style>
        """, unsafe_allow_html=True)

# 页面切换
if page == "Scan & Analyze":
    scan_page.render()
elif page == "My Meal":
    meal_page.render()
elif page == "AI Assistant":
    assistant_page.render()
