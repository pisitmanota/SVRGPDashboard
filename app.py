import streamlit as st

st.set_page_config(layout="wide")

# Sample data preview
st.markdown("## 📄 รายละเอียดพร้อมเสนอราคา")

# Example values (hardcoded for demonstration)
asking_price = 6603300.00
bottom_price = 5903300.00
offer_price = 5903300.00
cost = 4527360.00

gp_unit = round((offer_price - cost) / offer_price * 100, 2)
gp_committed_unit = round((bottom_price - cost) / bottom_price * 100, 2)
gp_committed_project = 28.40
gp_diff = round(gp_unit - gp_committed_project, 2)

# Display
st.write(f"**ยูนิต:** 22")
st.write(f"**Asking Price:** {asking_price:,.2f} บาท")
st.write(f"**Bottom Price:** {bottom_price:,.2f} บาท")
st.write(f"**ราคาที่เสนอ:** {offer_price:,.2f} บาท")

st.write(f"**GP (รายแปลง):** {gp_unit:.2f}%")
st.write(f"✨ **GP (Committed แปลงนี้):** {gp_committed_unit:.2f}%")
st.write(f"🎯 **GP (Committed โครงการ):** {gp_committed_project:.2f}%")

gp_diff_text = f"+{gp_diff:.2f}%" if gp_diff >= 0 else f"{gp_diff:.2f}%"
gp_color = "green" if gp_diff >= 0 else "red"
st.markdown(f"**ผลต่าง GP:** <span style='color:{gp_color}'>{gp_diff_text}</span>", unsafe_allow_html=True)