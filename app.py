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

# GP committed mapping per project
gp_committed_map = {
    "GRAND SVR": 30.60,
    "SVR VILLAGE 58": 29.39,
    "SVR PARK 76": 28.40,
    "SVR VILLAGE SAI-NOI": 26.73,
    "SVR NP-ASSUMPTION": 25.36,
    "SVR HYDE BK": 32.00,
    "SVR HYDE S3": 27.07
}

df = pd.read_excel("Corporate_Project_Template.xlsx")
projects = df["โครงการ"].unique()
selected_project = st.selectbox("เลือกโครงการ", projects)

# Get GP committed for the selected project
gp_committed = gp_committed_map.get(selected_project, 27.00)

project_df = df[df["โครงการ"] == selected_project].copy()
available_rooms = project_df["เลขห้อง"].astype(str).tolist()
selected_rooms = st.multiselect("🔎 เลือกยูนิต (Room No.) ที่ต้องการวิเคราะห์", available_rooms)

use_agent_pricing = st.checkbox("ตรวจสอบราคาสำหรับ agent")

if selected_rooms:
    st.subheader("📋 ข้อมูลยูนิตที่เลือก")
    unit_df = project_df[project_df["เลขห้อง"].astype(str).isin(selected_rooms)].copy()

    if use_agent_pricing:
        if all(col in unit_df.columns for col in ["asking price", "ค่าส่วนกลาง", "ต้นทุนรวม", "bottom price"]):
            unit_df["ราคาสำหรับ Agent"] = (
                (unit_df["asking price"] - (unit_df["asking price"] * 0.0027)) + (unit_df["ค่าส่วนกลาง"] * 24)
            ).round(2)

            unit_df["ราคาขายที่ GP 14%"] = (unit_df["ต้นทุนรวม"] / 0.86).round(2)

            user_prices = []
            st.subheader("✍️ เสนอราคาขายต่อยูนิต")
            for idx, row in unit_df.iterrows():
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"ยูนิต: {row['เลขห้อง']}")
                with col2:
                    user_price = st.number_input(
                        label=f"ราคาที่เสนอสำหรับยูนิต {row['เลขห้อง']}",
                        min_value=0.0,
                        step=10000.0,
                        key=f"user_price_{row['เลขห้อง']}"
                    )
                    user_prices.append(user_price)

            unit_df["ราคาที่เสนอ"] = user_prices
            unit_df["GP จากราคาที่เสนอ (%)"] = ((unit_df["ราคาที่เสนอ"] - unit_df["ต้นทุนรวม"]) / unit_df["ราคาที่เสนอ"] * 100).round(2)
            unit_df["ผลต่างราคา"] = (unit_df["ราคาที่เสนอ"] - unit_df["bottom price"]).round(2)
            unit_df["ผลต่าง GP (%)"] = (unit_df["GP จากราคาที่เสนอ (%)"] - gp_committed).round(2)

            st.markdown("---")
            st.subheader("🧾 สรุปรายยูนิต (Styled Summary)")
            for idx, row in unit_df.iterrows():
                bg_color = "#f9f9f9"
                st.markdown(f"""
                <div style='border: 1px solid #cce5ff; background-color: {bg_color}; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                    <strong>ยูนิต:</strong> {row['เลขห้อง']}<br>
                    <strong>Bottom Price:</strong> {row['bottom price']:,} บาท<br>
                    <strong>ราคาที่เสนอ:</strong> {row['ราคาที่เสนอ']:,} บาท<br>
                    <strong>ผลต่างราคา:</strong> <span style='color: {"red" if row["ผลต่างราคา"] < 0 else "green"}'>{row["ผลต่างราคา"]:,}</span> บาท<br><br>
                    <strong>GP (รายแปลง):</strong> {row["GP จากราคาที่เสนอ (%)"]:.2f}%<br>
                    <strong>GP (Committed):</strong> {gp_committed:.2f}%<br>
                    <strong>ผลต่าง GP:</strong> <span style='color: {"red" if row["ผลต่าง GP (%)"] < 0 else "green"}'>{row["ผลต่าง GP (%)"]:+.2f}%</span><br>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            sum_cost = unit_df["ต้นทุนรวม"].sum()
            sum_user_price = unit_df["ราคาที่เสนอ"].sum()
            gp_project = ((sum_user_price - sum_cost) / sum_user_price * 100).round(2) if sum_user_price > 0 else 0

            st.subheader("📊 GP ของโครงการ")
            st.markdown(f"""
                <div style='border: 2px solid #2ecc71; padding: 1rem; border-radius: 10px; background-color: #eafff5; text-align: center;'>
                    <h3 style='margin: 0;'>GP รวมของโครงการ: <span style='color: {"red" if gp_project < gp_committed else "green"}'>{gp_project:.2f}%</span></h3>
                    <p style='margin: 0;'>GP Committed สำหรับโครงการนี้: {gp_committed:.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ ไม่พบคอลัมน์ที่จำเป็น: asking price, ค่าส่วนกลาง, ต้นทุนรวม, bottom price")
    else:
        st.info("กรุณาเลือกโหมด 'ตรวจสอบราคาสำหรับ agent'")
else:
    st.info("กรุณาเลือกยูนิตเพื่อดูรายละเอียด")