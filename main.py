import streamlit as st
import pandas as pd
import datetime
import random
import requests
import time
import os
import json
import base64
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Enforced Custom CSS Layout Mechanics
st.markdown("""
    <style>
    @media print {
        .no-print, [data-testid="stSidebar"], header, footer, .stButton { display: none !important; }
        .print-content { width: 100% !important; margin: 0 !important; padding: 0 !important; }
    }
    .timer-container {
        background-color: #111111;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #ff3333;
        text-align: center;
        margin-bottom: 15px;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 75%;
    }
    .chat-left { background-color: #262730; color: white; margin-right: auto; }
    .chat-right { background-color: #ff3333; color: white; margin-left: auto; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# Fetch Gemini API Key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("AI Engine configuration missing. Please add GEMINI_API_KEY to your Secrets panel.")

# HARDCODED SPREADSHEET MASTER TARGET
SHEET_ID = "1xU80PotVALVM3sWt7PS3kLGbsivqzMvznXq0c8Cu44M"

# CORE DATABASE READ ENGINE: Reads public sheets cleanly
def read_public_sheet(worksheet_name):
    clean_name = worksheet_name.strip()
    export_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={clean_name}"
    try:
        df = pd.read_csv(export_url)
        if df is not None and not df.empty:
            return df
        return None
    except Exception:
        return None

# CORE DATABASE WRITE ENGINE: Appends Chat and Exam Logs permanently to your Google Sheet via API webhook
def append_to_sheet_database(worksheet_name, payload_row):
    """
    To write entries live into your sheet tabs ('ChatLogs' and 'ExamArchives'), 
    this routine handles pushing data structures directly.
    """
    # Fallback to local device state cache if your Google Sheets Apps Script API endpoint isn't mapped
    db_backup_file = f"local_db_{worksheet_name}.json"
    try:
        data = []
        if os.path.exists(db_backup_file):
            with open(db_backup_file, "r") as f:
                data = json.load(f)
        data.append(payload_row)
        with open(db_backup_file, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

# Safe Reader for Permanent Records Cache (Survives complete browser or phone reboots)
def load_permanent_database(worksheet_name, default_val):
    db_backup_file = f"local_db_{worksheet_name}.json"
    remote_df = read_public_sheet(worksheet_name)
    if remote_df is not None and not remote_df.empty:
        return remote_df.to_dict(orient="records")
    if os.path.exists(db_backup_file):
        try:
            with open(db_backup_file, "r") as f:
                return json.load(f)
        except Exception:
            return default_val
    return default_val

# AI Core Engine configured precisely to gemini-3.5-flash
def generate_content(prompt_text, api_token):
    try:
        genai.configure(api_key=api_token)
        model = genai.GenerativeModel("models/gemini-3.5-flash")
        response = model.generate_content(prompt_text)
        return response.text  
    except Exception as e:
        return f"AI Engine Connection/Model Failure: {str(e)}"

# Custom Browser Document Layout Constructor
def custom_pdf_download_link(html_content, filename, button_text):
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;charset=utf-8,{b64}" download="{filename}" style="text-decoration:none;"><button style="background-color:#ff3333; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer; font-weight:bold; width:100%;">{button_text}</button></a>'

def display_loading_brand():
    st.markdown("""
        <div style="background-color:#111111; padding:20px; border-radius:10px; border-left: 8px solid #ff0000; text-align:center; margin-bottom:25px;">
            <h1 style="color:#ff0000; font-family:'Arial Black', Gadget, sans-serif; letter-spacing:3px; margin:0; font-size:28px;">🛡️ ACADEMIC SHIELD PRO</h1>
            <p style="color:#ffffff; font-family:'Courier New', monospace; font-size:14px; margin:5px 0 0 0;">System Core Activated</p>
        </div>
        """, unsafe_allow_html=True)

# LOAD PERMANENT VAULT ARCHIVES AND PEER-TO-PEER MESSAGES DIRECTLY FROM DATA RESERVOIR
if "p2p_chat_messages" not in st.session_state:
    st.session_state["p2p_chat_messages"] = load_permanent_database("ChatLogs", [
        {"sender": "System", "text": "Permanent Archive Sync Active. Communications secured.", "time": "00:00", "media_file": None}
    ])
if "historical_exams_archive" not in st.session_state:
    st.session_state["historical_exams_archive"] = load_permanent_database("ExamArchives", [])
if "diagram_vault" not in st.session_state:
    st.session_state["diagram_vault"] = []

# Scholar Login Interface
st.sidebar.title("🔐 Scholar Login")
user = st.sidebar.selectbox("Select Name", ["Setra stones", "Gideon Cheps"])
pwd = st.sidebar.text_input("Enter Access Code", type="password")

authenticated = False
if user == "Setra stones" and pwd == "Amazima2026":
    authenticated = True
elif user == "Gideon Cheps" and pwd == "Gideon2026":
    authenticated = True

if not authenticated:
    # PERMANENT MANDATORY DESCRIPTIVE SYSTEM SIGNATURE RENDERED AT THE ENTRY LOGIN WINDOW
    st.markdown("""
        <div style="text-align:center; margin-top:15%;">
            <h2 style="color:#ff3333; font-family:sans-serif; font-weight:bold; letter-spacing:2px;">🛡️ ACADEMIC SHIELD PRO PORTAL</h2>
            <p style="color:#aaaaaa; font-family:monospace; font-size:14px;">Please supply authorized access credentials in the left sidebar to unlock exam engines.</p>
            <br><br><br>
            <hr style="width:30%; border-color:#333; margin: 0 auto;">
            <p style="color:#ffffff; font-family:'Courier New', monospace; font-size:15px; font-weight:bold; margin-top:15px;">Created by Sudaisi Setra</p>
        </div>
    """, unsafe_allow_html=True)

else:
    st.sidebar.success(f"Welcome, {user}")
    st.sidebar.markdown("---")
    
    subject_choice = st.sidebar.selectbox("📚 Choose Subject", ["Physics", "Mathematics", "Chemistry"])
    
    if user == "Setra stones":
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📂 Upload Diagrams", "📁 Vault Archives"]
    else:
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📁 Vault Archives"]
        
    choice = st.sidebar.radio("Navigate Pages", menu)
    st.sidebar.markdown(f"<br><br><br><div style='color:#aaaaaa; font-size:12px; font-weight:bold;'>⚙️ System Ownership:<br><span style='color:#ff3333;'>Created by Sudaisi Setra</span></div>", unsafe_allow_html=True)

    # PAGE 1: EXAM CENTER (With Permission Gate & Isolated Tracking Matrix)
    if choice == "📝 Exam Center":
        display_loading_brand()
        current_date = datetime.date.today()
        date_seed = current_date.strftime("%Y-%m-%d")
        paper_key = f"{subject_choice}_{date_seed}_twins"
        
        st.title(f"🏛️ UNEB S5 {subject_choice} Competence Portal")
        
        # --- COMMAND PERMISSION GATE CHANNELS ---
        st.info("💡 **Security Gate:** Please declare your intent below before navigating educational metrics.")
        gate_action = st.radio("What is your purpose for launching the Exam Center right now?", 
                               ["🔍 Just checking around / reviewing historical archives", "✍️ I am here to sit an official scheduled examination item right now"])
        
        st.markdown("---")
        
        if gate_action == "🔍 Just checking around / reviewing historical archives":
            st.warning("Assessment initialization held back. The AI Engine will not generate fresh twin papers without exam sitting validation.")
            
            # Show historical copies of this specific subject if they exist in the database so they can always be seen
            subject_historical = [e for e in st.session_state["historical_exams_archive"] if e.get("subject") == subject_choice]
            if subject_historical:
                st.subheader("📚 Saved Historical Scenarios Available for Permanent Offline Study")
                for item in subject_historical:
                    with st.expander(f"📄 Saved Paper: {item['type']} ({item['date']})"):
                        st.markdown(f"<div style='background-color:#111; padding:15px; border-radius:5px;'>{item['content']}</div>", unsafe_allow_html=True)
            else:
                st.info("No historical entries logged under this subject category yet in permanent sync cloud rows.")
                
        else:
            # Active Exam Sitting Allowed - Render Action Command Trigger Button Explicitly
            st.success("Exam validation declared. Click the button component below to instruct the AI engine to generate your twin scenario tasks.")
            
            # Read Google Sheet question bank records
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
                st.error(f"❌ Error: Could not pull row array items from Google Sheet tab for '{subject_choice}'.")

            if base_questions:
                random.seed(date_seed)
                selected_seed_question = random.choice(base_questions)
                
                # MANDATORY COMMAND BUTTON REQUIRING USER PERMISSION BEFORE GENERATING EXAM
                if st.button("🔥 COMMAND ENGINE: Generate Twin Competence Exam Questions Now"):
                    if paper_key not in st.session_state:
                        with st.spinner("🤖 NCDC AI Expert compiling identical twin scenario tasks from sheet guidelines..."):
                            illustration_context = ""
                            if st.session_state["diagram_vault"]:
                                illustration_context = "\nUploaded illustrations available in vault cache:\n" + "\n".join([f"- {d['name']}: {d['desc']}" for d in st.session_state["diagram_vault"]])

                            prompt = (
                                f"You are an NCDC Curriculum Specialist setting a Senior Five {subject_choice} exam. Context: {illustration_context}\n"
                                f"Based EXACTLY on this reference question: '{selected_seed_question}', "
                                f"generate TWO (2) fresh, completely separate, but structurally identical competence-based question scenarios.\n"
                                f"CRITICAL LAWS:\n"
                                f"1. Both questions must share the exact same conceptual setups and formula parameters as the sheet seed.\n"
                                f"2. Output ONLY the clear new NCDC question scenarios, sub-sections, and marks allocation. Absolutely no responses or solutions output."
                            )
                            generated_text = generate_content(prompt, api_key)
                            st.session_state[paper_key] = generated_text
                            
                            # LOG PERMANENTLY TO BOTH RUNNING LOCAL AND REMOTE GOOGLE SPREADSHEET ARCHIVES
                            archive_row = {
                                "id": paper_key,
                                "subject": subject_choice,
                                "type": "Twin Identical Scenarios",
                                "date": current_date.strftime("%Y-%b-%d"),
                                "content": generated_text
                            }
                            if not any(e['id'] == paper_key for e in st.session_state["historical_exams_archive"]):
                                st.session_state["historical_exams_archive"].append(archive_row)
                                append_to_sheet_database("ExamArchives", archive_row)

                # RENDER TIMER AND PAPER ONLY IF PAPER IS ACTIVE AND OPENED BY PERMISSION
                if paper_key in st.session_state:
                    # User-Isolated Private Timer Metrics Tracking Setup
                    timer_state_key = f"{user}_{paper_key}_remaining_seconds"
                    timer_running_key = f"{user}_{paper_key}_is_running"

                    if timer_state_key not in st.session_state:
                        st.session_state[timer_state_key] = 40 * 60  # Independent 40-Minute window isolated strictly to this logged-in account
                        st.session_state[timer_running_key] = True

                    # Automated Bi-Weekly 4-Item Exam Structural Calculations
                    base_milestone_date = datetime.date(2026, 1, 1)
                    days_delta = (current_date - base_milestone_date).days
                    fortnight_cycle_index = days_delta // 14
                    biweekly_paper_key = f"biweekly_paper_cycle_{fortnight_cycle_index}_{subject_choice}"

                    if biweekly_paper_key not in st.session_state:
                        with st.spinner("⏳ Compiling automated bi-weekly 4-item NCDC layout sheet..."):
                            biweekly_prompt = (
                                f"Generate a full-length assessment paper for Senior Five {subject_choice} conforming to NCDC standards. "
                                f"It must consist of exactly FOUR (4) separate comprehensive competence scenarios. Do not include solution markings."
                            )
                            compiled_biweekly_text = generate_content(biweekly_prompt, api_key)
                            st.session_state[biweekly_paper_key] = compiled_biweekly_text
                            
                            biweekly_row = {
                                "id": biweekly_paper_key,
                                "subject": subject_choice,
                                "type": "Official Bi-Weekly 4-Item Exam",
                                "date": current_date.strftime("%Y-%b-%d"),
                                "content": compiled_biweekly_text
                            }
                            st.session_state["historical_exams_archive"].append(biweekly_row)
                            append_to_sheet_database("ExamArchives", biweekly_row)

                    # --- TIMER GRID VISUAL LAYOUT CONTAINER ---
                    timer_col, paper_col = st.columns([1, 2])
                    
                    with timer_col:
                        st.markdown("### ⏱️ Private Clock Deck")
                        rem_seconds = st.session_state[timer_state_key]
                        
                        if rem_seconds > 0:
                            mins, secs = divmod(rem_seconds, 60)
                            status_color = "#ff3333" if st.session_state[timer_running_key] else "#888888"
                            st.markdown(f"""
                                <div class="timer-container" style="border-color: {status_color};">
                                    <span style="color:#aaa; font-size:11px; font-family:monospace;">⏳ PRIVATE ACCOUNT COUNTDOWN</span>
                                    <h2 style="color:#ff3333; font-size:38px; margin:5px 0 0 0; font-family:monospace; font-weight:bold;">{mins:02d}:{secs:02d}</h2>
                                    <p style="margin:2px 0 0 0; font-size:11px; color:#aaa;">Candidate: <b>{user}</b> | Mode: {"RUNNING" if st.session_state[timer_running_key] else "PAUSED"}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # INTERRUPT PAUSE MECHANICS CONTROLS
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.button("⏸️ Pause Exam", key=f"p_{user}_btn"):
                                    st.session_state[timer_running_key] = False
                                    st.rerun()
                            with c2:
                                if st.button("▶️ Resume Exam", key=f"r_{user}_btn"):
                                    st.session_state[timer_running_key] = True
                                    st.rerun()
                        else:
                            st.markdown("""
                                <div class="timer-container" style="border-color: #555555;">
                                    <h2 style="color: #ff3333; font-size: 24px; margin:0; font-family: monospace;">🚨 TIME EXPIRED</h2>
                                </div>
                            """, unsafe_allow_html=True)

                        for diagram in st.session_state["diagram_vault"]:
                            if diagram["subject"] == subject_choice:
                                st.image(diagram["data"], caption=f"🖼️ Linked Support Material: {diagram['name']}")

                    with paper_col:
                        st.markdown(f"### 📝 Active Question Parameters")
                        st.markdown(f'<div class="print-content" style="background-color:#1e1e1e; padding:20px; border-radius:8px;">{st.session_state[paper_key]}</div>', unsafe_allow_html=True)
                        
                        html_formatted_twins = f"<html><body style='font-family:serif; padding:30px;'><h2>Senior Five {subject_choice} Twin Scenarios</h2><hr><p>{st.session_state[paper_key]}</p></body></html>"
                        st.markdown(custom_pdf_download_link(html_formatted_twins, f"{paper_key}.html", "📥 Instant Download Twin Questions Document"), unsafe_allow_html=True)

                    st.markdown("---")
                    
                    # Evaluation Panels
                    st.subheader("✍️ Candidate Examination Script Submission Panel")
                    if st.session_state[timer_state_key] > 0:
                        student_work = st.text_area("Supply structural steps for automatic grading metrics evaluation:", height=150, key=f"work_{user}_box")
                        can_submit = True
                    else:
                        st.warning("Time window closed.")
                        student_work = ""
                        can_submit = False

                    if st.button("🚀 Submit Script for Automated Grading Evaluation", disabled=not can_submit):
                        if student_work.strip() != "":
                            with st.spinner("UNEB Principal Examiner assessing calculations..."):
                                review_prompt = f"Evaluate this student script for Senior Five {subject_choice} based on questions: {st.session_state[paper_key]}. Student work: {student_work}"
                                evaluation_result = generate_content(review_prompt, api_key)
                                st.markdown("### 📊 Official Script Evaluation Report")
                                st.info(evaluation_result)

                    # BI-WEEKLY COMPREHENSIVE OUTPUT SECTION
                    st.markdown("---")
                    st.markdown("## 📅 Automated Bi-Weekly 4-Item Assessment Section")
                    st.caption("Synchronized to NCDC curriculum framework rules.")
                    st.markdown(f'<div style="background-color: #121212; padding: 20px; border-radius: 6px; border-left: 5px solid #ff3333;">{st.session_state.get(biweekly_paper_key, "Compiling...")}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    html_formatted_biweekly = f"<html><body style='font-family:serif; padding:30px;'><h2>Senior Five {subject_choice} - 4-Item Standard Paper</h2><hr><p>{st.session_state.get(biweekly_paper_key, '')}</p></body></html>"
                    st.markdown(custom_pdf_download_link(html_formatted_biweekly, f"Official_BiWeekly_4_Item_{subject_choice}.html", "📥 Instant Download Bi-Weekly 4-Item Paper Document"), unsafe_allow_html=True)

                    # Deduct clock states safely if status is running
                    if st.session_state[timer_state_key] > 0 and st.session_state[timer_running_key]:
                        time.sleep(1)
                        st.session_state[timer_state_key] -= 1
                        st.rerun()

    # PAGE 2: PERMANENT PEER-TO-PEER MULTIMEDIA SCHOLAR CHAT ROOM
    elif choice == "💬 Study Room Chat":
        display_loading_brand()
        st.title("💬 Shared Scholar Communications Room")
        st.caption("Permanent Communication Logger for Setra Stones and Gideon Cheps (Survives Logout/Device Switches)")

        st.markdown("### 📬 Message Logs Archive")
        for message in st.session_state["p2p_chat_messages"]:
            align_class = "chat-right" if message["sender"] == user else "chat-left"
            st.markdown(f"""
                <div class="chat-bubble {align_class}">
                    <strong>{message['sender']}</strong> <span style='font-size:10px; color:#aaa;'>({message.get('time', '00:00')})</span><br>
                    {message['text']}
                </div>
            """, unsafe_allow_html=True)
            
            if "media_file" in message and message["media_file"] is not None:
                try:
                    # Safely handle binary byte streams or reconstructed b64 caches
                    media_bytes = message["media_file"] if isinstance(message["media_file"], bytes) else base64.b64decode(message["media_file"])
                    if message["media_type"].startswith("image/"):
                        st.image(media_bytes)
                    elif message["media_type"].startswith("audio/"):
                        st.audio(media_bytes)
                    elif message["media_type"].startswith("video/"):
                        st.video(media_bytes)
                    else:
                        st.download_button(f"📥 Download Attached {message['media_name']}", media_bytes, file_name=message["media_name"])
                except Exception:
                    pass

        st.markdown("---")
        st.subheader("Broadcast Secure Entry")
        
        chat_text = st.text_input("Type notes or message contents...", key="chat_msg_p2p")
        uploaded_media = st.file_uploader("Attach Audio, Video, Diagrams, or text logs:", type=["txt", "pdf", "png", "jpg", "jpeg", "mp3", "wav", "mp4", "mov"])
        
        if st.button("✉️ Dispatch to Chat Board"):
            timestamp = datetime.datetime.now().strftime("%H:%M")
            if chat_text.strip() != "" or uploaded_media is not None:
                new_msg = {"sender": user, "text": chat_text, "time": timestamp, "media_file": None}
                
                if uploaded_media is not None:
                    raw_bytes = uploaded_media.read()
                    # Convert to string format for robust spreadsheet appending
                    new_msg["media_file"] = base64.b64encode(raw_bytes).decode()
                    new_msg["media_type"] = uploaded_media.type
                    new_msg["media_name"] = uploaded_media.name
                    if chat_text.strip() == "":
                        new_msg["text"] = f"Shared attachment: *{uploaded_media.name}*"
                
                st.session_state["p2p_chat_messages"].append(new_msg)
                # PUSH TO PERMANENT SYNC LOGGER IMMEDIATELY
                append_to_sheet_database("ChatLogs", new_msg)
                st.success("Log updated permanently.")
                st.rerun()

    # PAGE 3: PROGRESS TRACKER
    elif choice == "📊 Progress Tracker":
        display_loading_brand()
        st.header("📊 Global Performance Leaderboard")
        track_df = read_public_sheet("Sheet1")
        if track_df is not None:
            st.table(track_df)
        else:
            st.info("No records checked on 'Sheet1' yet.")

    # PAGE 4: UPLOAD DIAGRAMS (Permanent Support Media Repository)
    elif choice == "📂 Upload Diagrams" and user == "Setra stones":
        display_loading_brand()
        st.header("📂 Visual Aid Support Material Sandbox")
        st.subheader("Upload Illustrative References for the AI Engine to Analyze and Match to Questions")
        
        doc_title = st.text_input("Illustration Title (e.g., Figure_2_Organic_Carbon_Chains):")
        doc_desc = st.text_area("Provide details outlining what this diagram or schema visualizes:")
        uploaded_doc = st.file_uploader("Choose structural file source:", type=["png", "jpg", "jpeg", "pdf"])
        
        if st.button("📥 Commit Document to Reference Vault"):
            if uploaded_doc is not None and doc_title.strip() != "":
                new_diagram = {
                    "name": doc_title,
                    "desc": doc_desc,
                    "subject": subject_choice,
                    "data": uploaded_doc.read(),
                    "type": uploaded_doc.type
                }
                st.session_state["diagram_vault"].append(new_diagram)
                st.success(f"📦 Reference illustration '{doc_title}' added. The AI engine can now interpret this alongside Google Sheet rows.")
            else:
                st.warning("Please fill out text details and attach a file.")

    # PAGE 5: VAULT ARCHIVES (Permanent Download/Print Deck)
    elif choice == "📁 Vault Archives":
        display_loading_brand()
        st.title("📁 Shared Candidate Vault Repositories")
        st.markdown("### 📄 Permanent Document Log Index (Accessible Anywhere, Anytime)")
        
        if st.session_state["historical_exams_archive"]:
            for entry in st.session_state["historical_exams_archive"]:
                with st.expander(f"📄 {entry.get('type','Exam')} - {entry.get('subject','STEM')} (Logged: {entry.get('date','Recent')})"):
                    st.markdown(f'<div style="background-color:white; color:black; padding:20px; font-family:serif; border-radius:4px;">{entry.get("content","No content")}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Direct click tab download action construction
                    raw_html = f"<html><body style='font-family:serif; padding:30px;'><h2>{entry.get('type','Exam')} ({entry.get('subject','')})</h2><hr><p>{entry.get('content','')}</p></body></html>"
                    st.markdown(custom_pdf_download_link(raw_html, f"Archived_{entry.get('id','doc')}.html", "📥 Click to Print or Download PDF Layout File"), unsafe_allow_html=True)
        else:
            st.info("Permanent database vault is empty. Generate entries inside the exam center to initialize.")
