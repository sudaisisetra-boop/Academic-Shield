import streamlit as st
import pandas as pd
import datetime
import random
import os
import base64
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
from PIL import Image

st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Initialize AI Brain
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("AI Engine configuration missing. Check the very first line of your Secrets panel.")

# Database Initialization
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database connection failed. Check your Secrets formatting.")

# Local Storage Directory Setup
VAULT_DIR = "vault_archive"
if not os.path.exists(VAULT_DIR):
    os.makedirs(VAULT_DIR)

# Login System
st.sidebar.title("🔐 Scholar Login")
user = st.sidebar.selectbox("Select Name", ["Setra stones", "Gideon Cheps"])
pwd = st.sidebar.text_input("Enter Access Code", type="password")

if pwd == "Amazima2026":
    st.sidebar.success(f"Welcome, {user}")
    st.sidebar.markdown("---")
    
    subject_choice = st.sidebar.selectbox("📚 Choose Subject", ["Physics", "Mathematics", "Chemistry"])
    menu = ["📝 Exam Center", "💬 Study Room Chat", "📊 Progress Tracker", "📂 Upload Samples", "📁 Vault Archives"]
    choice = st.sidebar.radio("Navigate Pages", menu)

    # PAGE 1: EXAM CENTER (Upgraded with Competence Freedom)
    if choice == "📝 Exam Center":
        st.title(f"🏛️ UNEB S5 {subject_choice} Competence Portal")
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        st.caption(f"📅 Daily Synchronized Session: **{today_str}**")

        try:
            raw_bank = conn.read(worksheet=subject_choice)
            base_questions = raw_bank['question_text'].dropna().tolist()
        except Exception:
            st.error(f"Could not read from the '{subject_choice}' tab. Make sure it has a 'question_text' column.")
            base_questions = []

        if base_questions:
            random.seed(today_str)
            selected_single_base = random.choice(base_questions)
            
            @st.cache_data(ttl=86400)
            def generate_competence_paper(seed_text, subject, date_key):
                prompt = f"""
                You are a senior expert examiner for the Uganda National Examinations Board (UNEB), specialized in the New Competence-Based Curriculum standards for Senior Five {subject}.
                Take this single reference question scenario: '{seed_text}'
                Based ONLY on that single topic, generate exactly TWO distinct, interconnected parallel questions (Question 1 and Question 2) using a fresh real-world Ugandan context.
                
                CRUCIAL Competence Evaluation Rule: 
                Depending on the nature of the topic, dynamically decide the best assessment structure:
                - MODE A (Visual Aid provided): Include a structured text-based visual layout, geometric sketch layout, or data matrix to support their calculation.
                - MODE B (Student Illustration required): Do NOT provide a visual layout. Instead, explicitly structure one of the questions to require the student to draw, sketch, or map out a labeled technical illustration/diagram based on the scenario, as this must contribute to their overall score.
                
                Format the output strictly like this:
                ### 📄 MAIN COMPETENCE SCENARIO
                [Insert the fresh scenario description here]
                
                ### 📊 VISUAL DESIGN / ASSESSMENT MODE
                [State clearly whether a visual matrix is provided below, or if the student is strictly required to draw/illustrate an answer chart manually]
                
                ### 📝 QUESTION 1 (Theory, Interpretation & Application)
                [An application question requiring explanation, derivation, or a mandatory command to sketch/label a technical layout setup if running Mode B]
                
                ### 🧮 QUESTION 2 (Structural Calculation & Proof)
                [A multi-step calculation or technical proof item using numbers or parameters extracted from the scenario]
                """
                response = model.generate_content(prompt)
                return response.text

            with st.spinner("🤖 AI Examiner is constructing your 2-item competence paper..."):
                active_paper_text = generate_competence_paper(selected_single_base, subject_choice, today_str)
            
            st.markdown("---")
            st.markdown(active_paper_text)
            st.markdown("---")
            
            st.subheader("✍️ Your Examination Submission Script")
            input_mode = st.radio("Choose how you want to submit your scripts today:", ["📷 Upload Photo of Handwritten Work", "⌨️ Type My Answers"])
            
            ans_text_1 = ""
            ans_text_2 = ""
            uploaded_photo_1 = None
            uploaded_photo_2 = None
            
            if input_mode == "⌨️ Type My Answers":
                ans_text_1 = st.text_area("Type your solution for Question 1:", height=150)
                ans_text_2 = st.text_area("Type your solution for Question 2:", height=150)
            else:
                col1, col2 = st.columns(2)
                with col1:
                    uploaded_photo_1 = st.file_uploader("Snap/Upload script for Question 1 (Including drawings):", type=["jpg", "jpeg", "png"], key="exam_p1")
                    if uploaded_photo_1: st.image(uploaded_photo_1, width=250)
                with col2:
                    uploaded_photo_2 = st.file_uploader("Snap/Upload script for Question 2:", type=["jpg", "jpeg", "png"], key="exam_p2")
                    if uploaded_photo_2: st.image(uploaded_photo_2, width=250)

            if st.button("📤 Submit Competence Script to Cloud Vault"):
                with st.spinner("📝 Examiner is evaluating your calculations and diagrams..."):
                    if uploaded_photo_1 is not None:
                        Image.open(uploaded_photo_1).save(os.path.join(VAULT_DIR, f"{today_str}_{user}_{subject_choice}_Q1.png"))
                    if uploaded_photo_2 is not None:
                        Image.open(uploaded_photo_2).save(os.path.join(VAULT_DIR, f"{today_str}_{user}_{subject_choice}_Q2.png"))
                    
                    if input_mode == "⌨️ Type My Answers":
                        ai_payload = [f"Student Written Answers:\nQuestion 1: {ans_text_1}\nQuestion 2: {ans_text_2}"]
                    else:
                        ai_payload = ["The student submitted handwritten work snapshots. Carefully inspect handwriting, equations, structural layout methods, and geometric sketches."]
                        if uploaded_photo_1 is not None: ai_payload.append(Image.open(uploaded_photo_1))
                        if uploaded_photo_2 is not None: ai_payload.append(Image.open(uploaded_photo_2))
                    
                    master_grading_instruction = f"""
                    You are a strict UNEB Senior Five Examiner grading a Competence-Based Assessment out of 50 total marks (25 marks per item).
                    Exam Context: {active_paper_text}
                    If a sketch or illustration was demanded by the question, carefully inspect the student's drawing for accuracy, proper scaling/labels, and correctness.
                    Provide detailed constructive critique and step-by-step corrections for missed marks.
                    At the very end of your review, output this exact line:
                    FINAL_PERCENTAGE: [X]
                    """
                    ai_payload.insert(0, master_grading_instruction)
                    
                    try:
                        grading_response = model.generate_content(ai_payload)
                        evaluation = grading_response.text
                    except Exception as e:
                        evaluation = f"Grading process encountered an issue: {str(e)}"
                    
                    try:
                        score_line = [line for line in evaluation.split('\n') if "FINAL_PERCENTAGE:" in line][-1]
                        final_grade = int(''.join(filter(str.isdigit, score_line)))
                    except Exception:
                        final_grade = 0
                        
                    st.markdown("---")
                    st.title(f"🏆 Score: {final_grade}%")
                    st.markdown(evaluation)
                    
                    try:
                        existing_data = conn.read(worksheet="Sheet1")
                        new_row = pd.DataFrame([{"Student": user, "Score": final_grade, "Subject": subject_choice}])
                        conn.update(worksheet="Sheet1", data=pd.concat([existing_data, new_row], ignore_index=True))
                        st.success("Exam logged to cloud leaderboard!")
                    except Exception:
                        st.warning("Evaluated locally, sync dropped out.")
        else:
            st.warning(f"Your '{subject_choice}' question repository is empty. Add a single baseline row to start!")

    # PAGE 2: BRAND NEW MULTIMEDIA STUDY ROOM CHAT
    elif choice == "💬 Study Room Chat":
        st.title("💬 Real-Time Scholar Study Room")
        st.caption("Communicate live during exams, leave voice notes, share diagrams, or drop reference PDFs.")
        
        # Pull chat logs from Google Sheet to retain permanent message history
        try:
            chat_df = conn.read(worksheet="ChatLog")
        except Exception:
            # Create tab automatically if missing
            chat_df = pd.DataFrame(columns=["Timestamp", "Sender", "Text", "MediaType", "MediaData", "FileName"])

        # Display Existing Messages Flow
        st.markdown("---")
        for idx, row in chat_df.tail(30).iterrows():
            with st.chat_message("user" if row["Sender"] == user else "assistant"):
                st.markdown(f"**{row['Sender']}** <span style='font-size:11px; color:gray;'>({row['Timestamp']})</span>", unsafe_allow_html=True)
                if pd.notna(row["Text"]) and str(row["Text"]).strip() != "":
                    st.write(row["Text"])
                
                # Render Media Elements if present
                if pd.notna(row["MediaType"]) and pd.notna(row["MediaData"]):
                    m_type = row["MediaType"]
                    m_data = base64.b64decode(row["MediaData"])
                    f_name = row["FileName"] if pd.notna(row["FileName"]) else "file"
                    
                    if m_type == "Image":
                        st.image(m_data, width=300)
                    elif m_type == "Audio":
                        st.audio(m_data)
                    elif m_type == "Video":
                        st.video(m_data)
                    elif m_type == "Document":
                        st.download_button(f"📥 Download {f_name}", m_data, file_name=f_name)
        st.markdown("---")

        # Message Input Panel Layout
        with st.form("chat_form", clear_on_submit=True):
            msg_text = st.text_input("Type text or insert emojis here...")
            
            st.markdown("<p style='font-size:12px; color:gray; margin-bottom:2px;'>📁 Attach Media Attachment (Voice Note, Photo, Video, or Document PDF)</p>", unsafe_allow_html=True)
            attached_file = st.file_uploader("Upload attachment", type=["jpg", "jpeg", "png", "mp3", "wav", "m4a", "mp4", "pdf", "docx", "txt"], label_visibility="collapsed")
            
            submit_msg = st.form_submit_button("🚀 Send Message")
            
            if submit_msg:
                if msg_text.strip() != "" or attached_file is not None:
                    timestamp_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    media_type = "None"
                    encoded_string = ""
                    filename = ""
                    
                    if attached_file is not None:
                        filename = attached_file.name
                        file_ext = filename.split(".")[-1].lower()
                        encoded_string = base64.b64encode(attached_file.read()).decode("utf-8")
                        
                        if file_ext in ["jpg", "jpeg", "png"]: media_type = "Image"
                        elif file_ext in ["mp3", "wav", "m4a"]: media_type = "Audio"
                        elif file_ext in ["mp4"]: media_type = "Video"
                        else: media_type = "Document"
                    
                    new_msg = pd.DataFrame([{
                        "Timestamp": timestamp_now,
                        "Sender": user,
                        "Text": msg_text,
                        "MediaType": media_type,
                        "MediaData": encoded_string,
                        "FileName": filename
                    }])
                    
                    try:
                        updated_chat = pd.concat([chat_df, new_msg], ignore_index=True)
                        conn.update(worksheet="ChatLog", data=updated_chat)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to log message to cloud channel: {str(e)}")

    # PAGE 3: PROGRESS TRACKER
    elif choice == "📊 Progress Tracker":
        st.header("📊 Global Leaderboard (Live Cloud Data)")
        try:
            st.table(conn.read(worksheet="Sheet1"))
        except Exception:
            st.write("No entries recorded in the cloud database yet.")

    # PAGE 4: UPLOAD SAMPLES
    elif choice == "📂 Upload Samples":
        st.header("📋 UNEB Reference Sample Vault")
        sample_file = st.file_uploader("Upload reference visual/past paper layout:", type=["jpg", "jpeg", "png", "pdf"])
        if sample_file:
            with open(os.path.join(VAULT_DIR, f"SAMPLE_{subject_choice}_{sample_file.name}"), "wb") as f:
                f.write(sample_file.getbuffer())
            st.success(f"📎 Reference item '{sample_file.name}' saved permanently to cloud memory archive!")

    # PAGE 5: VAULT ARCHIVES
    elif choice == "📁 Vault Archives":
        st.title("📁 Shared Candidate Vault Archives")
        if os.path.exists(VAULT_DIR):
            all_archived_files = os.listdir(VAULT_DIR)
            if all_archived_files:
                view_mode = st.selectbox("Filter Vault Files By Type", ["Show Exam Script Submissions", "Show Uploaded Reference Sample Papers"])
                for file_name in all_archived_files:
                    full_file_path = os.path.join(VAULT_DIR, file_name)
                    if view_mode == "Show Exam Script Submissions" and not file_name.startswith("SAMPLE_"):
                        st.markdown(f"**📝 Script Record:** `{file_name}`")
                        st.image(full_file_path, width=400)
                        st.markdown("---")
                    elif view_mode == "Show Uploaded Reference Sample Papers" and file_name.startswith("SAMPLE_"):
                        st.markdown(f"**📐 Reference Source Paper:** `{file_name.replace('SAMPLE_', '')}`")
                        st.image(full_file_path, width=400)
                        st.markdown("---")
            else:
                st.info("The storage vaults are currently empty.")
        else:
            st.info("No archive tracks recorded yet.")
else:
    st.warning("Please enter your access code in the sidebar.")
