import streamlit as st
import pandas as pd
import os
from datetime import datetime
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Eco Hero Waste System",
    page_icon="🌍",
    layout="wide"
)

# ---------------- PASTEL + ATTRACTIVE UI ----------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #fdfbfb, #ebedee);
}

h1, h2, h3 {
    color: #4b6cb7;
}

.stButton>button {
    background: linear-gradient(90deg, #4b6cb7, #182848);
    color: white;
    border-radius: 12px;
    padding: 10px;
    font-weight: bold;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #182848, #4b6cb7);
}

.card {
    background: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
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

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:

    st.title("🌍 Eco Hero Waste Management System")

    st.write("♻️ Save Earth | Earn Points | Become Hero")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("🚀 Login"):

        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Please fill all fields")

# ---------------- DASHBOARD ----------------
else:

    st.title(f"🌍 Welcome Eco Hero: {st.session_state.username}")

    total_waste = df["Weight_kg"].sum() if len(df) > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("♻️ Total Waste", f"{total_waste} kg")
    col2.metric("🏆 Eco Points", st.session_state.points)
    col3.metric("🌱 CO₂ Saved", f"{int(total_waste*0.4)} kg")
    col4.metric("🚛 Active Zones", len(df["Area"].unique()) if len(df)>0 else 0)

    st.divider()

    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗑 Report Waste",
        "📷 Upload Waste",
        "📊 Dashboard",
        "🤖 AI Assistant"
    ])

    # ---------------- REPORT ----------------
    with tab1:

        st.subheader("🗑 Report Waste")

        area = st.text_input("Area Name")
        waste_type = st.selectbox(
            "Waste Type",
            ["Organic","Plastic","Metal","Paper","Glass"]
        )
        weight = st.number_input("Weight (kg)", min_value=0.0)

        lat = st.number_input("Latitude")
        lon = st.number_input("Longitude")

        if st.button("Submit Report 🚀"):

            new = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Area": area,
                "Waste_Type": waste_type,
                "Weight_kg": weight,
                "Status": "Pending",
                "Latitude": lat,
                "Longitude": lon
            }])

            df = pd.concat([df, new], ignore_index=True)
            save_data(df)

            st.session_state.points += 15

            st.success("🎉 Report Added Successfully!")
            st.toast("🌱 Eco Points +15", icon="🏆")
            st.balloons()

    # ---------------- UPLOAD ----------------
    with tab2:

        st.subheader("📷 Upload Waste Image")

        file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

        if file:

            path = os.path.join(UPLOAD_DIR, file.name)

            with open(path, "wb") as f:
                f.write(file.getbuffer())

            st.image(file, caption="Uploaded Waste Image")
            st.success("Uploaded Successfully")
            st.toast("📷 Nice Work!", icon="✨")

    # ---------------- DASHBOARD ----------------
    with tab3:

        st.subheader("📊 Smart Analytics Dashboard")

        if len(df) > 0:

            st.dataframe(df)

            st.bar_chart(df.groupby("Area")["Weight_kg"].sum())
            st.bar_chart(df.groupby("Waste_Type")["Weight_kg"].sum())
            st.bar_chart(df["Status"].value_counts())

            map_df = df.rename(columns={"Latitude":"lat","Longitude":"lon"})
            st.map(map_df[["lat","lon"]])

            if df["Weight_kg"].max() > 100:
                st.warning("⚠️ High Waste Zone Detected!")
                st.toast("🚨 Alert!", icon="⚠️")

        else:
            st.info("No data yet")

    # ---------------- AI ASSISTANT ----------------
    with tab4:

        st.subheader("🤖 Eco AI Assistant")

        q = st.text_input("Ask anything about waste data")

        if q:

            if "total" in q.lower():
                st.success(f"Total Waste: {df['Weight_kg'].sum()} kg")

            elif "plastic" in q.lower():
                val = df[df["Waste_Type"]=="Plastic"]["Weight_kg"].sum()
                st.success(f"Plastic Waste: {val} kg")

            elif "most" in q.lower():
                area = df.groupby("Area")["Weight_kg"].sum().idxmax()
                st.success(f"Highest Waste Area: {area}")

            elif "status" in q.lower():
                st.write(df["Status"].value_counts())

            else:
                tips = [
                    "🌱 Keep Earth Clean!",
                    "♻️ Recycle Daily!",
                    "🌍 Reduce Plastic Usage!",
                    "🚛 Smart Waste = Smart City!"
                ]
                st.info(random.choice(tips))

    st.divider()

    # ---------------- FOOTER ----------------
    st.success("🌍 Keep Saving Earth | Eco Hero System")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
