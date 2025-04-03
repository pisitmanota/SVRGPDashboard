
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# โหลดไฟล์ Excel โดยอัตโนมัติ
@st.cache_data
def load_data():
    return pd.read_excel("Corporate_Project_Template.xlsx", sheet_name="ALL PROJECTS")

df = load_data()

# ส่วนหัว
st.image("logo.png", width=250)
st.markdown("## 📊 รายละเอียดพร้อมเสนอราคา")

# เลือกโครงการ
project_list = ["ALL PROJECTS"] + sorted(df["โครงการ"].dropna().unique())
selected_project = st.selectbox("เลือกโครงการ", project_list)

# กรองข้อมูลตามโครงการ
if selected_project != "ALL PROJECTS":
    df = df[df["โครงการ"] == selected_project]

# เลือกยูนิต
unit_list = sorted(df["เลขห้อง"].dropna().unique())
selected_unit = st.selectbox("เลือกยูนิต", unit_list)

# แสดงข้อมูลของยูนิตที่เลือก
unit = df[df["เลขห้อง"] == selected_unit].iloc[0]

st.markdown(f"### 📄 รายละเอียดราคาสำหรับยูนิต {selected_unit}")
st.write(unit)
