import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="AI Smart Waste Collection",
    page_icon="♻️",
    layout="wide"
)

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN PAGE =================

if not st.session_state.logged_in:

    st.title("♻️ AI Smart Waste Collection")
    st.subheader("Smart Waste Management System")

    st.markdown("---")

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("🚀 Login"):

        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Please enter username and password")

# ================= DASHBOARD =================

else:

    st.title("📊 Waste Collection Dashboard")

    st.success(f"Welcome {st.session_state.username}")

    st.info("🔔 Waste collection vehicle arriving in 15 minutes")

    # Metrics

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("♻️ Waste Collected", "1250 kg", "+12%")
    col2.metric("🚛 Active Trucks", "12", "+2")
    col3.metric("🌱 CO₂ Saved", "540 kg", "+15%")
    col4.metric("🏆 Eco Points", "250", "+20")

    st.markdown("---")

    # Buttons

    c1, c2, c3 = st.columns(3)

    with c1:
        st.button("🗑 Report Waste")

    with c2:
        st.button("📍 Track Collection")

    with c3:
        st.button("📷 Upload Waste Image")

    st.markdown("---")

    # Waste Category

    st.subheader("🗑 Waste Category")

    waste_type = st.selectbox(
        "Select Waste Type",
        ["Plastic", "Paper", "Metal", "Glass", "Organic"]
    )

    st.success(f"Selected Waste Type: {waste_type}")

    # Image Upload

    st.subheader("📷 Waste Image Analysis")

    uploaded_image = st.file_uploader(
        "Upload Waste Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:

        st.image(uploaded_image, width=300)

        st.success(f"AI Prediction: {waste_type} Waste ♻️")

    st.markdown("---")

    # Dataset Upload

    st.subheader("📂 Waste Dataset Analysis")

    uploaded_file = st.file_uploader(
        "Upload Dataset CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.write("### Dataset Preview")
        st.dataframe(df)

        st.write("### Dataset Statistics")
        st.write(df.describe())

        if len(df.columns) > 1:

            st.write("### Dataset Bar Chart")
            st.bar_chart(df.iloc[:, 1])

    st.markdown("---")

    # Pie Chart

    st.subheader("📈 Waste Distribution")

    waste_data = pd.DataFrame({
        "Type": ["Plastic", "Paper", "Metal", "Glass", "Organic"],
        "Count": [45, 30, 15, 20, 25]
    })

    fig = px.pie(
        waste_data,
        values="Count",
        names="Type",
        title="Waste Distribution Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Eco Rewards

    st.subheader("🏆 Eco Rewards")

    points = 250

    st.progress(points / 500)

    st.write(f"Current Eco Points: {points}/500")

    if points >= 250:
        st.success("🥈 Green Citizen Badge Earned!")

    st.markdown("---")

    # Monthly Collection Data

    st.subheader("📅 Monthly Waste Collection")

    monthly = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Waste": [120, 180, 200, 250, 300, 350]
    })

    st.line_chart(monthly.set_index("Month"))

    st.markdown("---")

    # Sustainability Score

    st.subheader("🌍 Sustainability Score")

    score = 85

    st.progress(score / 100)

    st.write(f"Current Sustainability Score: {score}/100")

    st.markdown("---")

    # Logout

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
