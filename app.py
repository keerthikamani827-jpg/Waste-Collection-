import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="AI Smart Waste Collection",
    page_icon="♻️",
    layout="wide"
)

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login Page
if not st.session_state.logged_in:

    st.title("♻️ AI Smart Waste Collection")
    st.subheader("Smart Waste Management System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Please enter username and password")

# Dashboard
else:

    st.title("📊 Waste Collection Dashboard")

    st.success(f"Welcome {st.session_state.username}")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("♻️ Waste Collected", "1250 kg")
    col2.metric("🚛 Active Trucks", "12")
    col3.metric("🌱 CO₂ Saved", "540 kg")
    col4.metric("🏆 Eco Points", "250")

    st.divider()

    # Buttons
    c1, c2, c3 = st.columns(3)

    with c1:
        st.button("🗑 Report Waste")

    with c2:
        st.button("📍 Track Collection")

    with c3:
        st.button("📷 Upload Waste Image")

    st.divider()

    # Waste Category
    st.subheader("Waste Category")

    waste_type = st.selectbox(
        "Select Waste Type",
        ["Plastic", "Paper", "Metal", "Glass", "Organic"]
    )

    st.write("Selected Waste Type:", waste_type)

    st.divider()

    # Image Upload
    uploaded_image = st.file_uploader(
        "Upload Waste Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:
        st.image(uploaded_image, width=300)
        st.success(f"Waste Type: {waste_type}")

    st.divider()

    # Dataset Upload
    st.subheader("Dataset Analysis")

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.write("### Dataset Preview")
        st.dataframe(df)

        st.write("### Dataset Statistics")
        st.write(df.describe())

        if len(df.columns) > 1:
            st.write("### Bar Chart")
            st.bar_chart(df.iloc[:, 1])

    st.divider()

    # Eco Rewards
    st.subheader("🏆 Eco Rewards")

    points = 250

    st.progress(points / 500)

    st.write(f"Eco Points: {points}/500")

    st.divider()

    # Monthly Collection
    st.subheader("📈 Monthly Collection")

    monthly_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Waste": [120, 180, 200, 250, 300, 350]
    })

    st.line_chart(monthly_data.set_index("Month"))

    st.divider()

    # Logout
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
