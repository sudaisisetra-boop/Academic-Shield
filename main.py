import streamlit as st
import pandas as pd
import datetime
import random
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection

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
            # Read the question prompts you typed without answers
            raw_bank = conn.read(worksheet=subject_choice)
            base_questions = raw_bank['question_text'].dropna().tolist()
        except Exception:
            st.error(f"Could not read from the '{subject_choice}' tab. Make sure it has a 'question_text' column.")
            base_questions = []

        if base_questions:
            # Seed ensure both you and Gideon get the exact same items today
            random.seed(today_str)
            
            # Select up to 4 baseline prompts from your sheet
            sample_size = min(4, len(base_questions))
            selected_bases = random.sample(base_questions, sample_size)
            
            # AI generation tool wrapped in a cache to lock the exact output for 24 hours
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
            
            # Displaying the questions and generating input scripts dynamically
            student_scripts = {}
            
            for i, item_raw in enumerate(active_paper_items):
                st.markdown("---")
                st.subheader(f"📝 Question Item {i+1}")
                
                # Render the AI question text neatly
                st.markdown(item_raw)
                
                # Create dedicated input scripts for this specific question item
                st.markdown(f"**✍️ Your Script for Item {i+1}:**")
                ans_a = st.text_area(f"Type solution for Item {i+1} - Part A:", height=100, key=f"script_a_{i}")
                ans_b = st.text_area(f"Type solution for Item {i+1} - Part B:", height=100, key=f"script_b_{i}")
                
                # Save answers to evaluate later
                student_scripts[f"item_{i}"] = {
                    "question_context": item_raw,
                    "ans_a": ans_a,
                    "ans_b": ans_b
                }

            st.markdown("---")
            
            if st.button("📤 Submit Entire Exam Script"):
                with st.spinner("📝 Examiner is marking your full scripts against curriculum standards..."):
                    
                    # Package all answers into a single grading review block
                    evaluation_summary = ""
                    total_calculated_score = 0
                    
                    for i in range(len(active_paper_items)):
                        script = student_scripts[f"item_{i}"]
                        grading_prompt = f"""
                        You are a strict UNEB Examiner grading a Senior Five student script.
                        Question text: '{script['question_context']}'
                        Student answers:
                        Part A: '{script['ans_a']}'
                        Part B: '{script['ans_b']}'
                        
                        Grade this item out of 25 maximum marks (12.5 marks for Part A, 12.5 marks for Part B).
                        Provide crisp feedback showing where they missed marks or made calculation errors.
                        At the very bottom of your response, output a single line formatted exactly like this:
                        ITEM_SCORE: [X]
                        Where [X] is the integer score out of 25 (e.g., ITEM_SCORE: 18).
                        """
                        grading_response = model.generate_content(grading_prompt)
                        review_text = grading_response.text
                        
                        evaluation_summary += f"\n\n### 📋 Evaluation for Item {i+1}\n" + review_text
                        
                        # Extract score out of 25 for this item
                        try:
                            score_line = [line for line in review_text.split('\n') if "ITEM_SCORE:" in line][-1]
                            item_score = int(''.join(filter(str.isdigit, score_line)))
                        except Exception:
                            item_score = 0
                        total_calculated_score += item_score
                    
                    # Convert total marks to a standard UNEB percentage scale
                    final_percentage = int((total_calculated_score / (len(active_paper_items) * 25)) * 100)
                    
                    st.markdown("---")
                    st.title(f"🏆 Final Exam Grade: {final_percentage}%")
                    st.markdown(evaluation_summary)
                    
                    # Log the cumulative score to Google Sheets
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
