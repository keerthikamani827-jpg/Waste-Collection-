import streamlit as st
import pandas as pd

# Page Settings
st.set_page_config(page_title="AI Smart Waste Collection", layout="wide")

# Login State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login Page
if not st.session_state.logged_in:

    st.title("♻️ AI Smart Waste Collection")
    st.subheader("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Enter username and password")

# Dashboard
else:

    st.title("📊 Waste Collection Dashboard")

    st.success(f"Welcome {st.session_state.username}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("🗑 Report Waste")

    with col2:
        st.button("📍 Track Collection")

    with col3:
        st.button("📷 Upload Waste Image")

    st.divider()

    st.subheader("Waste Dataset Analysis")

    uploaded_file = st.file_uploader(
        "Upload your dataset (CSV)",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.write("### Dataset Preview")
        st.dataframe(df)

        st.write("### Dataset Information")
        st.write(df.describe())

        if len(df.columns) > 1:
            st.write("### Visualization")
            st.bar_chart(df.iloc[:, 1])

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()