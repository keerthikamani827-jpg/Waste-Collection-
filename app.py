import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="AI Smart Waste Collection", page_icon="♻️", layout="wide")

st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#e8fff1,#f5f0ff);
}
.eco-card{
    padding:15px;border-radius:15px;
    background:#ffffff;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
}
.bounce {
  animation: bounce 2s infinite;
}
@keyframes bounce {
  0%,20%,50%,80%,100% {transform: translateY(0);}
  40% {transform: translateY(-10px);}
  60% {transform: translateY(-5px);}
}
</style>
""", unsafe_allow_html=True)

DATA_FILE = "data.csv"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "points" not in st.session_state:
    st.session_state.points = 250

if not st.session_state.logged_in:

    st.markdown("<h1 class='bounce'>♻️ AI Smart Waste Collection</h1>", unsafe_allow_html=True)
    st.subheader("Smart Waste Management System 🌍")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Please enter username and password")

else:

    st.title("📊 AI Smart Waste Dashboard")
    st.success(f"Welcome {st.session_state.username} 🌱")

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=[
            "Date","Area","Waste_Type","Weight_kg","Collection_Status"
        ])

    total_waste = df["Weight_kg"].sum() if len(df) else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("♻️ Waste Collected", f"{total_waste} kg")
    c2.metric("🚛 Active Trucks", "12")
    c3.metric("🌱 CO₂ Saved", f"{int(total_waste*0.4)} kg")
    c4.metric("🏆 Eco Points", st.session_state.points)

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🗑 Report Waste",
        "📷 Upload Image",
        "🚛 Update Status",
        "📊 Analytics"
    ])

    with tab1:
        st.subheader("🗑 Report New Waste")

        area = st.text_input("Area")
        waste_type = st.selectbox(
            "Waste Type",
            ["Organic","Plastic","Metal","Paper","Glass"]
        )
        weight = st.number_input("Weight (kg)", min_value=0)

        if st.button("Submit Waste Report"):
            new_row = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Area": area,
                "Waste_Type": waste_type,
                "Weight_kg": weight,
                "Collection_Status": "Pending"
            }])

            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.session_state.points += 10

            st.success("🎉 Yay! Waste Report Submitted Successfully!")
            st.balloons()

    with tab2:
        st.subheader("📷 Upload Waste Image")

        image = st.file_uploader(
            "Choose Image",
            type=["jpg","jpeg","png"]
        )

        if image is not None:

            file_path = os.path.join(UPLOAD_DIR, image.name)

            with open(file_path, "wb") as f:
                f.write(image.getbuffer())

            st.image(image, width=300)
            st.success("🌟 Image Uploaded Successfully!")

    with tab3:
        st.subheader("🚛 Update Collection Status")

        if len(df):

            area_update = st.selectbox(
                "Select Area",
                df["Area"].unique()
            )

            status = st.selectbox(
                "Status",
                ["Collected","Pending"]
            )

            if st.button("Update Status"):
                df.loc[df["Area"] == area_update,
                       "Collection_Status"] = status

                df.to_csv(DATA_FILE, index=False)

                st.success(f"✅ {area_update} updated to {status}")

        else:
            st.info("No data available")

    with tab4:
        st.subheader("📊 Analytics Dashboard")

        if len(df):

            st.dataframe(df)

            area_chart = df.groupby("Area")["Weight_kg"].sum()
            st.bar_chart(area_chart)

            waste_chart = df.groupby("Waste_Type")["Weight_kg"].sum()
            st.bar_chart(waste_chart)

            status_counts = df["Collection_Status"].value_counts()
            st.bar_chart(status_counts)

            high_waste = df["Weight_kg"].max()

            if high_waste > 100:
                st.warning(
                    "⚠️ Smart Alert: High Waste Detected!"
                )

        else:
            st.info("Upload or add data to view analytics")

    st.divider()

    st.subheader("🏆 Eco Rewards")

    st.progress(min(st.session_state.points / 500, 1.0))
    st.write(f"Eco Points: {st.session_state.points}/500")

    if st.session_state.points >= 300:
        st.success("🥇 Green Hero Badge Unlocked!")

    tips = [
        "🌍 Recycling helps save energy.",
        "♻️ Separate waste before disposal.",
        "🌱 Organic waste can become compost.",
        "✨ Small actions create a cleaner city."
    ]
        import random
    st.info(random.choice(tips))

    st.divider()

    st.subheader("🤖 AI Waste Assistant")

    question = st.text_input("Ask something about waste data")

    if question:

        if len(df) == 0:
            st.warning("No waste data available.")

        elif "most waste" in question.lower():

            max_area = df.groupby("Area")["Weight_kg"].sum().idxmax()
            max_weight = df.groupby("Area")["Weight_kg"].sum().max()

            st.success(
                f"📍 {max_area} generated the highest waste ({max_weight} kg)"
            )

        elif "pending" in question.lower():

            pending = df[df["Collection_Status"] == "Pending"]

            if len(pending) > 0:
                st.success("🚛 Pending Collection Areas")
                st.write(list(pending["Area"].unique()))
            else:
                st.success("✅ No pending collections")

        elif "plastic" in question.lower():

            plastic = df[df["Waste_Type"] == "Plastic"]["Weight_kg"].sum()

            st.success(
                f"♻️ Total Plastic Waste: {plastic} kg"
            )

        elif "organic" in question.lower():

            organic = df[df["Waste_Type"] == "Organic"]["Weight_kg"].sum()

            st.success(
                f"🌱 Total Organic Waste: {organic} kg"
            )

        elif "total waste" in question.lower():

            total = df["Weight_kg"].sum()

            st.success(
                f"🗑 Total Waste Collected: {total} kg"
            )

        else:
            st.info(
                "Try asking: most waste, pending collection, plastic waste, organic waste, or total waste."
            )

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

