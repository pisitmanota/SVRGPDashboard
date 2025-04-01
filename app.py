
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="SVR GP Dashboard", layout="wide")

# --- LOGO ---
col1, col2 = st.columns([6, 1])
with col1:
    st.title("🏗️ SVR PROJECT GP DASHBOARD")
with col2:
    logo = Image.open("Artboard 1 copy 4 (4).png")
    st.image(logo, width=100)

# --- UPLOAD ---
uploaded_file = st.file_uploader("📂 กรุณาอัปโหลด Corporate_Project_Template.xlsx", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ โหลดข้อมูลเรียบร้อยแล้ว")
    st.dataframe(df, use_container_width=True)

    # สรุป GP รวมจากราคานำเสนอ (Project Value)
    if "Project Value" in df.columns and "ต้นทุนรวม" in df.columns:
        try:
            df_valid = df.dropna(subset=["Project Value", "ต้นทุนรวม"])
            total_gp = (df_valid["Project Value"].sum() - df_valid["ต้นทุนรวม"].sum()) / df_valid["Project Value"].sum()
            st.metric("📊 GP จากราคานำเสนอรวม", f"{total_gp * 100:.2f}%")
        except:
            st.warning("ไม่สามารถคำนวณ GP ได้ กรุณาตรวจสอบข้อมูล")
