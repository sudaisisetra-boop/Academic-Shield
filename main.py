import streamlit as st
import pandas as pd
import datetime
import random
import base64
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Clean UI and Print CSS Layout Configuration
st.markdown("""
    <style>
    @media print {
        .no-print, [data-testid="stSidebar"], header, footer { display: none !important; }
        .print-content { width: 100% !important; margin: 0 !important; padding: 0 !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize AI Brain Engine
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("AI Engine configuration missing. Please add GEMINI_API_KEY to your Secrets panel.")

# Database Connection (Reads your Service Account Configuration)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database connection failed. Please double check your Secrets formatting.")

# Core Application Header Brand Layout
def display_loading_brand():
    st.markdown("""
        <div style="background-color:#111111; padding:20px; border-radius:10px; border-left: 8px solid #ff0000; text-align:center; margin-bottom:25px;">
            <h1 style="color:#ff0000; font-family:'Arial Black', Gadget, sans-serif; letter-spacing:3px; margin:0; font-size:28px;">🛡️ ACADEMIC SHIELD PRO</h1>
            <p style="color:#ffffff; font-family:'Courier New', monospace; font-size:14px; margin:5px 0 0 0;">Created by <span style="color:#ff3333; font-weight:bold;">Sudaisi Setra</span></p>
        </div>
        """, unsafe_allow_html=True)

# Secure Scholar Login Protocol
st.sidebar.title("🔐 Scholar Login")
user = st.sidebar.selectbox("Select Name", ["Setra stones", "Gideon Cheps"])
pwd = st.sidebar.text_input("Enter Access Code", type="password")

authenticated = False
if user == "Setra stones" and pwd == "Amazima2026":
    authenticated = True
elif user == "Gideon Cheps" and pwd == "Gideon2026":
    authenticated = True

if authenticated:
    st.sidebar.success(f"Welcome, {user}")
    st.sidebar.markdown("---")
    
    subject_choice = st.sidebar.selectbox("📚 Choose Subject", ["Physics", "Mathematics", "Chemistry"])
    
    # Authority Isolation Management Guard (Exclusive Admin Panel)
    if user == "Setra stones":
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📂 Upload Samples", "📁 Vault Archives"]
    else:
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📁 Vault Archives"]
        
    choice = st.sidebar.radio("Navigate Pages", menu)
    st.sidebar.markdown("<br><br><br><div style='color:#aaaaaa; font-size:12px; font-weight:bold;'>⚙️ System Ownership:<br><span style='color:#ff3333;'>ASP by Sudaisi Setra</span></div>", unsafe_allow_html=True)

    # LIVE REAL-TIME CHAT ALERT SYNC
    try:
        notify_df = conn.read(worksheet="ChatLog", ttl=0)
        if not notify_df.empty:
            last_row = notify_df.iloc[-1]
            if last_row["Sender"] != user:
                st.toast(f"💬 New Alert from {last_row['Sender']}: {str(last_row['Text'])[:40]}...", icon="🔔")
    except Exception:
        pass

    # PAGE 1: EXAM CENTER (Strict Worksheet Binding)
    if choice == "📝 Exam Center":
        display_loading_brand()
        
        current_date = datetime.date.today()
        week_number = current_date.isocalendar()[1]
        is_assessment_week = (week_number % 2 == 0)
        
        if is_assessment_week:
            st.title(f"🏆 Official Bi-Weekly 4-Item UNEB Standard Exam")
        else:
            st.title(f"🏛️ UNEB S5 {subject_choice} Competence Portal")
            st.caption(f"📅 Daily Synchronized Training Session: **{current_date.strftime('%Y-%m-%d')}**")

        base_questions = []
        try:
            # Targeted reading by exact subject worksheet name
            raw_bank = conn.read(worksheet=subject_choice, ttl=0)
            if 'question_text' in raw_bank.columns:
                base_questions = raw_bank['question_text'].dropna().tolist()
            else:
                st.error(f"The '{subject_choice}' worksheet tab was found, but row cell A1 must be exactly named 'question_text'.")
        except Exception:
            st.error(f"Could not connect to the '{subject_choice}' worksheet. Confirm that it exists in your Google Sheet.")

        if base_questions:
            date_seed = current_date.strftime("%Y-%b") if is_assessment_week else current_date.strftime("%Y-%m-%d")
            random.seed(date_seed)
            
            if is_assessment_week:
                sample_pool = random.sample(base_questions, min(2, len(base_questions)))
                seed_text = " || ".join(sample_pool)
            else:
                seed_text = random.choice(base_questions)
            
            @st.cache_data(ttl=60)
            def generate_ncdc_competence_paper(seed_source, subject, cycle_key, large_format):
                if large_format:
                    prompt = f"Construct an official standard competence examination paper for Senior Five {subject} based on: '{seed_source}'. Generate 4 detailed compulsory curriculum items matching NCDC Elements of Construct."
                else:
                    prompt = f"Take this reference question scenario: '{seed_source}' and generate exactly two distinct parallel competence-based questions for Senior Five {subject} using a real Ugandan context."
                response = model.generate_content(prompt)
                return response.text

            with st.spinner("🤖 NCDC AI Expert is compiling the exam paper layout..."):
                active_paper_text = generate_ncdc_competence_paper(seed_text, subject_choice, date_seed, is_assessment_week)
            
            st.markdown("---")
            st.markdown(f'<div class="print-content"> {active_paper_text} </div>', unsafe_allow_html=True)
            st.markdown("---")
            
            st.subheader("✍️ Your Examination Submission Script")
            input_mode = st.radio("Choose execution submission mode:", ["📷 Upload Photo of Handwritten Work", "⌨️ Type My Answers"])
            
            uploaded_photo = None
            if input_mode == "📷 Upload Photo of Handwritten Work":
                uploaded_photo = st.file_uploader("Snap or upload your answer script sheets here:", type=["jpg", "jpeg", "png"])

            if st.button("📤 Submit Competence Script to Cloud Vault"):
                with st.spinner("📝 Archiving script file into Cloud Vault..."):
                    encoded_img = ""
                    if uploaded_photo is not None:
                        encoded_img = base64.b64encode(uploaded_photo.read()).decode("utf-8")
                    
                    try:
                        try:
                            vault_df = conn.read(worksheet="ScriptVault", ttl=0)
                        except Exception:
                            vault_df = pd.DataFrame(columns=["Date", "Student", "Subject", "ImageData"])
                        
                        new_script_row = pd.DataFrame([{
                            "Date": date_seed,
                            "Student": user,
                            "Subject": subject_choice,
                            "ImageData": encoded_img
                        }])
                        conn.update(worksheet="ScriptVault", data=pd.concat([vault_df, new_script_row], ignore_index=True))
                        st.success("Script securely archived forever in your cloud repository!")
                    except Exception:
                        st.error("Storage Sync Error: Please verify that row 1 of your 'ScriptVault' tab has headers: Date, Student, Subject, ImageData.")
        else:
            st.warning(f"Awaiting question banking strings. Please ensure rows exist under the 'question_text' column inside your '{subject_choice}' worksheet tab.")

    # PAGE 2: MULTIMEDIA STUDY ROOM CHAT (Strict Tab Binding)
    elif choice == "💬 Study Room Chat":
        display_loading_brand()
        st.title("💬 Real-Time Scholar Study Room")
        
        try: 
            chat_df = conn.read(worksheet="ChatLog", ttl=0)
        except Exception: 
            chat_df = pd.DataFrame(columns=["Timestamp", "Sender", "Text", "MediaType", "MediaData", "FileName"])

        for idx, row in chat_df.tail(25).iterrows():
            with st.chat_message("user" if row["Sender"] == user else "assistant"):
                st.markdown(f"**{row['Sender']}** <span style='font-size:11px; color:gray;'>({row['Timestamp']})</span>", unsafe_allow_html=True)
                if pd.notna(row["Text"]) and str(row["Text"]).strip() != "": st.write(row["Text"])
                if pd.notna(row["MediaType"]) and pd.notna(row["MediaData"]) and str(row["MediaData"]).strip() != "":
                    try:
                        m_data = base64.b64decode(row["MediaData"])
                        if row["MediaType"] == "Image": st.image(m_data, width=300)
                        elif row["MediaType"] == "Audio": st.audio(m_data)
                        elif row["MediaType"] == "Video": st.video(m_data)
                    except Exception:
                        pass
        st.markdown("---")

        with st.form("chat_form", clear_on_submit=True):
            msg_text = st.text_input("Type text or insert emojis here...")
            attached_file = st.file_uploader("Upload media attachment", type=["jpg", "jpeg", "png"])
            submit_msg = st.form_submit_button("🚀 Send Message")
            
            if submit_msg:
                if msg_text.strip() != "" or attached_file is not None:
                    timestamp_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    media_type, encoded_string, filename = "None", "", ""
                    if attached_file is not None:
                        filename = attached_file.name
                        encoded_string = base64.b64encode(attached_file.read()).decode("utf-8")
                        media_type = "Image"
                    
                    new_msg = pd.DataFrame([{"Timestamp": timestamp_now, "Sender": user, "Text": msg_text, "MediaType": media_type, "MediaData": encoded_string, "FileName": filename}])
                    try:
                        conn.update(worksheet="ChatLog", data=pd.concat([chat_df, new_msg], ignore_index=True))
                        st.rerun()
                    except Exception: 
                        st.error("Message sync dropped. Ensure 'ChatLog' tab has headers: Timestamp, Sender, Text, MediaType, MediaData, FileName")

    # PAGE 3: PROGRESS TRACKER (Locked explicitly to 'Sheet1')
    elif choice == "📊 Progress Tracker":
        display_loading_brand()
        st.header("📊 Global Leaderboard")
        try: 
            # Explicit worksheet call prevents pulling from default first tab
            st.table(conn.read(worksheet="Sheet1", ttl=0))
        except Exception: 
            st.write("No historical script grades recorded on 'Sheet1' yet.")

    # PAGE 4: UPLOAD SAMPLES (Admin Restricted - Locked to 'SampleVault')
    elif choice == "📂 Upload Samples" and user == "Setra stones":
        display_loading_brand()
        st.header("📋 UNEB Reference Sample Vault")
        sample_file = st.file_uploader("Upload reference visual or past paper layout:", type=["jpg", "jpeg", "png"])
        
        if sample_file:
            if st.button("💾 Confirm Permanent Save to Cloud Vault"):
                with st.spinner("Locking resource string into SampleVault worksheet..."):
                    encoded_sample = base64.b64encode(sample_file.read()).decode("utf-8")
                    try:
                        try:
                            sample_df = conn.read(worksheet="SampleVault", ttl=0)
                        except Exception:
                            sample_df = pd.DataFrame(columns=["Subject", "FileName", "ImageData"])
                        
                        new_sample_row = pd.DataFrame([{"Subject": subject_choice, "FileName": sample_file.name, "ImageData": encoded_sample}])
                        conn.update(worksheet="SampleVault", data=pd.concat([sample_df, new_sample_row], ignore_index=True))
                        st.success(f"📎 Reference item '{sample_file.name}' saved to cloud memory successfully!")
                    except Exception:
                        st.error("Upload aborted. Confirm that row 1 of your 'SampleVault' tab contains headers: Subject, FileName, ImageData.")

    # PAGE 5: VAULT ARCHIVES (Strict Workspace Content Resolution)
    elif choice == "📁 Vault Archives":
        display_loading_brand()
        st.title("📁 Shared Candidate Vault Archives")
        view_mode = st.selectbox("Filter Vault Files By Type", ["Show Exam Script Submissions", "Show Uploaded Reference Sample Papers"])
        
        if view_mode == "Show Exam Script Submissions":
            try:
                scripts = conn.read(worksheet="ScriptVault", ttl=0)
                if not scripts.empty:
                    for idx, row in scripts.iterrows():
                        if pd.notna(row["ImageData"]) and str(row["ImageData"]).strip() != "":
                            st.markdown(f"**📝 Candidate Script:** `{row['Student']}` | **Subject:** `{row['Subject']}`")
                            st.image(base64.b64decode(row["ImageData"]), width=450)
                            st.markdown("---")
                else:
                    st.info("No candidate scripts uploaded to this archive tab yet.")
            except Exception:
                st.info("No submission records found inside 'ScriptVault'.")
                
        elif view_mode == "Show Uploaded Reference Sample Papers":
            try:
                samples = conn.read(worksheet="SampleVault", ttl=0)
                if not samples.empty:
                    for idx, row in samples.iterrows():
                        if row["Subject"] == subject_choice and pd.notna(row["ImageData"]) and str(row["ImageData"]).strip() != "":
                            st.markdown(f"**📐 Reference Source:** `{row['FileName']}`")
                            st.image(base64.b64decode(row["ImageData"]), width=450)
                            st.markdown("---")
                else:
                    st.info("No sample sheets uploaded for this subject yet.")
            except Exception:
                st.info("No sample records found inside 'SampleVault'.")
else:
    st.sidebar.warning("Access Denied. Please enter your valid credentials.")
