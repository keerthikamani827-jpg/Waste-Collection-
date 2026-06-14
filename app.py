import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Smart Waste Collection System",
    page_icon="♻️",
    layout="wide"
)

# ---------------- CLEAN CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f6f8fa;
}

h1, h2, h3 {
    color: #1f2d3d;
}

.stButton>button {
    background-color: #1f4e79;
    color: white;
    border-radius: 6px;
    padding: 8px 16px;
}

.stButton>button:hover {
    background-color: #163a5c;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FILE ----------------
DATA_FILE = "data.csv"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "points" not in st.session_state:
    st.session_state.points = 100

# ---------------- LOAD DATA ----------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=[
        "Date","Area","Waste_Type","Weight_kg",
        "Status","Latitude","Longitude"
    ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# ---------------- LOGOUT ----------------
def logout():
    st.session_state.clear()
    st.rerun()

# ---------------- TITLE ----------------
st.title("♻️ AI Smart Waste Collection System")

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:

    st.subheader("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Enter valid credentials")

# ---------------- DASHBOARD ----------------
else:

    st.success(f"Welcome {st.session_state.username}")

    total_waste = df["Weight_kg"].sum() if len(df) > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Waste", f"{total_waste} kg")
    c2.metric("Eco Points", st.session_state.points)
    c3.metric("CO₂ Saved", f"{int(total_waste*0.4)} kg")

    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "Report Waste",
        "Upload Image",
        "Analytics"
    ])

    # ---------------- REPORT ----------------
    with tab1:

        st.subheader("Waste Reporting")

        area = st.text_input("Area")
        waste_type = st.selectbox(
            "Waste Type",
            ["Organic","Plastic","Metal","Paper","Glass"]
        )
        weight = st.number_input("Weight (kg)", min_value=0.0)

        # CLEAN LAT/LON INPUT
        st.write("Location Details")
        col1, col2 = st.columns(2)

        with col1:
            latitude = st.number_input("Latitude")

        with col2:
            longitude = st.number_input("Longitude")

        if st.button("Submit Report"):

            new_data = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Area": area,
                "Waste_Type": waste_type,
                "Weight_kg": weight,
                "Status": "Pending",
                "Latitude": latitude,
                "Longitude": longitude
            }])

            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)

            st.session_state.points += 10

            st.success("Report Submitted Successfully")

    # ---------------- UPLOAD ----------------
    with tab2:

        st.subheader("Upload Waste Image")

        file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

        if file:

            path = os.path.join(UPLOAD_DIR, file.name)

            with open(path, "wb") as f:
                f.write(file.getbuffer())

            st.image(file, width=300)
            st.success("Uploaded Successfully")

    # ---------------- ANALYTICS ----------------
    with tab3:

        st.subheader("Analytics Dashboard")

        if len(df) > 0:

            st.dataframe(df)

            st.bar_chart(df.groupby("Area")["Weight_kg"].sum())
            st.bar_chart(df.groupby("Waste_Type")["Weight_kg"].sum())
            st.bar_chart(df["Status"].value_counts())

            # FIXED MAP HANDLING
            map_df = df.dropna(subset=["Latitude","Longitude"])
            map_df = map_df.rename(columns={"Latitude":"lat","Longitude":"lon"})

            st.map(map_df[["lat","lon"]])

            if df["Weight_kg"].max() > 100:
                st.warning("High Waste Area Detected")

        else:
            st.info("No data available")

    st.divider()

    # ---------------- LOGOUT ----------------
    if st.button("Logout"):
        logout()
