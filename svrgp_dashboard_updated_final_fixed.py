
import streamlit as st
import pandas as pd

st.set_page_config(page_title="SVR GP Dashboard", layout="wide")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="ALL PROJECTS")

    project_list = ["ALL PROJECTS"] + sorted(df["โครงการ"].dropna().unique())
    selected_project = st.sidebar.selectbox("เลือกโครงการ", project_list)

    if selected_project != "ALL PROJECTS":
        df = df[df["โครงการ"] == selected_project]

    st.title("📊 รายละเอียดพร้อมเสนอราคา")
    st.dataframe(df)
else:
    st.title("📊 รายละเอียดพร้อมเสนอราคา")
    st.info("กรุณาอัปโหลดไฟล์ Excel เพื่อตรวจสอบข้อมูล")
