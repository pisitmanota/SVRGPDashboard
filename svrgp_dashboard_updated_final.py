
import streamlit as st
import pandas as pd

# ตั้งค่าหน้า
st.set_page_config(page_title="SVR PROJECT GP DASHBOARD", layout="wide")

# โหลดข้อมูล
@st.cache_data
def load_data():
    df = pd.read_excel("Corporate_Project_Template.xlsx", sheet_name="ALL PROJECTS")
    return df

df = load_data()

# Sidebar
st.sidebar.image("logo.png", width=250)
st.sidebar.subheader("เลือกโครงการ")
project_list = ["ALL PROJECTS"] + sorted(df["Project Name"].dropna().unique())
selected_project = st.sidebar.selectbox("เลือกโครงการ", project_list)

if selected_project != "ALL PROJECTS":
    df = df[df["Project Name"] == selected_project]

# เลือกยูนิต
room_options = sorted(df["เลขห้อง"].dropna().astype(str).unique())
selected_room = st.sidebar.selectbox("🔍 เลือกยูนิต (Room No.) ที่ต้องการวิเคราะห์", [""] + room_options)

check_agent = st.sidebar.checkbox("ตรวจสอบราคาสำหรับ agent")

# แสดงรายละเอียด
st.header("📊 รายละเอียดพร้อมเสนอราคา")

if selected_room:
    unit = df[df["เลขห้อง"].astype(str) == selected_room]
    if not unit.empty:
        asking_price = unit["asking price"].values[0]
        bottom_price = unit["bottom price"].values[0]
        cost = unit["ต้นทุนรวม"].values[0]
        area = unit["พื้นที่(ตร.ว.)"].values[0]
        common_fee = unit["ค่าส่วนกลาง"].values[0]

        # ราคาเสนอ default = bottom price
        default_offer = bottom_price

        # ถ้าเลือก agent คำนวณราคาพิเศษ
        if check_agent:
            agent_fee = asking_price * 0.27
            maintenance_2yr = area * common_fee * 24
            offer_price = asking_price - (agent_fee + maintenance_2yr)
        else:
            offer_price = default_offer

        # คำนวณ GP รายแปลง และ GP committed รายแปลง
        gp_unit = round(((offer_price - cost) / offer_price) * 100, 2)
        gp_committed_unit = round(((bottom_price - cost) / bottom_price) * 100, 2)

        gp_committed_project = unit["GP COMMITTED (%)"].values[0]
        gp_diff = round(gp_unit - gp_committed_project, 2)

        st.markdown(f"### ยูนิต: {selected_room}")
        st.markdown(f"**Asking Price:** {asking_price:,.2f} บาท")
        st.markdown(f"**Bottom Price:** {bottom_price:,.2f} บาท")
        st.markdown(f"**ราคาที่เสนอ:** {offer_price:,.2f} บาท")
        st.markdown(f"**GP (รายแปลง):** {gp_unit:.2f}%")
        st.markdown(f"✨ **GP (Committed แปลงนี้):** {gp_committed_unit:.2f}%")
        st.markdown(f"🎯 **GP (Committed โครงการ):** {gp_committed_project:.2f}%")
        gp_diff_color = "green" if gp_diff >= 0 else "red"
        st.markdown(f"**ผลต่าง GP:** <span style='color:{gp_diff_color}'>{gp_diff:+.2f}%</span>", unsafe_allow_html=True)
    else:
        st.info("ไม่พบข้อมูลยูนิตที่เลือก")
else:
    st.info("กรุณาเลือกยูนิตเพื่อแสดงข้อมูล")
