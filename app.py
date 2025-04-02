import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# ตั้งค่า Dashboard
st.set_page_config(page_title="SVR PROJECT GP DASHBOARD", layout="wide")

# โหลดโลโก้
logo = Image.open("logo.png")

# Header layout
title_col, logo_col = st.columns([5, 1])
with title_col:
    st.title("📊 SVR PROJECT GP DASHBOARD")
with logo_col:
    st.image(logo, width=130)

# โหลดข้อมูล
df = pd.read_excel("Corporate_Project_Template.xlsx")

# Filter: เลือกโครงการ
projects = df["โครงการ"].unique()
selected_project = st.selectbox("เลือกโครงการ", projects)

# Filter: ตัวกรองซ้อน เลือกเฉพาะยูนิตในโครงการที่เลือก
project_df = df[df["โครงการ"] == selected_project].copy()
available_rooms = project_df["เลขห้อง"].astype(str).tolist()

# Filter: เลือกยูนิต
selected_rooms = st.multiselect("🔎 เลือกยูนิต (Room No.) ที่ต้องการวิเคราะห์", available_rooms)

# ตัวเลือก Agent Mode
use_agent_pricing = st.checkbox("ตรวจสอบราคาสำหรับ agent")

# เฉพาะยูนิตที่เลือก
unit_df = project_df[project_df["เลขห้อง"].astype(str).isin(selected_rooms)]

if selected_rooms:
    st.subheader("📋 ข้อมูลยูนิตที่เลือก")
    st.dataframe(unit_df, use_container_width=True)
    
    # เพิ่มตัวอย่างการแสดงผลกราฟถ้าต้องการ
    if "ราคาขายสุทธิ" in unit_df.columns:
        st.subheader("💹 กราฟราคาขายสุทธิ")
        fig, ax = plt.subplots()
        ax.bar(unit_df["เลขห้อง"].astype(str), unit_df["ราคาขายสุทธิ"])
        ax.set_ylabel("ราคาขายสุทธิ")
        ax.set_xlabel("ยูนิต")
        st.pyplot(fig)
else:
    st.info("กรุณาเลือกยูนิตเพื่อดูรายละเอียด")