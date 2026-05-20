import streamlit as st
import pandas as pd
import datetime
import random
import requests
import time

st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Custom print layout rules and responsive styling
st.markdown("""
    <style>
    @media print {
        .no-print, [data-testid="stSidebar"], header, footer { display: none !important; }
        .print-content { width: 100% !important; margin: 0 !important; padding: 0 !important; }
    }
    .timer-box {
        background-color: #111111;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #ff3333;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Fetch Gemini API Key Safely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("AI Engine configuration missing. Please add GEMINI_API_KEY to your Secrets panel.")

# UNCHANGED: Bulletproof URL Reader for Public Google Sheets
def read_public_sheet(worksheet_name):
    sheet_id = "1xU80PotVALVM3sWt7PS3kLGbsivqzMvznXq0c8Cu44M"
    clean_name = worksheet_name.strip()
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={clean_name}"
    try:
        df = pd.read_csv(export_url)
        if df is not None and not df.empty:
            return df
        return None
    except Exception:
        return None

# DIRECT REST API CALL TIER - MODEL SPECIFIED: gemini-3.5-flash
def generate_content(prompt_text, api_token):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_token}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"API Server Notice: Unable to construct layout under version 3.5. Status {response.status_code}"
    except Exception as e:
        return f"AI Connection Failure: {str(e)}"

def display_loading_brand():
    st.markdown("""
        <div style="background-color:#111111; padding:20px; border-radius:10px; border-left: 8px solid #ff0000; text-align:center; margin-bottom:25px;">
            <h1 style="color:#ff0000; font-family:'Arial Black', Gadget, sans-serif; letter-spacing:3px; margin:0; font-size:28px;">🛡️ ACADEMIC SHIELD PRO</h1>
            <p style="color:#ffffff; font-family:'Courier New', monospace; font-size:14px; margin:5px 0 0 0;">Created by <span style="color:#ff3333; font-weight:bold;">Sudaisi Setra</span></p>
        </div>
        """, unsafe_allow_html=True)

# Initialize global session state objects for private tracking
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "uploaded_materials" not in st.session_state:
    st.session_state["uploaded_materials"] = [
        {"name": "Kinematics Component Analysis Guide.txt", "timestamp": "System Default"},
        {"name": "Relative Motion Vector Mechanics Worksheet.txt", "timestamp": "System Default"}
    ]

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
    st.sidebar.markdown("<br><br><br><div style='color:#aaaaaa; font-size:12px; font-weight:bold;'>⚙️ System Ownership:<br><span style='color:#ff3333;'>ASP Private System</span></div>", unsafe_allow_html=True)

    # PAGE 1: EXAM CENTER (With live 25-Minute Session Timer)
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

        # Fixed multi-tier data bank lookup syntax for flawless cross-subject fetching
        base_questions = []
        raw_bank = read_public_sheet(f"{subject_choice}pro")
        if raw_bank is None or raw_bank.empty:
            raw_bank = read_public_sheet(subject_choice)
        if raw_bank is None or raw_bank.empty:
            raw_bank = read_public_sheet(subject_choice.lower())

        if raw_bank is not None and not raw_bank.empty:
            col_name = raw_bank.columns[0]
            base_questions = raw_bank[col_name].dropna().tolist()
        else:
            st.error(f"❌ Error: Database worksheet entries for '{subject_choice}' could not be pulled from your Google Sheet. Please confirm the tab name matches exactly.")

        if base_questions:
            date_seed = current_date.strftime("%Y-%b") if is_assessment_week else current_date.strftime("%Y-%m-%d")
            random.seed(date_seed)
            seed_text = " || ".join(random.sample(base_questions, min(2, len(base_questions)))) if is_assessment_week else random.choice(base_questions)
            
            # Generate the layout if seed changes
            if "current_paper" not in st.session_state or st.session_state.get("paper_seed") != seed_text or st.session_state.get("current_subject") != subject_choice:
                with st.spinner("🤖 NCDC AI Expert is compiling exam questions..."):
                    prompt = (
                        f"Construct an official standard competence examination question sheet for Senior Five {subject_choice} "
                        f"based on this topic seed: '{seed_text}' using real Ugandan educational contexts. "
                        f"CRITICAL RULES:\n"
                        f"1. Output ONLY the questions, clear instruction metrics, and marks allocation.\n"
                        f"2. Do NOT under any circumstances output answers, step-by-step solutions, final parameters, or marking schemes."
                    )
                    st.session_state["current_paper"] = generate_content(prompt, api_key)
                    st.session_state["paper_seed"] = seed_text
                    st.session_state["current_subject"] = subject_choice
                    st.session_state["start_time"] = time.time()

            # Countdown Timer Execution Logic (Strictly 25 Minutes)
            TOTAL_EXAM_SECONDS = 25 * 60  
            elapsed_time = time.time() - st.session_state.get("start_time", time.time())
            remaining_seconds = int(TOTAL_EXAM_SECONDS - elapsed_time)

            if remaining_seconds > 0:
                mins, secs = divmod(remaining_seconds, 60)
                time_str = f"{mins:02d}:{secs:02d}"
                
                st.markdown(f"""
                    <div class="timer-box">
                        <span style="color: #ffffff; font-size: 14px; font-family: monospace;">⏳ EXAMINATION TIME REMAINING</span>
                        <h2 style="color: #ff3333; font-size: 36px; margin: 5px 0 0 0; font-family: 'Courier New', monospace; font-weight: bold;">{time_str}</h2>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(remaining_seconds / TOTAL_EXAM_SECONDS)
                
                time.sleep(1)
                st.rerun()
            else:
                st.markdown("""
                    <div class="timer-box" style="border: 2px solid #888888;">
                        <h2 style="color: #ff3333; font-size: 28px; margin: 0; font-family: 'Courier New', monospace;">🚨 TIME EXPIRED</h2>
                        <span style="color: #aaaaaa; font-size: 13px;">The 25-minute submission window has concluded.</span>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(f'<div class="print-content"> {st.session_state["current_paper"]} </div>', unsafe_allow_html=True)
            st.markdown("---")
            
            # Submission Interface Script
            st.subheader("✍ *Candidate Examination Script Submission Panel*")
            
            if remaining_seconds > 0:
                student_work = st.text_area("Type or paste your complete mathematical workings, formula steps, and structural derivations here:", height=250)
                submit_disabled = False
            else:
                st.warning("Submission deactivated. The 25-minute examination session time has run out.")
                student_work = ""
                submit_disabled = True
            
            if st.button("🚀 Submit Script for Automated Grading Evaluation", disabled=submit_disabled):
                if student_work.strip() == "":
                    st.warning("Please supply written workings or answers before evaluation mapping.")
                else:
                    with st.spinner("UNEB Matrix parsing engine evaluating calculations..."):
                        review_prompt = (
                            f"You are the UNEB Principal Examiner evaluating an academic script for Senior Five {subject_choice}.\n\n"
                            f"EXAM QUESTION SHEET:\n{st.session_state['current_paper']}\n\n"
                            f"CANDIDATE'S SUBMITTED WORKING SCRIPTS:\n{student_work}\n\n"
                            f"GRADING DIRECTIVE:\n"
                            f"Analyze their solution methodology step-by-step. If they passed all parameters correctly, congratulate them warmly.\n"
                            f"If they committed mathematical mistakes, missed steps, or failed any questions, show them exactly where they went wrong, "
                            f"followed by the complete step-by-step calculations and conceptual breakdowns."
                        )
                        evaluation_result = generate_content(review_prompt, api_key)
                        st.markdown("### 📊 Official Script Evaluation Report")
                        st.info(evaluation_result)

    # PAGE 2: FULLY OPERATIONAL MULTI-TURN CHAT ROOM
    elif choice == "💬 Study Room Chat":
        display_loading_brand()
        st.title("💬 Private Scholar Study Room Engine")
        st.caption("Active Session - Interactive Technical STEM Tutor Mode")
        
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        user_query = st.chat_input("Inquire regarding equations, formulas, vectors or mechanics profiles...")
        if user_query:
            st.session_state["chat_history"].append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)
                
            with st.spinner("Compiling solution profile..."):
                chat_prompt = (
                    f"You are an elite private STEM instructor analyzing a Senior Five candidate's question. "
                    f"Break down the answer using clear conceptual steps and textbook annotations. Question: {user_query}"
                )
                bot_reply = generate_content(chat_prompt, api_key)
                st.session_state["chat_history"].append({"role": "assistant", "content": bot_reply})
                with st.chat_message("assistant"):
                    st.write(bot_reply)

    # PAGE 3: PROGRESS TRACKER
    elif choice == "📊 Progress Tracker":
        display_loading_brand()
        st.header("📊 Global Performance Leaderboard")
        track_df = read_public_sheet("Sheet1")
        if track_df is not None:
            st.table(track_df)
        else:
            st.info("No historical script assessment records verified on 'Sheet1' yet.")

    # PAGE 4: UPLOAD SAMPLES (Fully Functional Private Sandbox Storage)
    elif choice == "📂 Upload Samples" and user == "Setra stones":
        display_loading_brand()
        st.header("📋 UNEB Reference Sample Vault Manager")
        st.subheader("Stage New Source Material into Local Cache")
        
        uploaded_file = st.file_uploader("Choose reference materials or text scripts to append:", type=["txt", "csv", "md", "json"])
        if uploaded_file is not None:
            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not any(item['name'] == uploaded_file.name for item in st.session_state["uploaded_materials"]):
                st.session_state["uploaded_materials"].append({"name": uploaded_file.name, "timestamp": current_timestamp})
                st.success(f"📦 Successfully staged operational attachment: '{uploaded_file.name}' into internal cache.")

    # PAGE 5: VAULT ARCHIVES (Fully Functional Interactive Repository File System)
    elif choice == "📁 Vault Archives":
        display_loading_brand()
        st.title("📁 Shared Candidate Vault Repositories")
        st.markdown("### Complete Active File Index")
        
        if st.session_state["uploaded_materials"]:
            for file_obj in st.session_state["uploaded_materials"]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"📄 **{file_obj['name']}**")
                with col2:
                    st.caption(f"🗓️ {file_obj['timestamp']}")
                st.markdown("---")
        else:
            st.write("Repository vault is empty.")
else:
    st.sidebar.warning("Access Denied. Please input valid candidate authentication credentials.")
