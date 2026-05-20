import streamlit as st
import pandas as pd
import datetime
import random
import base64
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

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

# Database Connection Engine with Explicit Fallback configuration rules
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database connection failed. Please double check your Secrets TOML formatting.")

def display_loading_brand():
    st.markdown("""
        <div style="background-color:#111111; padding:20px; border-radius:10px; border-left: 8px solid #ff0000; text-align:center; margin-bottom:25px;">
            <h1 style="color:#ff0000; font-family:'Arial Black', Gadget, sans-serif; letter-spacing:3px; margin:0; font-size:28px;">🛡️ ACADEMIC SHIELD PRO</h1>
            <p style="color:#ffffff; font-family:'Courier New', monospace; font-size:14px; margin:5px 0 0 0;">Created by <span style="color:#ff3333; font-weight:bold;">Sudaisi Setra</span></p>
        </div>
        """, unsafe_allow_html=True)

# Scholar Login Interface
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
    
    if user == "Setra stones":
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📂 Upload Samples", "📁 Vault Archives"]
    else:
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📁 Vault Archives"]
        
    choice = st.sidebar.radio("Navigate Pages", menu)
    st.sidebar.markdown("<br><br><br><div style='color:#aaaaaa; font-size:12px; font-weight:bold;'>⚙️ System Ownership:<br><span style='color:#ff3333;'>ASP by Sudaisi Setra</span></div>", unsafe_allow_html=True)

    # PAGE 1: EXAM CENTER
    if choice == "📝 Exam Center":
        display_loading_brand()
        current_date = datetime.date.today()
        week_number = current_date.isocalendar()[1]
        is_assessment_week = (week_number % 2 == 0)
        
        if is_assessment_week:
            st.title(f"🏆 Official Bi-Weekly 4-Item UNEB Standard Exam")
        else:
            st.title(f"🏛️ UNEB S5 {subject_choice} Competence Portal")
            st.caption(f"📅 Daily Session: **{current_date.strftime('%Y-%m-%d')}**")

        base_questions = []
        try:
            # Force dynamic read with clear cache argument rule mapping
            raw_bank = conn.read(worksheet=subject_choice, ttl="0m")
            if 'question_text' in raw_bank.columns:
                base_questions = raw_bank['question_text'].dropna().tolist()
            else:
                st.error(f"The '{subject_choice}' worksheet tab was found, but row cell A1 must be exactly named 'question_text'.")
        except Exception as e:
            st.error(f"Could not connect to the '{subject_choice}' worksheet. Please select Clear Cache in 'Manage App' to force service account connection update.")

        if base_questions:
            date_seed = current_date.strftime("%Y-%b") if is_assessment_week else current_date.strftime("%Y-%m-%d")
            random.seed(date_seed)
            seed_text = " || ".join(random.sample(base_questions, min(2, len(base_questions)))) if is_assessment_week else random.choice(base_questions)
            
            @st.cache_data(ttl=60)
            def generate_paper(seed_source, subject, cycle_key, large_format):
                prompt = f"Construct an official standard competence examination paper for Senior Five {subject} based on: '{seed_source}' using real Ugandan contexts."
                return model.generate_content(prompt).text

            with st.spinner("🤖 NCDC AI Expert is compiling the exam paper layout..."):
                active_paper_text = generate_paper(seed_text, subject_choice, date_seed, is_assessment_week)
            
            st.markdown("---")
            st.markdown(f'<div class="print-content"> {active_paper_text} </div>', unsafe_allow_html=True)
            st.markdown("---")
            
            st.subheader("✍️ Your Examination Submission Script")
            input_mode = st.radio("Choose execution submission mode:", ["📷 Upload Photo of Handwritten Work", "⌨️ Type My Answers"])
            
            uploaded_photo = None
            if input_mode == "📷 Upload Photo of Handwritten Work":
                uploaded_photo = st.file_uploader("Snap or upload answer script sheets here:", type=["jpg", "jpeg", "png"])

            if st.button("📤 Submit Competence Script to Cloud Vault"):
                with st.spinner("📝 Archiving script file..."):
                    encoded_img = base64.b64encode(uploaded_photo.read()).decode("utf-8") if uploaded_photo else ""
                    try:
                        try:
                            vault_df = conn.read(worksheet="ScriptVault", ttl="0m")
                        except Exception:
                            vault_df = pd.DataFrame(columns=["Date", "Student", "Subject", "ImageData"])
                        
                        new_row = pd.DataFrame([{"Date": date_seed, "Student": user, "Subject": subject_choice, "ImageData": encoded_img}])
                        conn.update(worksheet="ScriptVault", data=pd.concat([vault_df, new_row], ignore_index=True))
                        st.success("Script securely archived in your cloud repository!")
                    except Exception:
                        st.error("Storage Sync Error: Please verify ScriptVault headers or clear system storage cache.")

    # PAGE 2: MULTIMEDIA STUDY ROOM CHAT
    elif choice == "💬 Study Room Chat":
        display_loading_brand()
        st.title("💬 Real-Time Scholar Study Room")
        try: 
            chat_df = conn.read(worksheet="ChatLog", ttl="0m")
        except Exception: 
            chat_df = pd.DataFrame(columns=["Timestamp", "Sender", "Text", "MediaType", "MediaData", "FileName"])

        for idx, row in chat_df.tail(25).iterrows():
            with st.chat_message("user" if row["Sender"] == user else "assistant"):
                st.markdown(f"**{row['Sender']}** <span style='font-size:11px; color:gray;'>({row['Timestamp']})</span>", unsafe_allow_html=True)
                if pd.notna(row["Text"]) and str(row["Text"]).strip() != "": st.write(row["Text"])
                if pd.notna(row["MediaType"]) and pd.notna(row["MediaData"]) and str(row["MediaData"]).strip() != "":
                    try:
                        st.image(base64.b64decode(row["MediaData"]), width=300)
                    except Exception: pass
        st.markdown("---")

        with st.form("chat_form", clear_on_submit=True):
            msg_text = st.text_input("Type text here...")
            attached_file = st.file_uploader("Upload attachment", type=["jpg", "jpeg", "png"])
            submit_msg = st.form_submit_button("🚀 Send Message")
            
            if submit_msg and (msg_text.strip() != "" or attached_file is not None):
                timestamp_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                media_type, encoded_string, filename = ("Image", base64.b64encode(attached_file.read()).decode("utf-8"), attached_file.name) if attached_file else ("None", "", "")
                new_msg = pd.DataFrame([{"Timestamp": timestamp_now, "Sender": user, "Text": msg_text, "MediaType": media_type, "MediaData": encoded_string, "FileName": filename}])
                try:
                    conn.update(worksheet="ChatLog", data=pd.concat([chat_df, new_msg], ignore_index=True))
                    st.rerun()
                except Exception: 
                    st.error("Message sync dropped. Ensure 'ChatLog' tab has headers: Timestamp, Sender, Text, MediaType, MediaData, FileName")

    # PAGE 3: PROGRESS TRACKER
    elif choice == "📊 Progress Tracker":
        display_loading_brand()
        st.header("📊 Global Leaderboard")
        try: 
            st.table(conn.read(worksheet="Sheet1", ttl="0m"))
        except Exception: 
            st.write("No historical script grades recorded on 'Sheet1' yet.")

    # PAGE 4: UPLOAD SAMPLES
    elif choice == "📂 Upload Samples" and user == "Setra stones":
        display_loading_brand()
        st.header("📋 UNEB Reference Sample Vault")
        sample_file = st.file_uploader("Upload past paper layout:", type=["jpg", "jpeg", "png"])
        if sample_file and st.button("💾 Confirm Permanent Save to Cloud Vault"):
            with st.spinner("Locking resource string into SampleVault..."):
                encoded_sample = base64.b64encode(sample_file.read()).decode("utf-8")
                try:
                    try:
                        sample_df = conn.read(worksheet="SampleVault", ttl="0m")
                    except Exception:
                        sample_df = pd.DataFrame(columns=["Subject", "FileName", "ImageData"])
                    new_sample_row = pd.DataFrame([{"Subject": subject_choice, "FileName": sample_file.name, "ImageData": encoded_sample}])
                    conn.update(worksheet="SampleVault", data=pd.concat([sample_df, new_sample_row], ignore_index=True))
                    st.success("Reference item saved to cloud successfully!")
                except Exception:
                    st.error("Upload failed. Make sure your 'SampleVault' tab has 'Subject', 'FileName', and 'ImageData' headers in row 1.")

    # PAGE 5: VAULT ARCHIVES
    elif choice == "📁 Vault Archives":
        display_loading_brand()
        st.title("📁 Shared Candidate Vault Archives")
        view_mode = st.selectbox("Filter Vault Files By Type", ["Show Exam Script Submissions", "Show Uploaded Reference Sample Papers"])
        
        if view_mode == "Show Exam Script Submissions":
            try:
                scripts = conn.read(worksheet="ScriptVault", ttl="0m")
                for idx, row in scripts.iterrows():
                    if pd.notna(row["ImageData"]) and str(row["ImageData"]).strip() != "":
                        st.markdown(f"**📝 Candidate Script:** `{row['Student']}` | **Subject:** `{row['Subject']}`")
                        st.image(base64.b64decode(row["ImageData"]), width=450)
            except Exception: st.info("No records found inside 'ScriptVault'.")
                
        elif view_mode == "Show Uploaded Reference Sample Papers":
            try:
                samples = conn.read(worksheet="SampleVault", ttl="0m")
                for idx, row in samples.iterrows():
                    if row["Subject"] == subject_choice and pd.notna(row["ImageData"]) and str(row["ImageData"]).strip() != "":
                        st.markdown(f"**📐 Reference Source:** `{row['FileName']}`")
                        st.image(base64.b64decode(row["ImageData"]), width=450)
            except Exception: st.info("No records found inside 'SampleVault'.")
else:
    st.sidebar.warning("Access Denied. Please enter your valid credentials.")
# force reload
# Deploy 
