
import streamlit as st
import pandas as pd
from PIL import Image

# Load logo
logo = Image.open("logo.png")
st.image(logo, width=250)

st.markdown("## 📊 รายละเอียดพร้อมเสนอราคา")

# Upload Excel
uploaded_file = st.file_uploader("อัปโหลดไฟล์ Excel", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # Drop rows with missing project or unit
    df = df.dropna(subset=["โครงการ", "เลขห้อง"])
    
    # Unique project list
    project_list = ["ALL PROJECTS"] + sorted(df["โครงการ"].unique())
    selected_project = st.selectbox("เลือกโครงการ", project_list)
    
    if selected_project != "ALL PROJECTS":
        df = df[df["โครงการ"] == selected_project]
    
    unit_list = df["เลขห้อง"].astype(str).unique().tolist()
    selected_unit = st.selectbox("🔍 เลือกยูนิต (Room No.) ที่ต้องการวิเคราะห์", [""] + unit_list)
    
    if selected_unit:
        unit = df[df["เลขห้อง"].astype(str) == selected_unit]
        if not unit.empty:
            asking_price = float(unit["Asking Price"].values[0])
            bottom_price = float(unit["Bottom Price"].values[0])
            cost = float(unit["ต้นทุนรวม"].values[0])
            area = float(unit["พื้นที่ ตร.ว."].values[0])
            common_fee = float(unit["ค่าส่วนกลาง"].values[0])

            # Agent Fee: 27% + ค่าส่วนกลาง × พท × 24
            agent_fee = (asking_price * 0.27) + (area * 24 * common_fee)
            agent_price = asking_price - agent_fee

            gp_raw = (bottom_price - cost) / bottom_price
            gp_committed = (agent_price - cost) / agent_price
            gp_diff = gp_raw - gp_committed

            st.markdown(f"### 💰 ราคาที่เสนอสำหรับยูนิต {selected_unit}")
            st.code(f"{bottom_price:,.2f}")

            with st.container():
                st.markdown(f"**ยูนิต:** {selected_unit}")
                st.markdown(f"**Asking Price:** {asking_price:,.2f} บาท")
                st.markdown(f"**Bottom Price:** {bottom_price:,.2f} บาท")
                st.markdown(f"**ราคาที่เสนอ:** {bottom_price:,.2f} บาท")
                st.markdown(f"**GP (รายแปลง):** {gp_raw:.2%}")
                st.markdown(f"✨ **GP (Committed แปลงนี้):** {gp_committed:.2%}")
                st.markdown(f"📍 **ผลต่าง GP:** {'+' if gp_diff >= 0 else ''}{gp_diff:.2%}")
        
        else:
            st.warning("ไม่พบข้อมูลยูนิตนี้")
else:
    st.info("กรุณาอัปโหลดไฟล์ Excel เพื่อตรวจสอบข้อมูล")
