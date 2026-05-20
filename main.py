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

# Database Connection Engine
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
    target_worksheet = f"{subject_choice}pro"
    
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
            # Public spreadsheet read requires handling header strings cleanly
            raw_bank = conn.read(worksheet=target_worksheet, ttl=0)
            if 'question_text' in raw_bank.columns:
                base_questions = raw_bank['question_text'].dropna().tolist()
            else:
                st.error(f"The '{target_worksheet}' worksheet tab was found, but row cell A1 must be exactly named 'question_text'.")
        except Exception:
            st.error(f"Could not connect to the '{target_worksheet}' worksheet. Verify that your Google Sheet general access is set to 'Anyone with the link' and that your tab names match exactly.")

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
                st.warning("Note: Writing operations are disabled in public connection fallback mode. Please submit your completed handwritten scripts directly to your peer review team.")

    # PAGE 2: MULTIMEDIA STUDY ROOM CHAT
    elif choice == "💬 Study Room Chat":
        display_loading_brand()
        st.title("💬 Real-Time Scholar Study Room")
        st.info("The chat engine is offline during public database maintenance mode.")

    # PAGE 3: PROGRESS TRACKER
    elif choice == "📊 Progress Tracker":
        display_loading_brand()
        st.header("📊 Global Leaderboard")
        try: 
            st.table(conn.read(worksheet="Sheet1", ttl=0))
        except Exception: 
            st.write("No historical script grades recorded on 'Sheet1' yet.")

    # PAGE 4: UPLOAD SAMPLES
    elif choice == "📂 Upload Samples" and user == "Setra stones":
        display_loading_brand()
        st.header("📋 UNEB Reference Sample Vault")
        st.info("Upload operations are paused during public configuration mode.")

    # PAGE 5: VAULT ARCHIVES
    elif choice == "📁 Vault Archives":
        display_loading_brand()
        st.title("📁 Shared Candidate Vault Archives")
        st.info("Vault rendering is temporarily unavailable.")
else:
    st.sidebar.warning("Access Denied. Please enter your valid credentials.")
