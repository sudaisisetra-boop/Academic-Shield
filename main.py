import streamlit as st
import pandas as pd
import datetime
import random
import requests
import time
import os
import json
import base64
import math
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Enforced Layout CSS Mechanics
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

# CORE DATABASE READ ENGINE
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

# CORE DATABASE WRITE ENGINE: Securely updates local JSON memory and relays data to your active sheet rows
def append_to_sheet_database(worksheet_name, payload_row):
    db_backup_file = f"local_db_{worksheet_name}.json"
    clean_row = payload_row.copy()
    
    try:
        data = []
        if os.path.exists(db_backup_file):
            with open(db_backup_file, "r") as f:
                data = json.load(f)
        
        # Guard clause: Compress multi-media base64 strings to save sheet grid workspace limits
        if "media_file" in clean_row and clean_row["media_file"] is not None:
            if isinstance(clean_row["media_file"], str) and len(clean_row["media_file"]) > 500:
                clean_row["media_file"] = f"Attachment Binary Stored: {clean_row.get('media_name', 'System Document')}"
                
        data.append(clean_row)
        with open(db_backup_file, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

    # Fire row objects straight to the Web App URL hook
    webhook_url = st.secrets.get("WEBHOOK_DATABASE_URL", "")
    if webhook_url:
        try:
            payload = {
                "worksheet": worksheet_name,
                "row": clean_row
            }
            requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"}, timeout=6)
        except Exception:
            pass

# Safe Reader for Permanent Records Cache
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

# AI Core Engine configured precisely to gemini-3.5-flash (Supports Multi-modal Image analysis)
def generate_content(prompt_text, api_token, image_bytes_data=None, mime_type=None):
    try:
        genai.configure(api_key=api_token)
        model = genai.GenerativeModel("models/gemini-3.5-flash")
        
        if image_bytes_data is not None:
            contents = [
                {"mime_type": mime_type, "data": image_bytes_data},
                prompt_text
            ]
            response = model.generate_content(contents)
        else:
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

# LOAD VAULT REPOSITORIES
if "p2p_chat_messages" not in st.session_state:
    st.session_state["p2p_chat_messages"] = load_permanent_database("ChatLogs", [
        {"sender": "System", "text": "Permanent Storage Sync Active.", "time": "00:00", "timestamp_epoch": 0.0, "media_file": None}
    ])
if "historical_exams_archive" not in st.session_state:
    st.session_state["historical_exams_archive"] = load_permanent_database("ExamArchives", [])
if "diagram_vault" not in st.session_state:
    st.session_state["diagram_vault"] = []

# View State Tracker Registry Map for Chat Alerts
if "user_last_viewed_chat" not in st.session_state:
    st.session_state["user_last_viewed_chat"] = {"Setra stones": time.time(), "Gideon Cheps": time.time()}

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
    
    # UNREAD COUNTER LOGIC
    last_view_time = st.session_state["user_last_viewed_chat"].get(user, 0.0)
    has_unread = False
    unread_count = 0
    
    for msg in st.session_state["p2p_chat_messages"]:
        if msg.get("sender") != user and msg.get("timestamp_epoch", 0.0) > last_view_time:
            has_unread = True
            unread_count += 1

    chat_label = f"💬 Study Room Chat (🔴 {unread_count} NEW)" if has_unread else "💬 Study Room Chat"
    
    if user == "Setra stones":
        menu = ["📝 Exam Center", chat_label, "📊 Progress Tracker", "📂 Upload Diagrams", "📁 Vault Archives"]
    else:
        menu = ["📝 Exam Center", chat_label, "📊 Progress Tracker", "📁 Vault Archives"]
        
    choice = st.sidebar.radio("Navigate Pages", menu)
    st.sidebar.markdown(f"<br><br><br><div style='color:#aaaaaa; font-size:12px; font-weight:bold;'>⚙️ System Ownership:<br><span style='color:#ff3333;'>Created by Sudaisi Setra</span></div>", unsafe_allow_html=True)

    # ACTIVE LIVE TOAST POP-UP ALERTS (Triggers when browsing any other segment panel layout)
    if has_unread and not choice.startswith("💬 Study Room Chat"):
        st.toast(f"🔔 Scholar Room Alert: You have {unread_count} new unread structural messages waiting for verification!", icon="✉️")

    # PAGE 1: EXAM CENTER
    if choice == "📝 Exam Center":
        display_loading_brand()
        current_date = datetime.date.today()
        date_seed = current_date.strftime("%Y-%m-%d")
        paper_key = f"{subject_choice}_{date_seed}_twins"
        
        st.title(f"🏛️ UNEB S5 {subject_choice} Competence Portal")
        
        st.info("💡 **Security Gate:** Please declare your intent below before navigating educational metrics.")
        gate_action = st.radio("What is your purpose for launching the Exam Center right now?", 
                               ["🔍 Just checking around / reviewing historical archives", "✍️ I am here to sit an official scheduled examination item right now"])
        
        st.markdown("---")
        
        if gate_action == "🔍 Just checking around / reviewing historical archives":
            st.warning("Assessment initialization held back. The AI Engine will not generate fresh twin papers without exam sitting validation.")
            
            subject_historical = [e for e in st.session_state["historical_exams_archive"] if e.get("subject") == subject_choice]
            if subject_historical:
                st.subheader("📚 Saved Historical Scenarios Available for Permanent Offline Study")
                for item in subject_historical:
                    with st.expander(f"📄 Saved Paper: {item['type']} ({item['date']})"):
                        st.markdown(f"<div style='background-color:#111; padding:15px; border-radius:5px;'>{item['content']}</div>", unsafe_allow_html=True)
            else:
                st.info("No historical entries logged under this subject category yet in permanent sync cloud rows.")
                
        else:
            st.success("Exam validation declared. Click the button component below to instruct the AI engine to generate your twin scenario tasks.")
            
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

                if paper_key in st.session_state:
                    timer_state_key = f"{user}_{paper_key}_remaining_seconds"
                    timer_running_key = f"{user}_{paper_key}_is_running"

                    if timer_state_key not in st.session_state:
                        st.session_state[timer_state_key] = 40 * 60  
                        st.session_state[timer_running_key] = True

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

                    # THREE COLUMN MATRIX INTERFACE LAYOUT (Packs the side calculator deck beautifully)
                    timer_col, paper_col, calc_col = st.columns([1.1, 1.8, 1.1])
                    
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

                    # BRAND NEW ADDITION: SMART SCIENTIFIC CALCULATOR COMPONENT EXPANDER DECK
                    with calc_col:
                        st.markdown("### 🧮 Exam Scientific Deck")
                        with st.expander("📊 Launch Calculator Engine", expanded=False):
                            st.caption("Perform complex calculations directly inside your workflow.")
                            expr = st.text_input("Enter math expression (e.g., sin(45) * sqrt(180) or 2.5**3):", key=f"calc_{user}_input")
                            if expr:
                                try:
                                    # Create a safe mapping sandbox for evaluating scientific parameters locally
                                    safe_env = {
                                        "sin": lambda x: math.sin(math.radians(x)),
                                        "cos": lambda x: math.cos(math.radians(x)),
                                        "tan": lambda x: math.tan(math.radians(x)),
                                        "sqrt": math.sqrt,
                                        "log": math.log10,
                                        "ln": math.log,
                                        "pi": math.pi,
                                        "e": math.e
                                    }
                                    calc_res = eval(expr, {"__builtins__": None}, safe_env)
                                    st.success(f"Result: **{calc_res}**")
                                except Exception:
                                    st.error("Invalid Math Syntax")

                    st.markdown("---")
                    
                    # SYSTEM PANEL UPGRADE: FLEXIBLE DUAL TEXT/PHOTO ASSIGNMENT SUBMISSION GATEWAY
                    st.subheader("✍️ Candidate Examination Script Submission Panel")
                    if st.session_state[timer_state_key] > 0:
                        submission_mode = st.radio("Choose script compilation input style:", ["⌨️ Type answer text scripts directly", "📸 Upload a photo of handwritten structural calculations"])
                        
                        student_work_text = ""
                        uploaded_photo_bytes = None
                        photo_mime = None
                        
                        if submission_mode == "⌨️ Type answer text scripts directly":
                            student_work_text = st.text_area("Supply structural steps for automatic grading metrics evaluation:", height=150, key=f"work_txt_{user}_box")
                        else:
                            uploaded_photo = st.file_uploader("Snap or upload your handwritten answer sheet:", type=["png", "jpg", "jpeg"], key=f"work_img_{user}_box")
                            if uploaded_photo is not None:
                                uploaded_photo_bytes = uploaded_photo.read()
                                photo_mime = uploaded_photo.type
                                st.image(uploaded_photo_bytes, caption="Uploaded Script Preview", width=250)
                        
                        can_submit = True
                    else:
                        st.warning("Time window closed.")
                        can_submit = False

                    # UPGRADED EVALUATION BLOCK: MARKS REVIEWS AND UNLOCKS CONDITIONAL NCDC SOLUTIONS UPON FAILURE
                    if st.button("🚀 Submit Script for Automated Grading Evaluation", disabled=not can_submit):
                        has_content = (student_work_text.strip() != "") or (uploaded_photo_bytes is not None)
                        if has_content:
                            with st.spinner("UNEB Principal Examiner assessing calculations and cross-matching logic structures..."):
                                
                                review_prompt = (
                                    f"You are a Senior UNEB Principal Examiner grading an S5 {subject_choice} exam based strictly on these target questions:\n"
                                    f"{st.session_state[paper_key]}\n\n"
                                    f"Evaluate the candidate's work provided below. Mark strictly against the official NCDC criteria.\n"
                                    f"IMPORTANT INSTRUCTIONS:\n"
                                    f"1. Give a clear score/grade distribution out of full marks.\n"
                                    f"2. Check if the student has failed, misfired, or gotten any part of the core conceptual calculation steps incorrect.\n"
                                    f"3. CRITICAL: If and only if the student has failed or misfired on any component number, print this exact keyword phrase tag: '[[MISFIRE_DETECTION_TRIGGERED]]' anywhere inside your text response block, and then append a beautiful, highly detailed, step-by-step NCDC standard reference solutions model detailing all mathematical steps."
                                )
                                
                                if uploaded_photo_bytes is not None:
                                    evaluation_result = generate_content(review_prompt, api_key, uploaded_photo_bytes, photo_mime)
                                else:
                                    full_text_prompt = f"{review_prompt}\n\nCandidate typed answer script content:\n{student_work_text}"
                                    evaluation_result = generate_content(full_text_prompt, api_key)
                                
                                st.markdown("### 📊 Official Script Evaluation Report")
                                
                                # Cleanly remove the hidden keyword flag string if present, before showing report text to scholars
                                polished_report = evaluation_result.replace("[[MISFIRE_DETECTION_TRIGGERED]]", "")
                                st.info(polished_report)
                                
                                # Auto-log the grade review to historical records database array rows
                                log_payload = {
                                    "id": f"Review_{paper_key}_{user}",
                                    "subject": subject_choice,
                                    "type": f"Graded Work: {user}",
                                    "date": current_date.strftime("%Y-%b-%d"),
                                    "content": polished_report
                                }
                                append_to_sheet_database("ExamArchives", log_payload)

                    st.markdown("---")
                    st.markdown("## 📅 Automated Bi-Weekly 4-Item Assessment Section")
                    st.caption("Synchronized to NCDC curriculum framework rules.")
                    st.markdown(f'<div style="background-color: #121212; padding: 20px; border-radius: 6px; border-left: 5px solid #ff3333;">{st.session_state.get(biweekly_paper_key, "Compiling...")}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    html_formatted_biweekly = f"<html><body style='font-family:serif; padding:30px;'><h2>Senior Five {subject_choice} - 4-Item Standard Paper</h2><hr><p>{st.session_state.get(biweekly_paper_key, '')}</p></body></html>"
                    st.markdown(custom_pdf_download_link(html_formatted_biweekly, f"Official_BiWeekly_4_Item_{subject_choice}.html", "📥 Instant Download Bi-Weekly 4-Item Paper Document"), unsafe_allow_html=True)

                    if st.session_state[timer_state_key] > 0 and st.session_state[timer_running_key]:
                        time.sleep(1)
                        st.session_state[timer_state_key] -= 1
                        st.rerun()

    # PAGE 2: PERMANENT CHAT ROOM
    elif choice.startswith("💬 Study Room Chat"):
        display_loading_brand()
        
        # Clear view tracking registers safely
        st.session_state["user_last_viewed_chat"][user] = time.time()
        
        st.title("💬 Shared Scholar Communications Room")
        st.caption("Permanent Communication Logger (Real-Time Counter Alerts Engaged)")

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
            current_time_epoch = time.time()
            timestamp = datetime.datetime.now().strftime("%H:%M")
            if chat_text.strip() != "" or uploaded_media is not None:
                new_msg = {
                    "sender": user, 
                    "text": chat_text, 
                    "time": timestamp, 
                    "timestamp_epoch": current_time_epoch, 
                    "media_file": None
                }
                
                if uploaded_media is not None:
                    raw_bytes = uploaded_media.read()
                    new_msg["media_file"] = base64.b64encode(raw_bytes).decode()
                    new_msg["media_type"] = uploaded_media.type
                    new_msg["media_name"] = uploaded_media.name
                    if chat_text.strip() == "":
                        new_msg["text"] = f"Shared attachment: *{uploaded_media.name}*"
                
                st.session_state["p2p_chat_messages"].append(new_msg)
                append_to_sheet_database("ChatLogs", new_msg)
                
                st.session_state["user_last_viewed_chat"][user] = current_time_epoch
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

    # PAGE 4: UPLOAD DIAGRAMS
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

    # PAGE 5: VAULT ARCHIVES
    elif choice == "📁 Vault Archives":
        display_loading_brand()
        st.title("📁 Shared Candidate Vault Repositories")
        st.markdown("### 📄 Permanent Document Log Index")
        
        if st.session_state["historical_exams_archive"]:
            for entry in st.session_state["historical_exams_archive"]:
                with st.expander(f"📄 {entry.get('type','Exam')} - {entry.get('subject','STEM')} (Logged: {entry.get('date','Recent')})"):
                    st.markdown(f'<div style="background-color:white; color:black; padding:20px; font-family:serif; border-radius:4px;">{entry.get("content","No content")}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    raw_html = f"<html><body style='font-family:serif; padding:30px;'><h2>{entry.get('type','Exam')} ({entry.get('subject','')})</h2><hr><p>{entry.get('content','')}</p></body></html>"
                    st.markdown(custom_pdf_download_link(raw_html, f"Archived_{entry.get('id','doc')}.html", "📥 Click to Print or Download PDF Layout File"), unsafe_allow_html=True)
        else:
            st.info("Permanent database vault is empty. Generate entries inside the exam center to initialize.")
