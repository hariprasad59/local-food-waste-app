import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Local Food Wastage Management System",
    layout="wide"
)

# ✅ Clean styling — no background color, only centered footer
st.markdown("""
    <style>
        footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            color: gray;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# 🌟 Page Title
st.title("Local Food Wastage Management System")
st.markdown("### Bridging the gap between surplus and scarcity")

# 🧩 Layout columns
col1, col2 = st.columns([1.2, 1])

with col1:
    st.write("""
    Every day, tons of edible food go to waste while many people remain hungry.  
    The **Local Food Wastage Management System** aims to tackle this by connecting:
    - **Food Providers** (restaurants, NGOs, caterers, hotels) who have surplus food  
    - **Receivers** (shelters, food banks, orphanages) who are in need of food  

    Through this system, we can:
    - Streamline food donation and distribution  
    - Reduce wastage by optimizing logistics based on **location and demand**  
    - Gain data-driven insights to **improve efficiency and equity**  

    ---
    """)

with col2:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2921/2921822.png",
        use_container_width=True,
        caption="Reduce food waste, feed the needy 🍛"
    )

st.markdown("---")

# 🧾 Footer (centered)
st.markdown("""
    <footer>
        Developed by <b>M. Hari Prasad</b>
    </footer>
""", unsafe_allow_html=True)
