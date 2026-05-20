import streamlit as st
import pandas as pd
import datetime
import random
import requests
import time
import os
import json
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Enforced Custom Styles & Print Setup
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
        margin-bottom: 25px;
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

# UNCHANGED: Stable Google Sheets Reader Engine
def read_public_sheet(worksheet_name):
    sheet_id = "1xU80PotVALVM3sWt7PS3kLGbsivqzMvznXq0c8Cu44M"
    clean_name = worksheet_name.strip()
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={clean_name}"
    try:
        df = pd.read_csv(export_url)
        if df is not None and not df.empty:
            return df
        return None
    except Exception as e:
        return None

# FIXED: Permanent Official Gemini SDK Function as commanded by the Recovery Guide
def generate_content(prompt_text, api_token):
    try:
        genai.configure(api_key=api_token)
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt_text)
        return response.text  
    except Exception as e:
        return f"AI Engine Failure: {str(e)}"

def display_loading_brand():
    st.markdown("""
        <div style="background-color:#111111; padding:20px; border-radius:10px; border-left: 8px solid #ff0000; text-align:center; margin-bottom:25px;">
            <h1 style="color:#ff0000; font-family:'Arial Black', Gadget, sans-serif; letter-spacing:3px; margin:0; font-size:28px;">🛡️ ACADEMIC SHIELD PRO</h1>
            <p style="color:#ffffff; font-family:'Courier New', monospace; font-size:14px; margin:5px 0 0 0;">Created by <span style="color:#ff3333; font-weight:bold;">Sudaisi Setra</span></p>
        </div>
        """, unsafe_allow_html=True)

# Mock Persistent Storage for Peer-to-Peer Scholar Chat & Diagrams Cache
if "p2p_chat_messages" not in st.session_state:
    st.session_state["p2p_chat_messages"] = [
        {"sender": "System", "text": "Welcome to the Scholar Room. Leave notes, files, or audio for each other here.", "type": "text", "time": "00:00"}
    ]
if "diagram_vault" not in st.session_state:
    st.session_state["diagram_vault"] = {}

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

    # PAGE 1: EXAM CENTER (Hides answers, renders questions next to the timer, checks data correctly)
    if choice == "📝 Exam Center":
        display_loading_brand()
        current_date = datetime.date.today()
        
        st.title(f"🏛️ UNEB S5 {subject_choice} Competence Portal")
        st.caption(f"📅 Daily Session: **{current_date.strftime('%Y-%m-%d')}**")

        # Multi-tier spreadsheet reading
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
            # Seed selection ensuring stable tracking across updates
            date_seed = current_date.strftime("%Y-%m-%d")
            random.seed(date_seed)
            selected_seed_question = random.choice(base_questions)
            
            # STAGE 1: Generate 2 Identical New Curriculum Questions from the Google Sheet reference
            if "twin_questions" not in st.session_state or st.session_state.get("exam_subject") != subject_choice:
                with st.spinner("🤖 NCDC AI Expert is compiling the twin identical competence items..."):
                    prompt = (
                        f"You are an NCDC Curriculum Specialist setting a Senior Five {subject_choice} exam.\n"
                        f"Based EXACTLY on this reference question from our database: '{selected_seed_question}', "
                        f"generate TWO (2) fresh, separate, but identical competence-based question scenarios.\n"
                        f"CRITICAL REQUIREMENTS:\n"
                        f"1. Both questions must require the exact same structural approach and solution methods as the reference question.\n"
                        f"2. Frame them purely as modern NCDC competence scenarios (contextual real-life scenarios), NOT old curriculum knowledge retrieval.\n"
                        f"3. Output ONLY the questions, clear sub-sections (a, b, c), and marks. Absolute ban on providing solutions, answers, guides, or final parameters."
                    )
                    st.session_state["twin_questions"] = generate_content(prompt, api_key)
                    st.session_state["exam_subject"] = subject_choice
                    st.session_state["timer_start_time"] = time.time()
                    st.session_state["four_item_paper"] = None  # Clear downstream paper until unlocked

            # STAGE 2: Timer Layout Configuration (Fixed to prevent UI wiping out questions)
            TOTAL_EXAM_SECONDS = 40 * 60  # Updated to strictly 40 minutes for the two items
            elapsed = time.time() - st.session_state.get("timer_start_time", time.time())
            remaining = int(TOTAL_EXAM_SECONDS - elapsed)

            # RENDER TIMER AND QUESTIONS TOGETHER INSIDE FIXED STREAMLIT COLS
            timer_col, paper_col = st.columns([1, 2])
            
            with timer_col:
                if remaining > 0:
                    mins, secs = divmod(remaining, 60)
                    st.markdown(f"""
                        <div class="timer-container">
                            <span style="color: #aaaaaa; font-size: 12px; font-family: monospace;">⏱️ TWIN-ITEM countdown</span>
                            <h2 style="color: #ff3333; font-size: 42px; margin: 5px 0 0 0; font-family: monospace; font-weight: bold;">{mins:02d}:{secs:02d}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="timer-container" style="border-color: #555555;">
                            <h2 style="color: #ff3333; font-size: 26px; margin:0;">🚨 TIME ELAPSED</h2>
                        </div>
                    """, unsafe_allow_html=True)

                # Show visual aid diagram if it was previously uploaded for this seed
                if selected_seed_question in st.session_state["diagram_vault"]:
                    st.image(st.session_state["diagram_vault"][selected_seed_question], caption="Official Visual Aid Diagram for this Exam Item")

            with paper_col:
                st.markdown("### 📝 Active Candidate Examination Questions")
                st.markdown(f'<div class="print-content">{st.session_state["twin_questions"]}</div>', unsafe_allow_html=True)

            st.markdown("---")
            
            # Hand in Scripts Layout
            st.subheader("✍️ Candidate Examination Script Submission Panel")
            if remaining > 0:
                student_work = st.text_area("Type or paste your step-by-step structural derivations and final values here:", height=200)
                can_submit = True
            else:
                st.warning("Submission structural link locked. The 40-minute window for these twin items has concluded.")
                student_work = ""
                can_submit = False

            if st.button("🚀 Submit Script for Automated Evaluation", disabled=not can_submit):
                if student_work.strip() == "":
                    st.warning("Please input workings before trying to submit.")
                else:
                    with st.spinner("UNEB Principal Examiner assessing your calculations..."):
                        review_prompt = (
                            f"You are the UNEB Principal Examiner evaluating an academic script for Senior Five {subject_choice}.\n"
                            f"EXAM QUESTION SHEET:\n{st.session_state['twin_questions']}\n\n"
                            f"CANDIDATE'S SUBMITTED WORKING SCRIPTS:\n{student_work}\n\n"
                            f"GRADING DIRECTIVE:\n"
                            f"Check their solutions step-by-step. If they passed perfectly, congratulate them warmly.\n"
                            f"If they made structural mathematical errors or failed any portion, highlight exactly where the calculation failed, "
                            f"then provide the complete step-by-step markings, calculations, and explanations."
                        )
                        evaluation_result = generate_content(review_prompt, api_key)
                        st.markdown("### 📊 Official Script Evaluation Report")
                        st.info(evaluation_result)
                        
                        # STAGE 3: Unlock the Comprehensive 4-Item Printable Paper after submission
                        with st.spinner("🤖 Compiling your standalone 4-Item Full Length Assessment Paper..."):
                            four_item_prompt = (
                                f"Generate a complete, official standalone educational examination paper for Senior Five {subject_choice} "
                                f"conforming strictly to the new NCDC competence-based curriculum standard guidelines.\n"
                                f"The paper must contain exactly FOUR (4) comprehensive competence scenario questions. "
                                f"Output format: Strictly neat examination layout with instructions and marks distribution. No solutions included."
                            )
                            st.session_state["four_item_paper"] = generate_content(four_item_prompt, api_key)

            # Render the 4-Item Printable Exam Paper if Unlocked
            if st.session_state.get("four_item_paper"):
                st.markdown("---")
                st.markdown("## 🖨️ Printable Full-Length 4-Item Exam Paper")
                st.caption("This standard evaluation paper has been successfully generated for offline review or printing.")
                st.markdown(f'<div style="background-color: #1a1a1a; padding: 25px; border-radius: 5px;" class="print-content">{st.session_state["four_item_paper"]}</div>', unsafe_allow_html=True)
                
                # JavaScript Print Trigger Button
                st.button("🖨️ Open System Print Dialog", on_click=lambda: st.markdown("<script>window.print();</script>", unsafe_allow_html=True))

            # Infinite loop trigger script to update timer display smoothly
            if remaining > 0:
                time.sleep(1)
                st.rerun()

    # PAGE 2: TRUE PEER-TO-PEER MULTIMEDIA SCHOLAR CHAT ROOM (Not a bot chat)
    elif choice == "💬 Study Room Chat":
        display_loading_brand()
        st.title("💬 Shared Scholar Communications Room")
        st.caption("Live Communication Link between Setra Stones and Gideon Cheps")

        # Render message stream
        st.markdown("### 📬 Message Logs")
        for message in st.session_state["p2p_chat_messages"]:
            align_class = "chat-right" if message["sender"] == user else "chat-left"
            st.markdown(f"""
                <div class="chat-bubble {align_class}">
                    <strong>{message['sender']}</strong> <span style='font-size:10px; color:#aaa;'>({message['time']})</span><br>
                    {message['text']}
                </div>
            """, unsafe_allow_html=True)
            
            # Render media parameters if they exist in the data structure
            if "media_file" in message:
                if message["media_type"].startswith("image/"):
                    st.image(message["media_file"])
                elif message["media_type"].startswith("audio/"):
                    st.audio(message["media_file"])
                elif message["media_type"].startswith("video/"):
                    st.video(message["media_file"])
                else:
                    st.download_button("Download Document Attachment", message["media_file"], file_name=message["media_name"])

        st.markdown("---")
        st.subheader("Send Message or Media")
        
        # Inputs layout
        chat_text = st.text_input("Type your message here...", key="chat_input_msg")
        uploaded_media = st.file_uploader("Attach Audio, Videos, Documents, or Images to chat stream:", type=["txt", "pdf", "png", "jpg", "jpeg", "mp3", "wav", "mp4", "mov"])
        
        if st.button("✉️ Broadcast to Scholar Room"):
            timestamp = datetime.datetime.now().strftime("%H:%M")
            if chat_text.strip() != "" or uploaded_media is not None:
                new_msg = {"sender": user, "text": chat_text, "time": timestamp}
                
                if uploaded_media is not None:
                    new_msg["media_file"] = uploaded_media.read()
                    new_msg["media_type"] = uploaded_media.type
                    new_msg["media_name"] = uploaded_media.name
                    if chat_text.strip() == "":
                        new_msg["text"] = f"Shared an attachment: *{uploaded_media.name}*"
                
                st.session_state["p2p_chat_messages"].append(new_msg)
                st.success("Message dispatched.")
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

    # PAGE 4: UPLOAD DIAGRAMS (Strictly uploads diagram to map against Google Sheets question column)
    elif choice == "📂 Upload Diagrams" and user == "Setra stones":
        display_loading_brand()
        st.header("📂 Visual Aid Diagram Mapping Workspace")
        st.subheader("Link Graphic Diagrams directly to Google Sheet Question Texts")
        
        raw_bank = read_public_sheet(subject_choice)
        if raw_bank is not None and not raw_bank.empty:
            col_name = raw_bank.columns[0]
            questions_list = raw_bank[col_name].dropna().tolist()
            
            target_q = st.selectbox("🎯 Select the precise worksheet question text this diagram matches:", questions_list)
            diagram_file = st.file_uploader("Upload the exact structural visual aid diagram (.png, .jpg, .jpeg):", type=["png", "jpg", "jpeg"])
            
            if st.button("🔗 Bind Diagram to Question Column Record"):
                if diagram_file is not None:
                    st.session_state["diagram_vault"][target_q] = diagram_file.read()
                    st.success(f"Successfully bound visual diagram file to question context: '{target_q[:50]}...'")
                else:
                    st.warning("Please upload an image file first.")
        else:
            st.error("Cannot pull row data names to perform graphic mapping configurations.")

    # PAGE 5: VAULT ARCHIVES (Fully visible embedded PDF simulated logs view)
    elif choice == "📁 Vault Archives":
        display_loading_brand()
        st.title("📁 Shared Candidate Vault Repositories")
        st.markdown("### 📄 Accessible Active Document Logs (PDF Format Layout)")
        
        # Display simulated visible layout inside the application frame
        if "twin_questions" in st.session_state:
            st.markdown("#### 📥 Archived Active Twin-Question Component Log")
            with st.container():
                st.markdown(f"""
                    <div style="background-color: white; color: black; padding: 20px; border-radius: 4px; font-family: serif; border: 1px solid #ddd;">
                        <h3 style="text-align: center; color: black; margin:0;">ASP ARCHIVE SYSTEM DOCUMENT REPORT</h3>
                        <hr style="border-color: black;">
                        <p><strong>Subject:</strong> {st.session_state.get('exam_subject', 'STEM Standard')}</p>
                        <p><strong>Generated Text Grid:</strong></p>
                        <div style="font-size: 13px; line-height: 1.5;">{st.session_state['twin_questions']}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.caption("🚨 Document formatted dynamically to follow legal printable paper dimensions inside viewport.")
        else:
            st.info("Vault registry is clean. Generate an exam item inside the portal to populate archives.")
else:
    st.sidebar.warning("Access Denied. Please input valid candidate authentication credentials.")
