import streamlit as st
import pandas as pd

st.set_page_config(page_title="SVR Project GP Dashboard", layout="wide")

# ---------------------- Load Data ----------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Corporate_Project_Template.xlsx", sheet_name=None)
    return df

data = load_data()

# ---------------------- Sidebar ----------------------
st.sidebar.image("logo.png", use_column_width=True)
project = st.sidebar.selectbox("เลือกโครงการ", data.keys())
df = data[project]

room_list = df["เลขห้อง"].dropna().astype(str).tolist()
selected_rooms = st.sidebar.multiselect("🔎 เลือกยูนิต (Room No.) ที่ต้องการวิเคราะห์", room_list)

check_agent = st.sidebar.checkbox("ตรวจสอบราคาสำหรับ agent")

# ---------------------- GP Reference ----------------------
gp_reference = {
    "GRAND SVR": 30.60,
    "SVR VILLAGE 58": 29.39,
    "SVR PARK 76": 28.40,
    "SVR VILLAGE SAI-NOI": 26.73,
    "SVR NP-ASSUMPTION": 25.36,
    "SVR HYDE BK": 32.00,
    "SVR HYDE S3": 27.07,
}
gp_committed_project = gp_reference.get(project, 28.0)

# ---------------------- Main ----------------------
st.title("📊 รายละเอียดพร้อมเสนอราคา")

if not selected_rooms:
    st.info("กรุณาเลือกยูนิตเพื่อแสดงข้อมูล")
else:
    total_cost = 0
    total_offer = 0

    for room in selected_rooms:
        unit = df[df["เลขห้อง"].astype(str) == room]

        if unit.empty:
            continue

        asking_price = unit["asking price"].values[0]
        bottom_price = unit["bottom price"].values[0]
        cost = unit["ต้นทุนรวม"].values[0]
        area = unit.get("พื้นที่(ตร.ว.)", pd.Series([0])).values[0]
        common_fee = unit.get("ค่าส่วนกลาง", pd.Series([0])).values[0]

        if check_agent:
            offer_price = asking_price - ((asking_price * 0.0027) + (area * 24 * common_fee))
        else:
            offer_price = bottom_price

        gp_unit = round((offer_price - cost) / offer_price * 100, 2)
        gp_committed_unit = round((bottom_price - cost) / bottom_price * 100, 2)
        gp_diff = round(gp_unit - gp_committed_project, 2)

        total_cost += cost
        total_offer += offer_price

        gp_color = "green" if gp_diff >= 0 else "red"
        gp_diff_text = f"+{gp_diff:.2f}%" if gp_diff >= 0 else f"{gp_diff:.2f}%"

        with st.container():
            st.subheader(f"📋 ยูนิต: {room}")
            st.write(f"**Asking Price:** {asking_price:,.2f} บาท")
            st.write(f"**Bottom Price:** {bottom_price:,.2f} บาท")
            st.write(f"**ราคาที่เสนอ:** {offer_price:,.2f} บาท")

            st.write(f"**GP (รายแปลง):** {gp_unit:.2f}%")
            st.write(f"✨ **GP (Committed แปลงนี้):** {gp_committed_unit:.2f}%")
            st.write(f"🎯 **GP (Committed โครงการ):** {gp_committed_project:.2f}%")
            st.markdown(f"**ผลต่าง GP:** <span style='color:{gp_color}'>{gp_diff_text}</span>", unsafe_allow_html=True)

    # GP รวมโครงการ
    project_gp = round((total_offer - total_cost) / total_offer * 100, 2)
    gp_project_diff = round(project_gp - gp_committed_project, 2)
    diff_color = "green" if gp_project_diff >= 0 else "red"
    gp_diff_text_proj = f"+{gp_project_diff:.2f}%" if gp_project_diff >= 0 else f"{gp_project_diff:.2f}%"

    st.markdown("---")
    with st.container():
        st.subheader("📊 GP ของโครงการ")
        st.markdown(f"<div style='padding:20px; background-color:#E9FBF0; border:1px solid #2ECC71;'>"
                    f"<h3 style='text-align:center;'>GP รวมของโครงการ: <span style='color:#2ECC71'>{project_gp:.2f}%</span></h3>"
                    f"<p style='text-align:center;'>GP Committed สำหรับโครงการนี้: {gp_committed_project:.2f}%<br>"
                    f"ผลต่าง: <span style='color:{diff_color}'>{gp_diff_text_proj}</span></p></div>",
                    unsafe_allow_html=True)