
import streamlit as st
import pandas as pd

# โหลดข้อมูล
df = pd.read_excel("Corporate_Project_Template.xlsx")

st.set_page_config(page_title="Project GP Summary", layout="wide")
st.title("📊 Project GP Summary Dashboard")

# เลือกโครงการ
projects = df["โครงการ"].unique()
selected_project = st.selectbox("เลือกโครงการ", projects)

# กรองข้อมูลตามโครงการ
project_df = df[df["โครงการ"] == selected_project].copy()

# เลือกยูนิตที่จะใช้ในการวิเคราะห์
available_rooms = project_df["เลขห้อง"].astype(str).tolist()
selected_rooms = st.multiselect("🔎 เลือกยูนิต (Room No.) ที่ต้องการวิเคราะห์", available_rooms)

# กรองข้อมูลเฉพาะยูนิตที่เลือก
unit_df = project_df[project_df["เลขห้อง"].astype(str).isin(selected_rooms)].copy()

if unit_df.empty:
    st.warning("กรุณาเลือกยูนิตที่ต้องการก่อน จึงจะแสดงข้อมูลได้")
else:
    # ป้อนราคาที่เสนอ (อนุมัติ)
    st.markdown("### 💰 ป้อนราคาขายที่ต้องการเสนอ (ต่อยูนิต)")
    suggested_prices = []
    for i, row in unit_df.iterrows():
        price = st.number_input(
            label=f"ห้อง {row['เลขห้อง']} ({row['แบบบ้าน']}) - Bottom Price: {row['Bottom Price']:,.2f} THB",
            min_value=0.0,
            value=float(row["Project Value"]),
            key=f"suggested_{i}"
        )
        suggested_prices.append(price)

    # เพิ่มราคาขออนุมัติ
    unit_df["Proposed Price"] = suggested_prices

    # คำนวณ GP
    unit_df["GP_Actual"] = (unit_df["Proposed Price"] - unit_df["ต้นทุนรวม"]) / unit_df["Proposed Price"]
    unit_df["GP_Committed"] = (unit_df["Bottom Price"] - unit_df["ต้นทุนรวม"]) / unit_df["Bottom Price"]
    unit_df["GP_Diff"] = unit_df["GP_Actual"] - unit_df["GP_Committed"]

    # คำนวณรวม
    bottom_total = unit_df["Bottom Price"].sum()
    proposed_total = unit_df["Proposed Price"].sum()
    cost_total = unit_df["ต้นทุนรวม"].sum()

    gp_actual_avg = (proposed_total - cost_total) / proposed_total if proposed_total != 0 else 0
    gp_committed_avg = (bottom_total - cost_total) / bottom_total if bottom_total != 0 else 0
    gp_diff_avg = gp_actual_avg - gp_committed_avg
    price_diff = proposed_total - bottom_total

    st.markdown("### 📋 สรุปภาพรวมยูนิตที่เลือก")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**BOTTOM PRICE รวม**")
        st.write(f"฿{bottom_total:,.2f}")
    with col2:
        st.markdown("**ขออนุมัติราคา**")
        st.write(f"฿{proposed_total:,.2f}")
    with col3:
        st.markdown("**ส่วนต่างราคา**")
        st.write(f"฿{price_diff:,.2f}", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 เปรียบเทียบ GP")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("**GP (Committed)**")
        st.write(f"{gp_committed_avg * 100:.2f}%", unsafe_allow_html=True)
    with col5:
        st.markdown("**GP (รายแปลง)**")
        st.write(f"{gp_actual_avg * 100:.2f}%", unsafe_allow_html=True)
    with col6:
        color = "green" if gp_diff_avg > 0 else "red" if gp_diff_avg < 0 else "black"
        st.markdown(f"**GP Δ**")
        st.markdown(f"<span style='color:{color}; font-size:24px'>{gp_diff_avg * 100:+.2f}%</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧾 รายละเอียดยูนิตที่เลือก")

    # แสดงตารางรายละเอียดยูนิต พร้อมสถานะ
    detail_df = unit_df[["เลขห้อง", "แบบบ้าน", "สถานะแปลง", "ต้นทุนรวม", "Bottom Price", "Proposed Price", "GP_Actual", "GP_Committed", "GP_Diff"]].copy()
    detail_df = detail_df.rename(columns={
        "เลขห้อง": "Room",
        "แบบบ้าน": "Type",
        "สถานะแปลง": "Status",
        "ต้นทุนรวม": "Cost",
        "Bottom Price": "Bottom Price",
        "Proposed Price": "Proposed Price",
        "GP_Actual": "GP (Actual)",
        "GP_Committed": "GP (Committed)",
        "GP_Diff": "GP Δ"
    })
    st.dataframe(detail_df.style.format({
        "Cost": "฿{:,.2f}",
        "Bottom Price": "฿{:,.2f}",
        "Proposed Price": "฿{:,.2f}",
        "GP (Actual)": "{:.2%}",
        "GP (Committed)": "{:.2%}",
        "GP Δ": "{:+.2%}"
    }), use_container_width=True)
