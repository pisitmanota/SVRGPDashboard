
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sivarom GP Dashboard", layout="wide")

st.sidebar.image("https://i.imgur.com/HQ3JU8E.png", width=250)

st.title("📊 รายละเอียดพร้อมเสนอราคา")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Rename columns for consistency
    df = df.rename(columns={
        "โครงการ": "Project Name",
        "เลขห้อง": "Room No."
    })

    project_list = ["ALL PROJECTS"] + sorted(df["Project Name"].dropna().unique().tolist())
    selected_project = st.sidebar.selectbox("เลือกโครงการ", project_list)

    selected_df = df.copy()
    if selected_project != "ALL PROJECTS":
        selected_df = df[df["Project Name"] == selected_project]

    if not selected_df.empty:
        room_list = selected_df["Room No."].dropna().astype(str).unique().tolist()
        selected_room = st.sidebar.selectbox("🔍 เลือกยูนิต (Room No.) ที่ต้องการวิเคราะห์", room_list)

        st.subheader("📊 รายละเอียดพร้อมเสนอราคา")
        st.dataframe(selected_df[selected_df["Room No."].astype(str) == selected_room])
    else:
        st.info("กรุณาเลือกยูนิตเพื่อแสดงข้อมูล")
else:
    st.info("กรุณาอัปโหลดไฟล์ Excel เพื่อตรวจสอบข้อมูล")
