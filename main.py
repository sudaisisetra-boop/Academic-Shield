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
    
    /* Sleek Mobile Keyboard Style Framework */
    div.stButton > button {
        width: 100% !important;
        padding: 8px 2px !important;
        font-weight: bold !important;
        font-size: 15px !important;
        background-color: #222222 !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
        border-radius: 4px !important;
    }
    div.stButton > button:hover {
        background-color: #ff3333 !important;
        color: white !important;
        border-color: #ff3333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Fetch API Keys from Streamlit Secrets
or_key = st.secrets.get("OPENROUTER_API_KEY", "")
groq_key = st.secrets.get("GROQ_API_KEY", "")
cohere_key = st.secrets.get("COHERE_API_KEY", "")

if not or_key and not groq_key and not cohere_key:
    st.error("AI Engine configurations missing. Please verify your keys in the Secrets panel.")

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

# CORE DATABASE WRITE ENGINE
def append_to_sheet_database(worksheet_name, payload_row):
    db_backup_file = f"local_db_{worksheet_name}.json"
    clean_row = payload_row.copy()
    
    try:
        data = []
        if os.path.exists(db_backup_file):
            with open(db_backup_file, "r") as f:
                data = json.load(f)
        
        if "media_file" in clean_row and clean_row["media_file"] is not None:
            if isinstance(clean_row["media_file"], str) and len(clean_row["media_file"]) > 500:
                clean_row["media_file"] = f"Attachment Binary Stored: {clean_row.get('media_name', 'System Document')}"
                
        data.append(clean_row)
        with open(db_backup_file, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

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

# ULTIMATE HYBRID 3-PROVIDER FALLBACK CORE ENGINE (OpenRouter -> Groq -> Cohere)
def generate_content(prompt_text, dummy_api_token=None, image_bytes_data=None, mime_type=None):
    base64_img = ""
    if image_bytes_data is not None:
        base64_img = base64.b64encode(image_bytes_data).decode('utf-8')
        if not mime_type:
            mime_type = "image/jpeg"

    # -------------------------------------------------------------------------
    # PROVIDER 1: OpenRouter (Primary Choice - Gemini 1.5 Flash Free)
    # Handles BOTH Text and Handwritten Photos
    # -------------------------------------------------------------------------
    if or_key:
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {or_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://streamlit.app",
                "X-Title": "Academic Shield Pro"
            }
            
            if image_bytes_data is not None:
                content_payload = [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_img}"}}
                ]
            else:
                content_payload = [{"type": "text", "text": prompt_text}]

            payload = {
                "model": "google/gemini-1.5-flash:free",
                "messages": [{"role": "user", "content": content_payload}],
                "temperature": 0.3
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=25)
            if response.status_code == 200:
                res_json = response.json()
                if 'choices' in res_json and len(res_json['choices']) > 0:
                    return res_json['choices'][0]['message']['content']
        except Exception:
            pass # Suppress and drop down seamlessly into the Groq Backup Engine

    # -------------------------------------------------------------------------
    # PROVIDER 2: Groq Cloud (Backup - Llama 3.2 Vision Native Protocol)
    # Handles BOTH Text and Handwritten Photos
    # -------------------------------------------------------------------------
    if groq_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            }
            
            if image_bytes_data is not None:
                content_payload = [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_img}"}}
                ]
            else:
                content_payload = [{"type": "text", "text": prompt_text}]

            payload = {
                "model": "llama-3.2-11b-vision-preview",
                "messages": [{"role": "user", "content": content_payload}],
                "temperature": 0.3
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=25)
            if response.status_code == 200:
                res_json = response.json()
                if 'choices' in res_json and len(res_json['choices']) > 0:
                    return res_json['choices'][0]['message']['content']
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # PROVIDER 3: Cohere API (Final Text Fortress - Command R+)
    # Handles TEXT ONLY requests (Twin generation, Papers, typed scripts)
    # -------------------------------------------------------------------------
    if cohere_key and image_bytes_data is None:
        try:
            url = "https://api.cohere.com/v1/chat"
            headers = {
                "Authorization": f"Bearer {cohere_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "command-r-plus",
                "message": prompt_text,
                "temperature": 0.3
            }
            response = requests.post(url, json=payload, headers=headers, timeout=25)
            if response.status_code == 200:
                res_json = response.json()
                if 'text' in res_json:
                    return res_json['text']
        except Exception:
            pass

    # CRITICAL FAILURE ACROSS ALL CHANNELS
    return "API System Update Notice: All independent engine servers are currently heavily congested or undergoing maintenance. Please wait a brief moment and re-submit your script verification."

# Custom Browser Document Layout Constructor
def custom_pdf_download_link(html_content, filename, button_text):
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;charset=utf-8,{b64}" download="{filename}" style="text-decoration:none;"><button style="background-color:#ff3333; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer; font-weight:bold; width:100%;">{button_text}</button></a>'

def display_loading_brand():
    st.markdown("""
        <div style="background-color:#111111; padding:20px; border-radius:10px; border-left: 8px solid #ff0000; text-align:center; margin-bottom:25px;">
            <h1 style="color:#ff0000; font-family:'Arial Black', Gadget, sans-serif; letter-spacing:3px; margin:0; font-size:28px;">🛡️ ACADEMIC SHIELD PRO</h1>
            <p style="color:#ffffff; font-family:'Courier New', monospace; font-size:14px; margin:5px 0 0 0;">System Core Activated | Direct Triple Provider Protection</p>
        </div>
        """, unsafe_allow_html=True)

# INITIALIZE MASTER REGISTER VAULTS
if "p2p_chat_messages" not in st.session_state:
    st.session_state["p2p_chat_messages"] = load_permanent_database("ChatLogs", [
        {"sender": "System", "text": "Permanent Storage Sync Active.", "time": "00:00", "timestamp_epoch": 0.0, "media_file": None}
    ])
if "historical_exams_archive" not in st.session_state:
    st.session_state["historical_exams_archive"] = load_permanent_database("ExamArchives", [])
if "diagram_vault" not in st.session_state:
    st.session_state["diagram_vault"] = []

# Calculator Layout Notepad Memory Buffers
if "calc_expression_string" not in st.session_state:
    st.session_state["calc_expression_string"] = ""
if "calc_result_string" not in st.session_state:
    st.session_state["calc_result_string"] = "0"

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

    # ACTIVE LIVE TOAST POP-UP ALERTS
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
                            generated_text = generate_content(prompt)
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
                    biweekly_paper_key = f"biweekly_paper_cycle_current_{subject_choice}"

                    # 🧮 DROP-DOWN MOBILE KEYBOARD CALCULATOR INTERFACE (TAP TO SHOW / DISAPPEAR)
                    with st.expander("🧮 Tap to Open / Close Mobile Desk Calculator Layout", expanded=False):
                        st.markdown(f"""
                            <div style="background-color:#131715; padding:12px; border-radius:6px; border:2px solid #333; margin-bottom:10px;">
                                <div style="color:#777; font-family:monospace; font-size:12px; text-align:left; min-height:16px; letter-spacing:1px;">{st.session_state["calc_expression_string"] if st.session_state["calc_expression_string"] else "Ready"}</div>
                                <div style="color:#39ff14; font-family:monospace; font-size:26px; text-align:right; font-weight:bold; overflow:hidden;">{st.session_state["calc_result_string"]}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        def push_token(tok):
                            st.session_state["calc_expression_string"] += str(tok)
                        def clear_all():
                            st.session_state["calc_expression_string"] = ""
                            st.session_state["calc_result_string"] = "0"
                        def compute_total():
                            raw_expr = st.session_state["calc_expression_string"]
                            if not raw_expr: return
                            try:
                                process_string = raw_expr.replace("×", "*").replace("÷", "/")
                                process_string = process_string.replace("sin(", "math.sin(math.radians(")
                                process_string = process_string.replace("cos(", "math.cos(math.radians(")
                                process_string = process_string.replace("tan(", "math.tan(math.radians(")
                                process_string = process_string.replace("√(", "math.sqrt(")
                                process_string = process_string.replace("log(", "math.log10(")
                                process_string = process_string.replace("ln(", "math.log(")
                                process_string = process_string.replace("^", "**")
                                process_string = process_string.replace("π", "math.pi")
                                
                                open_braces = process_string.count("(")
                                check_braces = process_string.count(")")
                                if open_braces > check_braces:
                                    process_string += ")" * (open_braces - check_braces)
                                        
                                res = eval(process_string, {"math": math, "__builtins__": None}, {})
                                st.session_state["calc_result_string"] = str(round(res, 6) if isinstance(res, float) else res)
                            except Exception:
                                st.session_state["calc_result_string"] = "Syntax Error"

                        # Mobile Layout Rows Running Horizontally (Left to Right)
                        row1_cols = st.columns([1,1,1,1,1,1,1,1,1,1])
                        if row1_cols[0].button("1", key="m_1"): push_token("1"); st.rerun()
                        if row1_cols[1].button("2", key="m_2"): push_token("2"); st.rerun()
                        if row1_cols[2].button("3", key="m_3"): push_token("3"); st.rerun()
                        if row1_cols[3].button("4", key="m_4"): push_token("4"); st.rerun()
                        if row1_cols[4].button("5", key="m_5"): push_token("5"); st.rerun()
                        if row1_cols[5].button("6", key="m_6"): push_token("6"); st.rerun()
                        if row1_cols[7].button("8", key="m_8"): push_token("8"); st.rerun()
                        if row1_cols[6].button("7", key="m_7"): push_token("7"); st.rerun()
                        if row1_cols[8].button("9", key="m_9"): push_token("9"); st.rerun()
                        if row1_cols[9].button("0", key="m_0"): push_token("0"); st.rerun()

                        row2_cols = st.columns([1,1,1,1,1,1,1,1,1,1])
                        if row2_cols[0].button("+", key="m_add"): push_token("+"); st.rerun()
                        if row2_cols[1].button("-", key="m_sub"): push_token("-"); st.rerun()
                        if row2_cols[2].button("×", key="m_mul"): push_token("×"); st.rerun()
                        if row2_cols[3].button("÷", key="m_div"): push_token("÷"); st.rerun()
                        if row2_cols[4].button(".", key="m_dot"): push_token("."); st.rerun()
                        if row2_cols[5].button("x²", key="m_sq"): push_token("^2"); st.rerun()
                        if row2_cols[6].button("x³", key="m_cb"): push_token("^3"); st.rerun()
                        if row2_cols[7].button("xʸ", key="m_pwr"): push_token("^"); st.rerun()
                        if row2_cols[8].button("√", key="m_sqrt"): push_token("√("); st.rerun()
                        if row2_cols[9].button("π", key="m_pi"): push_token("π"); st.rerun()

                        row3_cols = st.columns([1,1,1,1,1,1,1,1,1,1])
                        if row3_cols[0].button("sin", key="m_sin"): push_token("sin("); st.rerun()
                        if row3_cols[1].button("cos", key="m_cos"): push_token("cos("); st.rerun()
                        if row3_cols[2].button("tan", key="m_tan"): push_token("tan("); st.rerun()
                        if row3_cols[3].button("log", key="m_log"): push_token("log("); st.rerun()
                        if row3_cols[4].button("ln", key="m_ln"): push_token("ln("); st.rerun()
                        if row3_cols[5].button(" ( ", key="m_op"): push_token("("); st.rerun()
                        if row3_cols[6].button(" ) ", key="m_cl"): push_token(")"); st.rerun()
                        if row3_cols[7].button("AC", key="m_ac"): clear_all(); st.rerun()
                        
                        # Large Execute Area inside row 3 columns
                        if row3_cols[8].button(" ＝ ", key="m_equals"):
                            compute_total()
                            st.rerun()

                    # SPLIT VISUAL PANELS
                    timer_col, paper_col = st.columns([1.0, 3.0])
                    
                    with timer_col:
                        st.markdown("### ⏱️ Session Deck")
                        st.markdown(f"""
                            <div class="timer-container" style="border-color: #ff3333;">
                                <span style="color:#aaa; font-size:11px; font-family:monospace;">📝 LOGGED CANDIDATE</span>
                                <h2 style="color:#ff3333; font-size:24px; margin:5px 0 0 0; font-family:monospace; font-weight:bold;">PORTAL LIVE</h2>
                                <p style="margin:2px 0 0 0; font-size:11px; color:#aaa;">Candidate: <b>{user}</b><br>Core Matrix: Dynamic Triple Fallback</p>
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
                    
                    # FLEXIBLE DUAL TEXT/PHOTO ASSIGNMENT SUBMISSION GATEWAY
                    st.subheader("✍️ Candidate Examination Script Submission Panel")
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

                    # EVALUATION BLOCK 
                    if st.button("🚀 Submit Script for Automated Grading Evaluation"):
                        has_content = (student_work_text.strip() != "") or (uploaded_photo_bytes is not None)
                        if has_content:
                            with st.spinner("UNEB Principal Examiner assessing calculations and cross-matching logic structures via API Protection Gate..."):
                                
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
                                    evaluation_result = generate_content(review_prompt, None, uploaded_photo_bytes, photo_mime)
                                else:
                                    full_text_prompt = f"{review_prompt}\n\nCandidate typed answer script content:\n{student_work_text}"
                                    evaluation_result = generate_content(full_text_prompt)
                                
                                st.markdown("### 📊 Official Script Evaluation Report")
                                polished_report = evaluation_result.replace("[[MISFIRE_DETECTION_TRIGGERED]]", "")
                                st.info(polished_report)
                                
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
                    
                    if st.button("✨ OPTIONAL ENGINE: Generate Bi-Weekly 4-Item Exam Paper"):
                        with st.spinner("⏳ Compiling full-length 4-item NCDC standard layout..."):
                            biweekly_prompt = (
                                f"Generate a full-length assessment paper for Senior Five {subject_choice} conforming to NCDC standards. "
                                f"It must consist of exactly FOUR (4) separate comprehensive competence scenarios. Do not include solution markings."
                            )
                            compiled_biweekly_text = generate_content(biweekly_prompt)
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
                    
                    if biweekly_paper_key in st.session_state:
                        st.markdown(f'<div style="background-color: #121212; padding: 20px; border-radius: 6px; border-left: 5px solid #ff3333;">{st.session_state[biweekly_paper_key]}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        html_formatted_biweekly = f"<html><body style='font-family:serif; padding:30px;'><h2>Senior Five {subject_choice} - 4-Item Standard Paper</h2><hr><p>{st.session_state[biweekly_paper_key]}</p></body></html>"
                        st.markdown(custom_pdf_download_link(html_formatted_biweekly, f"Official_BiWeekly_4_Item_{subject_choice}.html", "📥 Instant Download Bi-Weekly 4-Item Paper Document"), unsafe_allow_html=True)
                    else:
                        st.info("Bi-weekly paper sandbox dormant. Click the initialization button component above to safely generate structural items.")

    # PAGE 2: PERMANENT CHAT ROOM
    elif choice.startswith("💬 Study Room Chat"):
        display_loading_brand()
        st.session_state["user_last_viewed_chat"][user] = time.time()
        
        st.title("💬 Shared Scholar Communications Room")
        st.caption("Permanent Communication Logger")

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
