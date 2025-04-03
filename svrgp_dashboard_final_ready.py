
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
        "โครงการ": "โครงการ",
        "เลขห้อง": "เลขห้อง"
    })

    project_list = ["ALL PROJECTS"] + sorted(df["โครงการ"].dropna().unique().tolist())
    selected_project = st.sidebar.selectbox("เลือกโครงการ", project_list)

    selected_df = df.copy()
    if selected_project != "ALL PROJECTS":
        selected_df = df[df["โครงการ"] == selected_project]

    if not selected_df.empty:
        room_list = selected_df["เลขห้อง"].dropna().astype(str).unique().tolist()
        selected_room = st.sidebar.selectbox("🔍 เลือกยูนิต (เลขห้อง) ที่ต้องการวิเคราะห์", room_list)

        st.subheader("📊 รายละเอียดพร้อมเสนอราคา")
        selected_unit = selected_df[selected_df["เลขห้อง"].astype(str) == selected_room]
        st.dataframe(selected_unit)

        # คำนวณราคาสำหรับ Agent
        if not selected_unit.empty:
            asking = selected_unit["Asking Price"].values[0]
            area = selected_unit["พื้นที่ ตร.ว."].values[0]
            fee = selected_unit["ค่าส่วนกลาง"].values[0]
            agent_price = asking - ((asking * 0.27) + (area * 24 * fee))
            st.success(f"💰 ราคาสำหรับ Agent: {agent_price:,.2f} บาท")
    else:
        st.info("กรุณาเลือกยูนิตเพื่อแสดงข้อมูล")
else:
    st.info("กรุณาอัปโหลดไฟล์ Excel เพื่อตรวจสอบข้อมูล")
