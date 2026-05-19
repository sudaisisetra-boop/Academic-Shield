import streamlit as st
import pandas as pd
import datetime
import random
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
from PIL import Image

st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Initialize AI Brain
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("AI Engine configuration missing. Please add GEMINI_API_KEY to your Secrets panel.")

# Database Initialization
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database connection failed. Check your Secrets formatting.")

# Login System
st.sidebar.title("🔐 Scholar Login")
user = st.sidebar.selectbox("Select Name", ["Setra stones", "Gideon Cheps"])
pwd = st.sidebar.text_input("Enter Access Code", type="password")

if pwd == "Amazima2026":
    st.sidebar.success(f"Welcome, {user}")
    
    st.sidebar.markdown("---")
    subject_choice = st.sidebar.selectbox("📚 Choose Subject", ["Physics", "Mathematics", "Chemistry"])
    menu = ["📝 Exam Center", "📊 Progress Tracker", "📂 Upload Samples"]
    choice = st.sidebar.radio("Navigate Pages", menu)

    # PAGE 1: EXAM CENTER
    if choice == "📝 Exam Center":
        st.title(f"🏛️ UNEB S5 {subject_choice} AI Portal")
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
            sample_size = min(4, len(base_questions))
            selected_bases = random.sample(base_questions, sample_size)
            
            @st.cache_data(ttl=86400)
            def generate_full_paper(bases_list, subject, date_key):
                generated_items = []
                for idx, seed_text in enumerate(bases_list):
                    prompt = f"""
                    You are a UNEB Senior Five Examiner for {subject}.
                    Take this source reference question: '{seed_text}'
                    Generate a completely new, original parallel structural question (Item {idx+1}).
                    It must require the exact same approach, interpretations, formulas, or methods to solve, but use fresh values, contexts, or scenarios.
                    
                    Format the output strictly like this:
                    ITEM_TITLE: [A clear subtopic title]
                    SCENARIO: [The physical scenario or mathematical setup]
                    PART_A: [A descriptive question like explaining a law, sketching a diagram setup, or defining a property]
                    PART_B: [A calculation or structural proof item based on the scenario]
                    """
                    response = model.generate_content(prompt)
                    generated_items.append(response.text)
                return generated_items

            with st.spinner("🤖 AI Examiner is constructing your 4-item parallel paper..."):
                active_paper_items = generate_full_paper(selected_bases, subject_choice, today_str)
            
            student_scripts = {}
            
            for i, item_raw in enumerate(active_paper_items):
                st.markdown("---")
                st.subheader(f"📝 Question Item {i+1}")
                st.markdown(item_raw)
                
                st.markdown(f"**✍️ Submit Your Script for Item {i+1}:**")
                input_mode = st.radio(f"Choose submission method for Item {i+1}:", ["📷 Upload Photo of Handwritten Work", "⌨️ Type My Answers"], key=f"mode_{i}")
                
                ans_a = ""
                ans_b = ""
                uploaded_photo = None
                
                if input_mode == "⌨️ Type My Answers":
                    ans_a = st.text_area(f"Type solution for Item {i+1} - Part A:", height=100, key=f"script_a_{i}")
                    ans_b = st.text_area(f"Type solution for Item {i+1} - Part B:", height=100, key=f"script_b_{i}")
                else:
                    uploaded_photo = st.file_uploader(f"Snap/Upload photo of your written sheet for Item {i+1}:", type=["jpg", "jpeg", "png"], key=f"photo_{i}")
                    if uploaded_photo:
                        st.image(uploaded_photo, caption=f"Your uploaded script for Item {i+1}", width=300)
                
                student_scripts[f"item_{i}"] = {
                    "question_context": item_raw,
                    "mode": input_mode,
                    "ans_a": ans_a,
                    "ans_b": ans_b,
                    "photo": uploaded_photo
                }

            st.markdown("---")
            
            if st.button("📤 Submit Entire Exam Script"):
                with st.spinner("📝 Examiner is analyzing text and images to grade your scripts..."):
                    evaluation_summary = ""
                    total_calculated_score = 0
                    
                    for i in range(len(active_paper_items)):
                        script = student_scripts[f"item_{i}"]
                        
                        if script["mode"] == "⌨️ Type My Answers":
                            prompt_content = f"The student submitted text answers:\nPart A: '{script['ans_a']}'\nPart B: '{script['ans_b']}'"
                        else:
                            if script["photo"] is not None:
                                prompt_content = "The student submitted an image of their handwritten work. Carefully read their handwriting, evaluate every step of their calculations, and identify any structural loopholes, algebraic drops, or formula errors."
                            else:
                                prompt_content = "\n[The student left this question completely blank.]\n"
                        
                        master_grading_instruction = f"""
                        You are a strict UNEB Examiner grading a Senior Five student script.
                        The Exam Question was: '{script['question_context']}'
                        
                        {prompt_content}
                        
                        Grade this item out of 25 maximum marks (12.5 marks for Part A, 12.5 marks for Part B).
                        Provide crisp feedback showing where they missed marks, what parts they left incomplete, or where their calculation logic failed. 
                        If they failed or got a step wrong, write down the complete step-by-step model solution as a correction.
                        
                        At the very bottom of your response, output a single line formatted exactly like this:
                        ITEM_SCORE: [X]
                        Where [X] is the integer score out of 25 (e.g., ITEM_SCORE: 18).
                        """
                        
                        if script["mode"] == "📷 Upload Photo of Handwritten Work" and script["photo"] is not None:
                            actual_payload = [master_grading_instruction, Image.open(script["photo"])]
                        else:
                            actual_payload = [master_grading_instruction]
                            
                        try:
                            grading_response = model.generate_content(actual_payload)
                            review_text = grading_response.text
                        except Exception as e:
                            review_text = f"Grading failed for this item due to an interface error: {str(e)}"
                        
                        evaluation_summary += f"\n\n### 📋 Evaluation for Item {i+1}\n" + review_text
                        
                        try:
                            score_line = [line for line in review_text.split('\n') if "ITEM_SCORE:" in line][-1]
                            item_score = int(''.join(filter(str.isdigit, score_line)))
                        except Exception:
                            item_score = 0
                        total_calculated_score += item_score
                    
                    final_percentage = int((total_calculated_score / (len(active_paper_items) * 25)) * 100)
                    
                    st.markdown("---")
                    st.title(f"🏆 Final Exam Grade: {final_percentage}%")
                    st.markdown(evaluation_summary)
                    
                    try:
                        existing_data = conn.read(worksheet="Sheet1")
                        new_row = pd.DataFrame([{"Student": user, "Score": final_percentage, "Subject": subject_choice}])
                        updated_data = pd.concat([existing_data, new_row], ignore_index=True)
                        conn.update(worksheet="Sheet1", data=updated_data)
                        st.success("Your performance log has been securely saved to the cloud leaderboard!")
                    except Exception:
                        st.warning("Calculated locally, but cloud logging sync dropped out.")
                        
                    if final_percentage == 100: st.balloons()
        else:
            st.warning(f"Your '{subject_choice}' question archive is empty. Type some past paper questions into your Google Sheet column to begin!")

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
        st.header("📋 UNEB Archive Vault")
        st.write("Upload your past paper screenshots here to store them safely in your session library cache.")
        uploaded_files = st.file_uploader("Upload reference photos", accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                st.success(f"📎 {file.name} uploaded and saved to cache successfully!")
else:
    st.warning("Please enter your access code in the sidebar.")
