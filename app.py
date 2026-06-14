import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Smart Waste System",
    page_icon="♻️",
    layout="wide"
)

# ---------------- PROFESSIONAL CSS ----------------
st.markdown("""
<style>

body {
    background-color: #f4f6f9;
}

h1, h2, h3 {
    color: #1f4e79;
}

.stButton>button {
    background: linear-gradient(90deg, #2b5876, #4e4376);
    color: white;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
}

.stButton>button:hover {
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)

# ---------------- FILES ----------------
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

# ---------------- LOGOUT FUNCTION ----------------
def logout():
    st.session_state.clear()
    st.rerun()

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.title("♻️ AI Smart Waste System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Enter username & password")

# ---------------- DASHBOARD ----------------
else:

    st.title(f"📊 Welcome {st.session_state.username}")

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

        st.subheader("Report Waste")

        area = st.text_input("Area")
        waste = st.selectbox("Waste Type",
                             ["Organic","Plastic","Metal","Paper","Glass"])
        weight = st.number_input("Weight (kg)", min_value=0.0)

        lat = st.number_input("Latitude")
        lon = st.number_input("Longitude")

        if st.button("Submit"):

            new = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Area": area,
                "Waste_Type": waste,
                "Weight_kg": weight,
                "Status": "Pending",
                "Latitude": lat,
                "Longitude": lon
            }])

            df = pd.concat([df, new], ignore_index=True)
            save_data(df)

            st.session_state.points += 10

            st.success("Submitted Successfully!")
            st.toast("Eco Points +10 🌱")

    # ---------------- UPLOAD ----------------
    with tab2:

        st.subheader("Upload Image")

        img = st.file_uploader("Choose Image", type=["jpg","png","jpeg"])

        if img:

            path = os.path.join(UPLOAD_DIR, img.name)

            with open(path, "wb") as f:
                f.write(img.getbuffer())

            st.image(img, width=300)
            st.success("Uploaded Successfully")

    # ---------------- ANALYTICS ----------------
    with tab3:

        st.subheader("Analytics")

        if len(df) > 0:

            st.dataframe(df)

            st.bar_chart(df.groupby("Area")["Weight_kg"].sum())
            st.bar_chart(df.groupby("Waste_Type")["Weight_kg"].sum())

            st.map(df[["Latitude","Longitude"]])

        else:
            st.info("No data available")

    st.divider()

    # ---------------- LOGOUT ----------------
    st.button("🚪 Logout", on_click=logout)
