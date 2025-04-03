import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="SVR PROJECT GP DASHBOARD", layout="wide")
logo = Image.open("logo.png")

title_col, logo_col = st.columns([5, 1])
with title_col:
    st.title("📊 SVR PROJECT GP DASHBOARD")
with logo_col:
    st.image(logo, width=130)

gp_committed_map = {
    "GRAND SVR": 30.60,
    "SVR VILLAGE 58": 29.39,
    "SVR PARK 76": 28.40,
    "SVR VILLAGE SAI-NOI": 26.73,
    "SVR NP-ASSUMPTION": 25.36,
    "SVR HYDE BK": 32.00,
    "SVR HYDE S3": 27.07
}

df_raw = pd.read_excel("Corporate_Project_Template.xlsx")
df_raw.columns = df_raw.columns.str.strip().str.lower()

projects = df_raw["โครงการ"].unique()
selected_project = st.selectbox("เลือกโครงการ", projects)
gp_committed = gp_committed_map.get(selected_project, 27.00)

project_df = df_raw[df_raw["โครงการ"] == selected_project].copy()
available_rooms = project_df["เลขห้อง"].astype(str).tolist()
selected_rooms = st.multiselect("🔎 เลือกยูนิต (Room No.) ที่ต้องการวิเคราะห์", available_rooms)

use_agent_pricing = st.checkbox("ตรวจสอบราคาสำหรับ agent")

if selected_rooms:
    unit_df = project_df[project_df["เลขห้อง"].astype(str).isin(selected_rooms)].copy()
    unit_df["เลขห้อง"] = unit_df["เลขห้อง"].astype(str)

    st.subheader("📋 รายละเอียดพร้อมเสนอราคา")

    cost_total = 0.0
    price_total = 0.0

    for idx, row in unit_df.iterrows():
        room_no = row["เลขห้อง"]
        asking = row["asking price"]
        bottom = row["bottom price"]
        cost = row["ต้นทุนรวม"]
        maintenance = row["ค่าส่วนกลาง"]

        price_default = bottom
        price_label = f"ราคาที่เสนอสำหรับยูนิต {room_no}"

        if use_agent_pricing:
            agent_price = asking - ((asking * 0.0027) + (maintenance * 24))
            price_default = round(agent_price, 2)

        user_price = st.number_input(
            label=price_label,
            min_value=0.0,
            value=float(price_default),
            step=10000.0,
            key=f"user_price_{room_no}"
        )

        project_value = user_price
        gp_unit = round((project_value - cost) / project_value * 100, 2)
        gp_diff = round(gp_unit - gp_committed, 2)

        cost_total += cost
        price_total += user_price

        html_block = f"""
        <div style='border: 1px solid #ddd; background-color: #fefefe; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p><strong>ยูนิต:</strong> {room_no}</p>
            <p><strong>Asking Price:</strong> {asking:,.2f} บาท</p>
            <p><strong>Bottom Price:</strong> {bottom:,.2f} บาท</p>
            <p><strong>ราคาที่เสนอ:</strong> {user_price:,.2f} บาท</p>
            <hr style='margin: 10px 0;'>
            <p><strong>GP (รายแปลง):</strong> {gp_unit:.2f}%</p>
            <p><strong>GP (Committed):</strong> {gp_committed:.2f}%</p>
            <p><strong>ผลต่าง GP:</strong> <span style='color: {"green" if gp_diff >= 0 else "red"}'>{gp_diff:+.2f}%</span></p>
        </div>
        """
        st.markdown(html_block, unsafe_allow_html=True)

    gp_project = 0.0
    if price_total > 0:
        gp_project = round(((price_total - cost_total) / price_total * 100), 2)

    st.markdown("---")
    st.subheader("📊 GP ของโครงการ")
    gp_project_diff = round(gp_project - gp_committed, 2)
    st.markdown(f"""
        <div style='border: 2px solid #2ecc71; padding: 1rem; border-radius: 10px; background-color: #eafff5; text-align: center;'>
            <h3 style='margin: 0;'>GP รวมของโครงการ: <span style='color: {"red" if gp_project < gp_committed else "green"}'>{gp_project:.2f}%</span></h3>
            <p style='margin: 0;'>GP Committed สำหรับโครงการนี้: {gp_committed:.2f}%</p>
            <p style='margin: 0;'>ผลต่าง: <span style='color: {"green" if gp_project_diff >= 0 else "red"}'>{gp_project_diff:+.2f}%</span></p>
        </div>
    """, unsafe_allow_html=True)

else:
    st.info("กรุณาเลือกยูนิตเพื่อดูรายละเอียด")