
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="SVR GP Dashboard", layout="wide")

# โหลดโลโก้
st.image("logo.png", width=250)

st.title("📊 รายละเอียดพร้อมเสนอราคา")

# โหลดไฟล์ Excel โดยอัตโนมัติ
@st.cache_data
def load_data():
    return pd.read_excel("Corporate_Project_Template.xlsx", sheet_name="ALL PROJECTS")

df = load_data()

# ดรอปดาวน์เลือกโครงการ
project_list = ["ALL PROJECTS"] + sorted(df["โครงการ"].dropna().unique())
selected_project = st.selectbox("เลือกโครงการ", project_list)

# กรองข้อมูลตามโครงการ
filtered_df = df.copy()
if selected_project != "ALL PROJECTS":
    filtered_df = df[df["โครงการ"] == selected_project]

# ดรอปดาวน์เลือกยูนิต
unit_list = sorted(filtered_df["เลขห้อง"].dropna().astype(str).unique())
selected_unit = st.selectbox("เลือกยูนิต", unit_list)

# แสดงผลเฉพาะยูนิตที่เลือก
unit = filtered_df[filtered_df["เลขห้อง"].astype(str) == selected_unit]
if not unit.empty:
    u = unit.iloc[0]

    asking_price = float(u["Asking Price"])
    bottom_price = float(u["Bottom Price"])
    cost = float(u["ต้นทุนรวม"])
    area = float(u["พื้นที่ ตร.ว."])
    common_fee = float(u["ค่าส่วนกลาง"])

    # คำนวณราคา Agent และ GP
    agent_fee = (asking_price * 0.27) + (area * 24 * common_fee)
    agent_price = asking_price - agent_fee

    gp_committed = (bottom_price - cost) / bottom_price if bottom_price else 0
    gp_agent = (agent_price - cost) / agent_price if agent_price else 0

    # แสดงผลข้อมูล
    st.markdown(f"### ✳️ ยูนิต: {selected_unit}")
    st.markdown(f"**โครงการ:** {u['โครงการ']}")
    st.markdown(f"**แบบบ้าน:** {u['แบบบ้าน']}")
    st.markdown(f"**Asking Price:** {asking_price:,.2f} บาท")
    st.markdown(f"**Bottom Price:** {bottom_price:,.2f} บาท")
    st.markdown(f"**ราคาสำหรับ Agent:** {agent_price:,.2f} บาท")
    st.markdown(f"**ต้นทุนรวม:** {cost:,.2f} บาท")

    st.markdown("---")
    st.subheader("💹 สรุปกำไรเบื้องต้น (GP)")
    st.markdown(f"• GP (จาก Bottom Price): **{gp_committed*100:.2f}%**")
    st.markdown(f"• GP (จากราคาสำหรับ Agent): **{gp_agent*100:.2f}%**")
else:
    st.warning("ไม่พบข้อมูลยูนิตที่เลือก")
