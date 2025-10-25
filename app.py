import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Local Food Wastage Management System",
    layout="wide"
)

st.markdown("""
    <style>
        body {
            background-color: #f0f5f5;
        }
        .stApp {
            background-color: #f0f5f5;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Local Food Wastage Management System")
st.markdown("### Bridging the gap between surplus and scarcity")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.write("""
    Every day, tons of edible food go to waste while many people remain hungry.  
    The **Local Food Wastage Management System** aims to tackle this by connecting:
    - **Food Providers** (restaurants, NGOs, caterers, hotels) who have surplus food  
    -  **Receivers** (shelters, food banks, orphanages) who are in need of food  

    Through this system, we can:
    -  Streamline food donation and distribution  
    -  Reduce wastage by optimizing logistics based on **location and demand**  
    -  Gain data-driven insights to **improve efficiency and equity**  

    --- 
    """)

with col2:
    # Optional: You can place a nice banner or logo here
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2921/2921822.png",
        use_container_width=True,
        caption="Reduce food waste, feed the needy 🍛"
    )

st.markdown("---")
