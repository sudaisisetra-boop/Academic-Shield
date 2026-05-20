import streamlit as st
import pandas as pd
import datetime
import random
import base64
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
from PIL import Image
import io

st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Injection of Clean CSS for Print Optimization
st.markdown("""
    <style>
    @media print {
        .no-print, [data-testid="stSidebar"], header, footer { display: none !important; }
        .print-content { width: 100% !important; margin: 0 !important; padding: 0 !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize AI Brain
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("AI Engine configuration missing. Please add GEMINI_API_KEY to your Secrets panel.")

# Database Connection (Forced live synchronization)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database connection failed. Check your Secrets formatting.")

# Animated/Colorful Dynamic Loading Matrix Header Function
def display_loading_brand():
    st.markdown("""
        <div style="background-color:#111111; padding:20px; border-radius:10px; border-left: 8px solid #ff0000; text-align:center; margin-bottom:25px;">
            <h1 style="color:#ff0000; font-family:'Arial Black', Gadget, sans-serif; letter-spacing:3px; margin:0; font-size:28px;">🛡️ ACADEMIC SHIELD PRO</h1>
            <p style="color:#ffffff; font-family:'Courier New', monospace; font-size:14px; margin:5px 0 0 0;">Created by <span style="color:#ff3333; font-weight:bold;">Sudaisi Setra</span></p>
        </div>
        """, unsafe_allow_html=True)

# Login System with Separated Credentials
st.sidebar.title("🔐 Scholar Login")
user = st.sidebar.selectbox("Select Name", ["Setra stones", "Gideon Cheps"])
pwd = st.sidebar.text_input("Enter Access Code", type="password")

# Password Matching Logic
authenticated = False
if user == "Setra stones" and pwd == "Amazima2026":
    authenticated = True
elif user == "Gideon Cheps" and pwd == "Gideon2026":
    authenticated = True

if authenticated:
    st.sidebar.success(f"Welcome, {user}")
    st.sidebar.markdown("---")
    
    subject_choice = st.sidebar.selectbox("📚 Choose Subject", ["Physics", "Mathematics", "Chemistry"])
    
    # Restrict "Upload Samples" page to Sudaisi Setra only (Managing Authority Guard)
    if user == "Setra stones":
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📂 Upload Samples", "📁 Vault Archives"]
    else:
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📁 Vault Archives"]
        
    choice = st.sidebar.radio("Navigate Pages", menu)
    st.sidebar.markdown("<br><br><br><div style='color:#aaaaaa; font-size:12px; font-weight:bold;'>⚙️ System Ownership:<br><span style='color:#ff3333;'>ASP by Sudaisi Setra</span></div>", unsafe_allow_html=True)

    # LIVE NOTIFICATION BANNER ENGINE
    try:
        notify_df = conn.read(worksheet="ChatLog", ttl=0)
        if not notify_df.empty:
            last_row = notify_df.iloc[-1]
            if last_row["Sender"] != user:
                st.toast(f"💬 New Alert from {last_row['Sender']}: {str(last_row['Text'])[:40]}...", icon="🔔")
    except Exception:
        pass

    # PAGE 1: EXAM CENTER
    if choice == "📝 Exam Center":
        display_loading_brand()
        
        current_date = datetime.date.today()
        week_number = current_date.isocalendar()[1]
        is_assessment_week = (week_number % 2 == 0)
        
        if is_assessment_week:
            st.title(f"🏆 Official Bi-Weekly 4-Item UNEB Standard Exam")
            st.markdown("<p style='color:#ff3333; font-weight:bold;'>⚠️ EXAMINATION NOTICE: This is a synchronized compulsory assessment fortnight.</p>", unsafe_allow_html=True)
        else:
            st.title(f"🏛️ UNEB S5 {subject_choice} Competence Portal")
            st.caption(f"📅 Daily Training Session: **{current_date.strftime('%Y-%m-%d')}**")

        try:
            raw_bank = conn.read(worksheet=subject_choice, ttl=0)
            base_questions = raw_bank['question_text'].dropna().tolist()
        except Exception:
            st.error(f"Could not read from the '{subject_choice}' worksheet repository.")
            base_questions = []

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
                    prompt = f"Construct an official standard competence examination paper for Senior Five {subject} based on: '{seed_source}'. Must have exactly FOUR compulsory items matching NCDC standards."
                else:
                    prompt = f"You are a UNEB examiner. Take this scenario: '{seed_source}'. Generate exactly TWO distinct, parallel competence-based questions for S5 {subject} using a real Ugandan context."
                response = model.generate_content(prompt)
                return response.text

            with st.spinner("🤖 NCDC AI Expert is compiling the master exam paper layout..."):
                active_paper_text = generate_ncdc_competence_paper(seed_text, subject_choice, date_seed, is_assessment_week)
            
            st.markdown("---")
            col_left, col_right = st.columns([4, 1])
            with col_right:
                st.markdown('<button onclick="window.print()" style="background-color:#ff3333; color:white; border:none; padding:10px 18px; border-radius:5px; font-weight:bold; width:100%; cursor:pointer;">🖨️ Print Exam Sheet</button>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="print-content"> {active_paper_text} </div>', unsafe_allow_html=True)
            st.markdown("---")
            
            st.subheader("✍️ Your Examination Submission Script")
            input_mode = st.radio("Choose execution submission mode:", ["📷 Upload Photo of Handwritten Work", "⌨️ Type My Answers"])
            
            uploaded_photo = None
            if input_mode == "📷 Upload Photo of Handwritten Work":
                uploaded_photo = st.file_uploader("Snap or upload your answer script sheets here:", type=["jpg", "jpeg", "png"])
                if uploaded_photo:
                    st.image(uploaded_photo, width=300, caption="Submission Preview")

            if st.button("📤 Submit Competence Script to Cloud Vault"):
                with st.spinner("📝 Saving permanently to Google Sheet & evaluating performance..."):
                    encoded_img = ""
                    if uploaded_photo is not None:
                        encoded_img = base64.b64encode(uploaded_photo.read()).decode("utf-8")
                        
                        # Write image permanently to Google Sheet ScriptVault tab
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

                    st.success("Script securely archived forever in your personal cloud repository!")
        else:
            st.warning(f"Your '{subject_choice}' question repository is empty.")

    # PAGE 2: MULTIMEDIA STUDY ROOM CHAT
    elif choice == "💬 Study Room Chat":
        display_loading_brand()
        st.title("💬 Real-Time Scholar Study Room")
        
        try: chat_df = conn.read(worksheet="ChatLog", ttl=0)
        except Exception: chat_df = pd.DataFrame(columns=["Timestamp", "Sender", "Text", "MediaType", "MediaData", "FileName"])

        for idx, row in chat_df.tail(25).iterrows():
            with st.chat_message("user" if row["Sender"] == user else "assistant"):
                st.markdown(f"**{row['Sender']}** <span style='font-size:11px; color:gray;'>({row['Timestamp']})</span>", unsafe_allow_html=True)
                if pd.notna(row["Text"]) and str(row["Text"]).strip() != "": st.write(row["Text"])
                if pd.notna(row["MediaType"]) and pd.notna(row["MediaData"]):
                    m_data = base64.b64decode(row["MediaData"])
                    if row["MediaType"] == "Image": st.image(m_data, width=300)
                    elif row["MediaType"] == "Audio": st.audio(m_data)
                    elif row["MediaType"] == "Video": st.video(m_data)
                    elif row["MediaType"] == "Document": st.download_button(f"📥 Download {row['FileName']}", m_data, file_name=row['FileName'])

        with st.form("chat_form", clear_on_submit=True):
            msg_text = st.text_input("Type text or insert emojis here...")
            attached_file = st.file_uploader("Upload media attachment", type=["jpg", "jpeg", "png", "mp3", "wav", "m4a", "mp4", "pdf", "docx", "txt"])
            submit_msg = st.form_submit_button("🚀 Send Message")
            
            if submit_msg:
                if msg_text.strip() != "" or attached_file is not None:
                    timestamp_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    media_type, encoded_string, filename = "None", "", ""
                    if attached_file is not None:
                        filename = attached_file.name
                        file_ext = filename.split(".")[-1].lower()
                        encoded_string = base64.b64encode(attached_file.read()).decode("utf-8")
                        if file_ext in ["jpg", "jpeg", "png"]: media_type = "Image"
                        elif file_ext in ["mp3", "wav", "m4a"]: media_type = "Audio"
                        elif file_ext in ["mp4"]: media_type = "Video"
                        else: media_type = "Document"
                    
                    new_msg = pd.DataFrame([{"Timestamp": timestamp_now, "Sender": user, "Text": msg_text, "MediaType": media_type, "MediaData": encoded_string, "FileName": filename}])
                    try:
                        conn.update(worksheet="ChatLog", data=pd.concat([chat_df, new_msg], ignore_index=True))
                        st.rerun()
                    except Exception: pass

    # PAGE 3: PROGRESS TRACKER
    elif choice == "📊 Progress Tracker":
        display_loading_brand()
        st.header("📊 Global Leaderboard")
        try: st.table(conn.read(worksheet="Sheet1", ttl=0))
        except Exception: st.write("No entries recorded yet.")

    # PAGE 4: UPLOAD SAMPLES (Admin Only Page - Fixed to Save Permanently to Cloud)
    elif choice == "📂 Upload Samples" and user == "Setra stones":
        display_loading_brand()
        st.header("📋 UNEB Reference Sample Vault")
        sample_file = st.file_uploader("Upload reference visual or past paper layout:", type=["jpg", "jpeg", "png"])
        
        if sample_file:
            with st.spinner("Locking file into secure cloud drive storage..."):
                encoded_sample = base64.b64encode(sample_file.read()).decode("utf-8")
                try:
                    sample_df = conn.read(worksheet="SampleVault", ttl=0)
                except Exception:
                    sample_df = pd.DataFrame(columns=["Subject", "FileName", "ImageData"])
                
                new_sample_row = pd.DataFrame([{"Subject": subject_choice, "FileName": sample_file.name, "ImageData": encoded_sample}])
                conn.update(worksheet="SampleVault", data=pd.concat([sample_df, new_sample_row], ignore_index=True))
                st.success(f"📎 Reference item '{sample_file.name}' is now locked in cloud memory forever!")

    # PAGE 5: VAULT ARCHIVES (Forced to load directly out of Cloud Sheet data strings)
    elif choice == "📁 Vault Archives":
        display_loading_brand()
        st.title("📁 Shared Candidate Vault Archives")
        
        view_mode = st.selectbox("Filter Vault Files By Type", ["Show Exam Script Submissions", "Show Uploaded Reference Sample Papers"])
        
        if view_mode == "Show Exam Script Submissions":
            try:
                scripts = conn.read(worksheet="ScriptVault", ttl=0)
                if not scripts.empty:
                    for idx, row in scripts.iterrows():
                        st.markdown(f"**📝 Candidate Script:** `{row['Student']}` | **Subject:** `{row['Subject']}` | **Cycle:** `{row['Date']}`")
                        st.image(base64.b64decode(row["ImageData"]), width=450)
                        st.markdown("---")
                else:
                    st.info("No exam submissions recorded in the cloud archive yet.")
            except Exception:
                st.info("No submission records found. Ensure your 'ScriptVault' tab is active.")
                
        elif view_mode == "Show Uploaded Reference Sample Papers":
            try:
                samples = conn.read(worksheet="SampleVault", ttl=0)
                if not samples.empty:
                    for idx, row in samples.iterrows():
                        if row["Subject"] == subject_choice:
                            st.markdown(f"**📐 Reference Source:** `{row['FileName']}` | **Subject:** `{row['Subject']}`")
                            st.image(base64.b64decode(row["ImageData"]), width=450)
                            st.markdown("---")
                else:
                    st.info("No sample sheets uploaded for this subject yet.")
            except Exception:
                st.info("No sample records found. Ensure your 'SampleVault' tab is active.")
else:
    st.warning("Please enter your access code in the sidebar.")
