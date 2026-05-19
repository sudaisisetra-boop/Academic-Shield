import streamlit as st
import pandas as pd
import solutions 
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Academic Shield", layout="wide")

# Connect to Google Sheets using the raw secrets block you just saved
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database connection failed. Please verify your Streamlit Secrets panel configuration.")

# Login Sidebar System
st.sidebar.title("🔐 Scholar Login")
user = st.sidebar.selectbox("Select Name", ["Setra stones", "Gideon Cheps"])
pwd = st.sidebar.text_input("Enter Access Code", type="password")

if pwd == "Amazima2026":
    st.sidebar.success(f"Welcome, {user}")
    menu = ["📝 Exam Center", "📊 Progress Tracker", "📂 Upload Samples"]
    choice = st.sidebar.radio("Navigate", menu)

    if choice == "📝 Exam Center":
        st.header("Physics: Bridge Construction Item")
        st.write("**Scenario:** A concrete pillar (200kg) floats with 75% submerged in Fluid A (RD 1.2). A 50N weight is added to keep it at that depth in Fluid B.")
        
        q1 = st.number_input("Q1: Relative Density of Pillar", format="%.2f")
        q2 = st.number_input("Q2: Density of Fluid B (kg/m³)", format="%.1f")
        
        if st.button("Submit Exam"):
            score, feedback = solutions.grade_physics_item1(q1, q2)
            st.info(feedback)
            
            # This is the new cloud-sync engine!
            try:
                # 1. Read what is currently inside Sheet1
                existing_data = conn.read(worksheet="Sheet1")
                # 2. Build a brand new line with your score
                new_row = pd.DataFrame([{"Student": user, "Score": score, "Subject": "Physics"}])
                # 3. Stack the new line right under the old ones
                updated_data = pd.concat([existing_data, new_row], ignore_index=True)
                # 4. Push the whole updated table back to Google Drive
                conn.update(worksheet="Sheet1", data=updated_data)
                st.success("Score logged securely to Google Drive database!")
            except Exception as e:
                st.warning("Score calculated locally, but data tracking sync failed. Ensure your Google Sheet is shared with the bot's email address.")
                
            if score == 100: st.balloons()

    elif choice == "📊 Progress Tracker":
        st.header("Academic Standings (Live Cloud Data)")
        try:
            # Pull down the live table from your Google Sheets app
            df = conn.read(worksheet="Sheet1")
            st.table(df)
        except Exception:
            st.write("No entries recorded in the cloud spreadsheet database yet.")

    elif choice == "📂 Upload Samples":
        st.header("Submit UNEB Papers")
        st.file_uploader("Upload photos for AI analysis")
else:
    st.warning("Please enter the access code.")
