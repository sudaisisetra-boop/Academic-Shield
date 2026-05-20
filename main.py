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

# Custom Styles for Timers, Chats, and Document Layouts
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

# Stable Google Sheets Reader Engine
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

# SDK Function configured to stick precisely to your gemini-3.5-flash choice
def generate_content(prompt_text, api_token):
    try:
        genai.configure(api_key=api_token)
        model = genai.GenerativeModel("models/gemini-3.5-flash")
        response = model.generate_content(prompt_text)
        return response.text  
    except Exception as e:
        return f"AI Engine Connection/Model Failure: {str(e)}"

# Helper utility to generate printable/downloadable browser attachments
def custom_pdf_download_link(html_content, filename, button_text):
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;charset=utf-8,{b64}" download="{filename}" style="text-decoration:none;"><button style="background-color:#ff3333; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer; font-weight:bold; width:100%;">{button_text}</button></a>'

def display_loading_brand():
    st.markdown("""
        <div style="background-color:#111111; padding:20px; border-radius:10px; border-left: 8px solid #ff0000; text-align:center; margin-bottom:25px;">
            <h1 style="color:#ff0000; font-family:'Arial Black', Gadget, sans-serif; letter-spacing:3px; margin:0; font-size:28px;">🛡️ ACADEMIC SHIELD PRO</h1>
            <p style="color:#ffffff; font-family:'Courier New', monospace; font-size:14px; margin:5px 0 0 0;">Created by <span style="color:#ff3333; font-weight:bold;">Sudaisi Setra</span></p>
        </div>
        """, unsafe_allow_html=True)

# Global Memory State Initializations
if "p2p_chat_messages" not in st.session_state:
    st.session_state["p2p_chat_messages"] = [
        {"sender": "System", "text": "Welcome to the Scholar Room. Leave notes, files, or audio for each other here.", "type": "text", "time": "00:00"}
    ]
if "diagram_vault" not in st.session_state:
    st.session_state["diagram_vault"] = []  # Holds dictionaries of uploaded support material records
if "historical_exams_archive" not in st.session_state:
    st.session_state["historical_exams_archive"] = [] # Persistent tracking of all generated scenarios

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
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📂 Upload Diagrams", "📁 Vault Archives"]
    else:
        menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📁 Vault Archives"]
        
    choice = st.sidebar.radio("Navigate Pages", menu)
    st.sidebar.markdown("<br><br><br><div style='color:#aaaaaa; font-size:12px; font-weight:bold;'>⚙️ System Ownership:<br><span style='color:#ff3333;'>ASP Private System</span></div>", unsafe_allow_html=True)

    # PAGE 1: EXAM CENTER
    if choice == "📝 Exam Center":
        display_loading_brand()
        current_date = datetime.date.today()
        
        st.title(f"🏛️ UNEB S5 {subject_choice} Competence Portal")
        st.caption(f"📅 Daily Session: **{current_date.strftime('%Y-%m-%d')}**")

        # Read specific sheet tables cleanly
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
            st.error(f"❌ Error: Could not pull items from the Google Sheet tab for '{subject_choice}'.")

        if base_questions:
            date_seed = current_date.strftime("%Y-%m-%d")
            random.seed(date_seed)
            selected_seed_question = random.choice(base_questions)
            
            # STAGE 1: Isolated Generation & Archiving of the Twin Scenarios
            paper_key = f"{subject_choice}_{date_seed}_twins"
            if paper_key not in st.session_state:
                with st.spinner("🤖 NCDC AI Expert is compiling the twin identical competence items..."):
                    # Look up if any user-uploaded diagram descriptions can be fed as context to Gemini
                    illustration_context = ""
                    if st.session_state["diagram_vault"]:
                        illustration_context = "\nConsider these uploaded structural diagram references currently available in cache:\n" + "\n".join([f"- {d['name']}: {d['desc']}" for d in st.session_state["diagram_vault"]])

                    prompt = (
                        f"You are an NCDC Curriculum Specialist setting a Senior Five {subject_choice} exam. Use {illustration_context}\n"
                        f"Based EXACTLY on this reference row layout from our database: '{selected_seed_question}', "
                        f"generate TWO (2) fresh, separate, but structurally identical competence-based question scenarios.\n"
                        f"CRITICAL REQUIREMENTS:\n"
                        f"1. Both questions must require the exact same conceptual approach, formulas, and math steps as the reference layout.\n"
                        f"2. Phrase them purely as modern NCDC competence scenarios (contextual real-world tasks), NOT old syllabus parameters.\n"
                        f"3. Output ONLY the questions, clear sub-sections (a, b, c), and marks. Absolute ban on providing solutions, answers, or marking schemes initially."
                    )
                    generated_text = generate_content(prompt, api_key)
                    st.session_state[paper_key] = generated_text
                    
                    # Store to permanent session archive log instantly so it can be seen in Vault Archives forever
                    st.session_state["historical_exams_archive"].append({
                        "id": paper_key,
                        "subject": subject_choice,
                        "type": "Twin Identical Scenarios",
                        "date": current_date.strftime("%Y-%b-%d"),
                        "content": generated_text
                    })

            # STAGE 2: User-Specific Isolated Timer Initialization with Pause Controls
            timer_state_key = f"{user}_{paper_key}_remaining_seconds"
            timer_running_key = f"{user}_{paper_key}_is_running"

            if timer_state_key not in st.session_state:
                st.session_state[timer_state_key] = 40 * 60  # Strictly 40 Minutes initialized only for this current logged-in user
                st.session_state[timer_running_key] = True

            # STAGE 3: Automatic Bi-Weekly 4-Item Exam Generation Calculations
            # Calculates weeks from a milestone baseline epoch to verify fortnightly intervals
            base_milestone_date = datetime.date(2026, 1, 1)
            days_delta = (current_date - base_milestone_date).days
            fortnight_cycle_index = days_delta // 14
            biweekly_paper_key = f"biweekly_paper_cycle_{fortnight_cycle_index}_{subject_choice}"

            if biweekly_paper_key not in st.session_state:
                # Trigger automation rules immediately if a 14-day cycle window boundaries cross
                with st.spinner("⏳ Automated Fortnightly Cycle Detected. Compiling 4-Item UNEB Standard Exam Paper..."):
                    biweekly_prompt = (
                        f"Generate an official standalone educational assessment examination paper for Senior Five {subject_choice} "
                        f"conforming strictly to the new NCDC competence-based curriculum standard guidelines.\n"
                        f"The paper must contain exactly FOUR (4) comprehensive, multi-part scenario items contextually framed for Uganda. "
                        f"Output format: Standard neat examination paper layout with student directions and complete marks allocation. Do not include answers."
                    )
                    compiled_biweekly_text = generate_content(biweekly_prompt, api_key)
                    st.session_state[biweekly_paper_key] = compiled_biweekly_text
                    
                    # Log into long term visible archives
                    st.session_state["historical_exams_archive"].append({
                        "id": biweekly_paper_key,
                        "subject": subject_choice,
                        "type": "Official Bi-Weekly 4-Item Exam",
                        "date": current_date.strftime("%Y-%b-%d"),
                        "content": compiled_biweekly_text
                    })

            # --- UI RENDERING GRID ---
            timer_col, paper_col = st.columns([1, 2])
            
            with timer_col:
                st.markdown("### ⏱️ Isolated Session Control")
                rem_seconds = st.session_state[timer_state_key]
                
                if rem_seconds > 0:
                    mins, secs = divmod(rem_seconds, 60)
                    status_color = "#ff3333" if st.session_state[timer_running_key] else "#888888"
                    st.markdown(f"""
                        <div class="timer-container" style="border-color: {status_color};">
                            <span style="color: #aaaaaa; font-size: 11px; font-family: monospace; text-transform: uppercase;">⏱️ Your Private Exam Countdown</span>
                            <h2 style="color: #ff3333; font-size: 38px; margin: 5px 0 0 0; font-family: monospace; font-weight: bold;">{mins:02d}:{secs:02d}</h2>
                            <p style="margin:2px 0 0 0; font-size:11px; color:#aaa;">Status: {"ACTIVE" if st.session_state[timer_running_key] else "PAUSED"}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Native Manual Interruption Control Buttons
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("⏸️ Pause Clock", key=f"p_{user}"):
                            st.session_state[timer_running_key] = False
                            st.rerun()
                    with c2:
                        if st.button("▶️ Resume Clock", key=f"r_{user}"):
                            st.session_state[timer_running_key] = True
                            st.rerun()
                else:
                    st.markdown("""
                        <div class="timer-container" style="border-color: #555555;">
                            <h2 style="color: #ff3333; font-size: 24px; margin:0; font-family: monospace;">🚨 TIME EXPIRED</h2>
                        </div>
                    """, unsafe_allow_html=True)

                # Render matched support diagrams from vault inside your viewport
                for diagram in st.session_state["diagram_vault"]:
                    if diagram["subject"] == subject_choice:
                        st.image(diagram["data"], caption=f"🖼️ Linked Illustration: {diagram['name']}")

            with paper_col:
                st.markdown(f"### 📝 Active Candidate Examination Questions ({subject_choice})")
                st.markdown(f'<div class="print-content" style="background-color:#1e1e1e; padding:20px; border-radius:8px;">{st.session_state[paper_key]}</div>', unsafe_allow_html=True)
                
                # Immediate Download Tab Link Action for active items
                html_formatted_twins = f"<html><body style='font-family:sans-serif; padding:30px;'><h2>Senior Five {subject_choice} Twin Scenarios</h2><hr><p>{st.session_state[paper_key]}</p></body></html>"
                st.markdown(custom_pdf_download_link(html_formatted_twins, f"{paper_key}.html", "📥 Download/Print Active Twin Questions (PDF Layout)"), unsafe_allow_html=True)

            st.markdown("---")
            
            # Hand in Scripts Execution Logic
            st.subheader("✍️ Candidate Examination Script Submission Panel")
            if st.session_state[timer_state_key] > 0:
                student_work = st.text_area("Type or paste your complete step-by-step structural calculations and final outcomes here:", height=180, key=f"work_{user}")
                can_submit = True
            else:
                st.warning("Submission structural engine locked. The 40-minute window for these twin items has concluded.")
                student_work = ""
                can_submit = False

            if st.button("🚀 Submit Script for Automated Grading Evaluation", disabled=not can_submit):
                if student_work.strip() == "":
                    st.warning("Please supply calculations before submission mapping.")
                else:
                    with st.spinner("UNEB Principal Examiner assessing your calculations..."):
                        review_prompt = (
                            f"You are the UNEB Principal Examiner evaluating an academic script for Senior Five {subject_choice}.\n"
                            f"EXAM QUESTION SHEET:\n{st.session_state[paper_key]}\n\n"
                            f"CANDIDATE'S SUBMITTED WORKING SCRIPTS:\n{student_work}\n\n"
                            f"GRADING DIRECTIVE:\n"
                            f"Check their solutions step-by-step. If they passed perfectly, congratulate them warmly.\n"
                            f"If they made structural mathematical errors or failed any portion, highlight exactly where the calculation failed, "
                            f"then provide the complete step-by-step calculations and conceptual explanations."
                        )
                        evaluation_result = generate_content(review_prompt, api_key)
                        st.markdown("### 📊 Official Script Evaluation Report")
                        st.info(evaluation_result)

            # RENDER THE COMPREHENSIVE BI-WEEKLY 4-ITEM PAPER DOWNSTREAM WITH DIRECT DOWNLOAD TAB
            st.markdown("---")
            st.markdown("## 📅 Automated Bi-Weekly 4-Item Assessment Section")
            st.caption("Generated automatically every 2 weeks according to NCDC standards.")
            
            st.markdown(f'<div style="background-color: #121212; padding: 20px; border-radius: 6px; border-left: 5px solid #ff3333;">{st.session_state[biweekly_paper_key]}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Download Tab link action for Biweekly Paper
            html_formatted_biweekly = f"<html><body style='font-family:sans-serif; padding:30px;'><h2>Senior Five {subject_choice} - 4-Item Standard UNEB Paper</h2><hr><p>{st.session_state[biweekly_paper_key]}</p></body></html>"
            st.markdown(custom_pdf_download_link(html_formatted_biweekly, f"Official_BiWeekly_4_Item_{subject_choice}.html", "📥 Download/Print Bi-Weekly 4-Item Exam Sheet"), unsafe_allow_html=True)

            # Deduct seconds smoothly if session status is active
            if st.session_state[timer_state_key] > 0 and st.session_state[timer_running_key]:
                time.sleep(1)
                st.session_state[timer_state_key] -= 1
                st.rerun()

    # PAGE 2: TRUE PEER-TO-PEER MULTIMEDIA SCHOLAR CHAT ROOM
    elif choice == "💬 Study Room Chat":
        display_loading_brand()
        st.title("💬 Shared Scholar Communications Room")
        st.caption("Live Interactive Communication Feed between Setra Stones and Gideon Cheps")

        st.markdown("### 📬 Message Logs")
        for message in st.session_state["p2p_chat_messages"]:
            align_class = "chat-right" if message["sender"] == user else "chat-left"
            st.markdown(f"""
                <div class="chat-bubble {align_class}">
                    <strong>{message['sender']}</strong> <span style='font-size:10px; color:#aaa;'>({message['time']})</span><br>
                    {message['text']}
                </div>
            """, unsafe_allow_html=True)
            
            if "media_file" in message:
                if message["media_type"].startswith("image/"):
                    st.image(message["media_file"])
                elif message["media_type"].startswith("audio/"):
                    st.audio(message["media_file"])
                elif message["media_type"].startswith("video/"):
                    st.video(message["media_file"])
                else:
                    st.download_button(f"📥 Download {message['media_name']}", message["media_file"], file_name=message["media_name"])

        st.markdown("---")
        st.subheader("Broadcast Message or Media Attachment")
        
        chat_text = st.text_input("Type message entry or notes...", key="chat_msg_input")
        uploaded_media = st.file_uploader("Attach Audio clips, Videos, PDFs, or Graphic diagrams to chat log:", type=["txt", "pdf", "png", "jpg", "jpeg", "mp3", "wav", "mp4", "mov"])
        
        if st.button("✉️ Dispatch to Chat Board"):
            timestamp = datetime.datetime.now().strftime("%H:%M")
            if chat_text.strip() != "" or uploaded_media is not None:
                new_msg = {"sender": user, "text": chat_text, "time": timestamp}
                
                if uploaded_media is not None:
                    new_msg["media_file"] = uploaded_media.read()
                    new_msg["media_type"] = uploaded_media.type
                    new_msg["media_name"] = uploaded_media.name
                    if chat_text.strip() == "":
                        new_msg["text"] = f"Shared attachment file: *{uploaded_media.name}*"
                
                st.session_state["p2p_chat_messages"].append(new_msg)
                st.success("Log updated.")
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

    # PAGE 4: UPLOAD DIAGRAMS (Supports standalone attachments to supplement Gemini interpretation)
    elif choice == "📂 Upload Diagrams" and user == "Setra stones":
        display_loading_brand()
        st.header("📂 Visual Aid Support Material Sandbox")
        st.subheader("Upload Illustrative References for the AI Engine to Analyze")
        
        doc_title = st.text_input("Diagram or Document Reference Name (e.g., Figure_1_Kinematics):")
        doc_desc = st.text_area("Provide a concise technical summary explaining what this illustration shows (e.g., 'A pulley network tracking string acceleration with vectors'):")
        uploaded_doc = st.file_uploader("Upload visual aid files (.png, .jpg, .jpeg, .pdf):", type=["png", "jpg", "jpeg", "pdf"])
        
        if st.button("📥 Commit Document to Reference Cache"):
            if uploaded_doc is not None and doc_title.strip() != "":
                st.session_state["diagram_vault"].append({
                    "name": doc_title,
                    "desc": doc_desc,
                    "subject": subject_choice,
                    "data": uploaded_doc.read(),
                    "type": uploaded_doc.type
                })
                st.success(f"📦 Reference file '{doc_title}' added. The AI engine can now interpret this illustration alongside topic question rows.")
            else:
                st.warning("Please fill out the title name and upload a source material file.")

    # PAGE 5: VAULT ARCHIVES (With permanent download click buttons for all generated logs)
    elif choice == "📁 Vault Archives":
        display_loading_brand()
        st.title("📁 Shared Candidate Vault Repositories")
        st.markdown("### 📄 Accessible Active Document Logs (PDF Format Download Center)")
        
        if st.session_state["historical_exams_archive"]:
            for entry in st.session_state["historical_exams_archive"]:
                with st.expander(f"📄 {entry['type']} - {entry['subject']} ({entry['date']})"):
                    st.markdown(f'<div style="background-color:white; color:black; padding:20px; font-family:serif; border-radius:4px;">{entry["content"]}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Direct click tab download binding
                    raw_html = f"<html><body style='font-family:serif; padding:30px;'><h2>{entry['type']} - {entry['subject']}</h2><hr><p>{entry['content']}</p></body></html>"
                    st.markdown(custom_pdf_download_link(raw_html, f"Archived_{entry['id']}.html", f"📥 Download {entry['type']} directly to internal storage"), unsafe_allow_html=True)
        else:
            st.info("Vault registry is empty. Generate exam entries inside the portal to populate archives.")
else:
    st.sidebar.warning("Access Denied. Please input valid candidate authentication credentials.")
