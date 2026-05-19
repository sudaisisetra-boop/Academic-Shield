import streamlit as st
import pandas as pd
import datetime
import random
import os
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

# Local Directory Setup for Permanent Storage Vault
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
    menu = ["📝 Exam Center", "📊 Progress Tracker", "📂 Upload Samples", "📁 Vault Archives"]
    choice = st.sidebar.radio("Navigate Pages", menu)

    # PAGE 1: EXAM CENTER
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
            # Anchor seed so both candidates get identical items today
            random.seed(today_str)
            selected_single_base = random.choice(base_questions)
            
            @st.cache_data(ttl=86400)
            def generate_competence_paper(seed_text, subject, date_key):
                prompt = f"""
                You are a senior expert examiner for the Uganda National Examinations Board (UNEB), specialized in the New Competence-Based Curriculum standards for Senior Five {subject}.
                
                Take this single reference question: '{seed_text}'
                
                Based ONLY on that single scenario/topic, generate exactly TWO distinct, interconnected parallel questions (Question 1 and Question 2). 
                Both questions must require the exact same structural approach, interpretation, and method to solve as the original, but set within a fresh real-world Ugandan context or scenario.
                
                CRUCIAL Competence Requirement: You must include a structured text-based visual matrix, diagrammatic sketch setup, or data table layout inside the scenario block to act as a visual aid/support material for the student, matching the modern integration-style assessment items.
                
                Format the output strictly like this:
                ### 📄 MAIN COMPETENCE SCENARIO
                [Insert the fresh scenario description here]
                
                ### 📊 VISUAL AID / SETUP SUPPORT MATERIAL
                [Provide a highly detailed text diagram, coordinate blueprint layout, configuration layout, or structured data matrix here to guide their calculations]
                
                ### 📝 QUESTION 1 (Theory, Interpretation & Application)
                [A high-order application question requiring explanation, derivation of laws, or structural analysis based on the scenario above]
                
                ### 🧮 QUESTION 2 (Structural Calculation & Proof)
                [A multi-step calculation or technical proof item using numbers or variables extracted from the scenario and visual setup]
                """
                response = model.generate_content(prompt)
                return response.text

            with st.spinner("🤖 AI Examiner is constructing your 2-item competence paper..."):
                active_paper_text = generate_competence_paper(selected_single_base, subject_choice, today_str)
            
            st.markdown("---")
            st.markdown(active_paper_text)
            st.markdown("---")
            
            # Submission Interface
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
                    uploaded_photo_1 = st.file_uploader("Snap/Upload script for Question 1:", type=["jpg", "jpeg", "png"], key="exam_p1")
                    if uploaded_photo_1:
                        st.image(uploaded_photo_1, caption="Question 1 Submission Preview", width=250)
                with col2:
                    uploaded_photo_2 = st.file_uploader("Snap/Upload script for Question 2:", type=["jpg", "jpeg", "png"], key="exam_p2")
                    if uploaded_photo_2:
                        st.image(uploaded_photo_2, caption="Question 2 Submission Preview", width=250)

            st.markdown("---")
            
            if st.button("📤 Submit Competence Script to Cloud Vault"):
                with st.spinner("📝 Examiner is processing text, archiving files, and running evaluations..."):
                    
                    # Permanent Image Storage Protocol
                    # Saves images to local app environment system cache so they survive across user screens
                    if uploaded_photo_1 is not None:
                        img1 = Image.open(uploaded_photo_1)
                        img1.save(os.path.join(VAULT_DIR, f"{today_str}_{user}_{subject_choice}_Q1.png"))
                    if uploaded_photo_2 is not None:
                        img2 = Image.open(uploaded_photo_2)
                        img2.save(os.path.join(VAULT_DIR, f"{today_str}_{user}_{subject_choice}_Q2.png"))
                    
                    # Build Grading Packets
                    if input_mode == "⌨️ Type My Answers":
                        payload_content = f"Student Written Answers:\nQuestion 1: {ans_text_1}\nQuestion 2: {ans_text_2}"
                        ai_payload = [payload_content]
                    else:
                        payload_content = "The student submitted handwritten work snapshots. Carefully look at the handwriting and verify their mathematical loopholes and steps."
                        ai_payload = [payload_content]
                        if uploaded_photo_1 is not None: ai_payload.append(Image.open(uploaded_photo_1))
                        if uploaded_photo_2 is not None: ai_payload.append(Image.open(uploaded_photo_2))
                    
                    master_grading_instruction = f"""
                    You are a strict UNEB Senior Five Examiner grading a Competence-Based Assessment.
                    Exam Script Context: {active_paper_text}
                    
                    Analyze their submission thoroughly out of 50 total marks (25 marks per item).
                    Identify structural loopholes, mathematical or formula drops, and conceptual errors.
                    If they fail or get a calculation wrong, print out the complete step-by-step correction marking guide.
                    
                    At the very end of your review, output this exact phrase line:
                    FINAL_PERCENTAGE: [X]
                    Where [X] is the overall combined integer percentage from 0 to 100.
                    """
                    ai_payload.insert(0, master_grading_instruction)
                    
                    try:
                        grading_response = model.generate_content(ai_payload)
                        evaluation = grading_response.text
                    except Exception as e:
                        evaluation = f"Grading process timed out or encountered an issue: {str(e)}"
                    
                    try:
                        score_line = [line for line in evaluation.split('\n') if "FINAL_PERCENTAGE:" in line][-1]
                        final_grade = int(''.join(filter(str.isdigit, score_line)))
                    except Exception:
                        final_grade = 0
                        
                    st.markdown("---")
                    st.title(f"🏆 Score: {final_grade}%")
                    st.markdown(evaluation)
                    
                    # Save performance metrics to Leaderboard
                    try:
                        existing_data = conn.read(worksheet="Sheet1")
                        new_row = pd.DataFrame([{"Student": user, "Score": final_grade, "Subject": subject_choice}])
                        updated_data = pd.concat([existing_data, new_row], ignore_index=True)
                        conn.update(worksheet="Sheet1", data=updated_data)
                        st.success("Exam logged and synchronization finalized across the cloud leaderboard!")
                    except Exception:
                        st.warning("Evaluated successfully, but cloud database writing dropped out.")
                        
                    if final_grade == 100: st.balloons()
        else:
            st.warning(f"Your '{subject_choice}' question repository is empty. Add a single baseline row to start!")

    # PAGE 2: PROGRESS TRACKER
    elif choice == "📊 Progress Tracker":
        st.header("📊 Global Leaderboard (Live Cloud Data)")
        try:
            df = conn.read(worksheet="Sheet1")
            st.table(df)
        except Exception:
            st.write("No entries recorded in the cloud database yet.")

    # PAGE 3: UPLOAD SAMPLES
    elif choice == "📂 Upload Samples":
        st.header("📋 UNEB Reference Sample Vault")
        st.write("Upload source reference materials or diagram diagrams here. These are saved permanently into the system library directory.")
        
        sample_file = st.file_uploader("Upload reference visual/past paper layout:", type=["jpg", "jpeg", "png", "pdf"])
        if sample_file:
            # Save past paper samples permanently into archive directory
            file_path = os.path.join(VAULT_DIR, f"SAMPLE_{subject_choice}_{sample_file.name}")
            with open(file_path, "wb") as f:
                f.write(sample_file.getbuffer())
            st.success(f"📎 Reference item '{sample_file.name}' saved permanently to cloud memory archive!")

    # PAGE 4: VAULT ARCHIVES (The new comparison library)
    elif choice == "📁 Vault Archives":
        st.title("📁 Shared Candidate Vault Archives")
        st.write("Review past session question samples and view your partner's handwritten scripts and working methods side-by-side.")
        
        st.markdown("---")
        if os.path.exists(VAULT_DIR):
            all_archived_files = os.listdir(VAULT_DIR)
            if all_archived_files:
                st.subheader("🗄️ Available Archive Inventories")
                
                # Filter categories for easy view on mobile screen
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
                st.info("The storage vaults are currently empty. Complete an exam or upload a reference paper to view logs.")
        else:
            st.info("No archive tracks recorded yet.")
else:
    st.warning("Please enter your access code in the sidebar.")
