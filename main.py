import streamlit as st
import pandas as pd
import datetime
import random
import os
import json
import time

# =========================================================================
# 1. PLATFORM CONFIGURATIONS, SECURITY HEADERS & VISUAL STYLING
# =========================================================================
st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

st.markdown("""
    <head>
        <link rel="manifest" href="manifest.json">
        <meta name="theme-color" content="#ff3333">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    </head>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .timer-container {
        background-color: #111111;
        padding: 14px;
        border-radius: 8px;
        border: 2px solid #ff3333;
        text-align: center;
        margin-bottom: 15px;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        background-color: #0b141a; 
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .chat-bubble {
        padding: 10px 14px;
        border-radius: 12px;
        margin-bottom: 8px;
        max-width: 75%;
        font-family: sans-serif;
        font-size: 14px;
        line-height: 1.4;
    }
    .chat-left { background-color: #202c33; color: #e9edef; margin-right: auto; text-align: left; border-top-left-radius: 0px;}
    .chat-right { background-color: #005c4b; color: #e9edef; margin-left: auto; text-align: left; border-top-right-radius: 0px;}
    .system-warn-box { background-color: #3b1111; border: 2px solid #ff3333; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #ff9999; font-weight: bold;}
    .top-profile-pic { border-radius: 50%; border: 2px solid #ff3333; object-fit: cover; width: 55px; height: 55px; }
    .admin-broadcast-banner { background-color: #ff3333; color: white; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    div.stButton > button { width: 100% !important; font-weight: bold !important; background-color: #1e1e1e !important; color: #ffffff !important; border: 1px solid #444444 !important; border-radius: 4px !important; }
    div.stButton > button:hover { background-color: #ff3333 !important; color: white !important; border-color: #ff3333 !important; }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# 2. OFFICIAL NATIONAL CURRICULUM DIRECTORY MAP (NCDC STANDARDS)
# =========================================================================
NCDC_CURRICULUM_MAP = {
    "Mathematics": ["Numerical Concepts", "Equations and Inequalities", "Coordinate Geometry 1", "Partial Fractions", "Trigonometry", "Descriptive Statistics", "Vectors", "Differentiation 1", "Integration 1", "Complex Numbers", "Differential Equations"],
    "Physics": ["Measurement and Dimensions", "Statics", "Linear Motion", "Fluid Mechanics", "Mechanical Properties of Matter", "Thermometry", "Heat Quantities", "Electrostatics", "Capacitors"],
    "Chemistry": ["Moles and Equations", "Atomic and Electronic Structure", "Bonding and Structure", "Periodicity I", "Thermochemistry", "Organic Chemistry I", "Equilibria I", "Electrochemistry"],
    "Biology": ["Cell Biology", "Nutrition", "Transport", "Respiration", "Homeostasis", "Coordination", "Ecology"]
}

SUDAISI_IMAGE_STREAM = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=200"
AVATAR_OPTIONS = [
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    "https://cdn-icons-png.flaticon.com/512/4140/4140037.png",
    "https://cdn-icons-png.flaticon.com/512/4140/4140048.png"
]

if "SHEET_ID" in st.secrets:
    SHEET_ID = st.secrets["SHEET_ID"]
else:
    SHEET_ID = "1xU80PotVALVM3sWt7PS3kLGbsivqzMvznXq0c8Cu44M"

def read_public_sheet(worksheet_name):
    export_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={worksheet_name.strip()}"
    try:
        df = pd.read_csv(export_url)
        return df if (df is not None and not df.empty) else None
    except Exception:
        return None

def save_cache_to_disk(filename, data):
    try:
        with open(filename, "w") as f: json.dump(data, f, default=str)
    except Exception: pass

def load_cache_from_disk(filename, default_val):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f: return json.load(f)
        except Exception: pass
    return default_val

# =========================================================================
# 3. CRITICAL PERSISTENCE STORAGE ENGINE & DATABASE SYSTEM MIRRORS
# =========================================================================
if "users_registry" not in st.session_state:
    st.session_state["users_registry"] = load_cache_from_disk("db_users.json", {
        "0000": {"username": "Admin", "pwd": "SudaisiAdmin2026", "name": "Sudaisi Setra", "class": "Senior Five", "school": "St Marys", "phone": "0752047103", "email": "admin@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry", "Biology"], "status": "Approved", "warning_msg": "", "avatar": "SUDAISI_BAKED", "partner": ""},
        "6601": {"username": "Setra stones", "pwd": "Amazima2026", "name": "Setra Stones", "class": "Senior Five", "school": "St Marys", "phone": "0752047103", "email": "setra@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry"], "status": "Approved", "warning_msg": "Initial warning template look.", "avatar": AVATAR_OPTIONS[0], "partner": ""}
    })

if "pending_registrations" not in st.session_state: st.session_state["pending_registrations"] = load_cache_from_disk("db_pending.json", [])
if "general_chat" not in st.session_state: st.session_state["general_chat"] = load_cache_from_disk("db_genchat.json", [])
if "private_chats" not in st.session_state: st.session_state["private_chats"] = load_cache_from_disk("db_p2pchat.json", [])
if "suggestions" not in st.session_state: st.session_state["suggestions"] = load_cache_from_disk("db_suggestions.json", [])
if "global_alerts" not in st.session_state: st.session_state["global_alerts"] = load_cache_from_disk("db_alerts.json", ["🚀 Platform Online. Secure Mirror Systems Functional."])
if "exam_vault" not in st.session_state: st.session_state["exam_vault"] = load_cache_from_disk("db_exams.json", {})
if "last_read_tracker" not in st.session_state: st.session_state["last_read_tracker"] = load_cache_from_disk("db_readtrack.json", {})
if "generated_registration_codes" not in st.session_state: st.session_state["generated_registration_codes"] = load_cache_from_disk("db_regcodes.json", ["SHIELD2026", "ASP2026"])

# =========================================================================
# 4. GLOBAL AUTHENTICATION & SECURITY STATE SYNC
# =========================================================================
is_authenticated = False
session_user = ""
session_uid = ""
session_class = "Senior Five"
session_partner = ""
allowed_subjects = ["Mathematics", "Physics", "Chemistry"]
current_avatar_url = AVATAR_OPTIONS[0]
user_account_status = "Approved"
account_warning_text = ""

st.sidebar.title("🔐 ASP Access Interface")
app_mode = st.sidebar.radio("Select Portal Target Module", ["Login Page Panel", "Registration Terminal", "System Administrator Hub"])

if app_mode == "Login Page Panel":
    st.sidebar.subheader("🔒 Enter Active Credentials")
    login_uid = st.sidebar.text_input("User ID Code Token:")
    login_user = st.sidebar.text_input("Username:")
    login_pwd = st.sidebar.text_input("Password:", type="password")
    
    if login_uid == "0000" and login_user == "Admin" and login_pwd == "SudaisiAdmin2026":
        is_authenticated = True
        session_user = "Admin"
        session_uid = "0000"
        session_class = "Senior Five"
        session_partner = ""
        allowed_subjects = ["Mathematics", "Physics", "Chemistry", "Biology"]
        current_avatar_url = "SUDAISI_BAKED"
        user_account_status = "Approved"
    elif login_uid in st.session_state["users_registry"]:
        node = st.session_state["users_registry"][login_uid]
        if node["username"] == login_user and node["pwd"] == login_pwd:
            user_account_status = node.get("status", "Approved")
            account_warning_text = node.get("warning_msg", "")
            
            if user_account_status in ["Banned", "Locked"]:
                st.sidebar.error("❌ Access Terminated! Contact administration lines.")
            else:
                is_authenticated = True
                session_user = login_user
                session_uid = login_uid
                session_class = node.get("class", "Senior Five")
                session_partner = node.get("partner", "")
                allowed_subjects = node["subjects"]
                current_avatar_url = node.get("avatar", AVATAR_OPTIONS[0])

col_head_title, col_head_pic = st.columns([11, 1])
with col_head_title:
    st.markdown("<h2 style='color:#ff3333; margin:0;'>🛡️ Academic Shield Pro</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#aaaaaa; font-style:italic; margin:0;'>“Conceptual Mastery Terminal Engine”</h5>", unsafe_allow_html=True)

with col_head_pic:
    if session_user == "Admin" or current_avatar_url == "SUDAISI_BAKED":
        st.markdown(f'<img src="{SUDAISI_IMAGE_STREAM}" class="top-profile-pic"/>', unsafe_allow_html=True)
    else:
        st.markdown(f'<img src="{current_avatar_url}" class="top-profile-pic"/>', unsafe_allow_html=True)

# =========================================================================
# MODULE A: REGISTRATION TERMINAL
# =========================================================================
if app_mode == "Registration Terminal":
    st.subheader("📋 Student Account Registration Desk")
    st.info("Notice: Send activation confirmation fee of 2000 UGX to mobile money line 0752047103 to process loops.")
    
    reg_user = st.text_input("Choose Unique Account Username:")
    reg_pwd = st.text_input("Choose Password:", type="password")
    reg_name = st.text_input("Full Legal Student Name:")
    reg_class = st.selectbox("Class Grade Level:", ["Senior Four", "Senior Five", "Senior Six"])
    reg_school = st.text_input("Current School Name:")
    reg_phone = st.text_input("Phone Contact Number:")
    reg_email = st.text_input("Email Address:")
    reg_gender = st.selectbox("Gender:", ["Male", "Female"])
    reg_town = st.text_input("Location (Current District):")
    
    st.markdown("#### 📚 Combination Core Subjects (Pick Exactly 3 Subjects)")
    sub_m = st.checkbox("Mathematics")
    sub_p = st.checkbox("Physics")
    sub_c = st.checkbox("Chemistry")
    sub_b = st.checkbox("Biology")
    
    reg_code_input = st.text_input("Enter Registration Code:")
    
    if st.button("🚀 Transmit Registration Payload"):
        chosen = []
        if sub_m: chosen.append("Mathematics")
        if sub_p: chosen.append("Physics")
        if sub_c: chosen.append("Chemistry")
        if sub_b: chosen.append("Biology")
        
        if len(chosen) != 3:
            st.error("❌ System Requirement: You must select exactly 3 combination subjects.")
        elif reg_code_input.strip() not in st.session_state["generated_registration_codes"]:
            st.error("❌ Invalid Code. Complete your payment check loops.")
        elif not reg_user or not reg_pwd:
            st.error("❌ Missing Data Fields.")
        else:
            new_request = {
                "username": reg_user, "pwd": reg_pwd, "name": reg_name, "class": reg_class,
                "school": reg_school, "phone": reg_phone, "email": reg_email, "gender": reg_gender,
                "location": reg_town, "subjects": chosen, "reg_code": reg_code_input,
                "avatar": AVATAR_OPTIONS[0], "partner": "", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            }
            st.session_state["pending_registrations"].append(new_request)
            save_cache_to_disk("db_pending.json", st.session_state["pending_registrations"])
            st.success("✔ Payload captured! Awaiting Admin activation check.")

# =========================================================================
# MODULE B: LOGIN PAGE PANEL & CLIENT WORKSPACE (MAIN ENGINE HUB)
# =========================================================================
elif app_mode == "Login Page Panel":
    if not is_authenticated:
        st.markdown("<div style='text-align:center; margin-top:12%;'><h3>🛡️ ASP PORTAL SECURITY SCREEN</h3><p>Provide your configuration logs inside the left side interface panel to access your workspace channels.</p></div>", unsafe_allow_html=True)
    else:
        if account_warning_text:
            st.markdown(f'<div class="system-warn-box">⚠️ <strong>SYSTEM ADMIN WARNING FLAG:</strong> {account_warning_text}</div>', unsafe_allow_html=True)
            
        if st.session_state["global_alerts"]:
            st.markdown(f'<div class="admin-broadcast-banner">📢 BROADCAST: {st.session_state["global_alerts"][-1]}</div>', unsafe_allow_html=True)

        u_last = st.session_state["last_read_tracker"].get(session_user, "1970-01-01 00:00:00")
        unread_p2p_cnt = sum(1 for m in st.session_state["private_chats"] if m.get("to") == session_user and m.get("timestamp", "") > u_last)
        unread_gen_cnt = sum(1 for m in st.session_state["general_chat"] if m.get("sender") != session_user and m.get("timestamp", "") > u_last)
        
        p2p_badge = f"🟢 {unread_p2p_cnt}" if unread_p2p_cnt > 0 else ""
        gen_badge = f"💬 {unread_gen_cnt}" if unread_gen_cnt > 0 else ""
        
        selected_subject = st.sidebar.selectbox("📚 Select Academic Subject Field", allowed_subjects)
        
        client_tab_choice = st.sidebar.radio("Workspace Channels", [
            "📝 Access Exam Center", 
            "🤝 Partner Connection Hub", 
            f"🌐 General Lounge Chat {gen_badge}", 
            f"🔒 Private Peer Chatroom {p2p_badge}", 
            "📊 Progress Tracker Logs", 
            "📁 Finished Exam Vault", 
            "🔑 Change Account Password", 
            "📩 Submit App Suggestions"
        ])

        # =========================================================================
        # UPGRADED HIGH-STANDARD EXAM EVALUATION CENTER
        # =========================================================================
        if client_tab_choice == "📝 Access Exam Center":
            st.title("📝 Precision Topic Exam Center")
            
            if f"exam_active_{session_uid}" not in st.session_state:
                st.session_state[f"exam_active_{session_uid}"] = False

            if not st.session_state[f"exam_active_{session_uid}"]:
                st.markdown("### 🛑 Security Access Gateway Check")
                st.info("Exam questions are safely concealed. Confirm authorization parameters below to display items.")
                if st.button("👉 YES, I am here to take a test!"):
                    st.session_state[f"exam_active_{session_uid}"] = True
                    st.session_state[f"exam_start_{session_uid}"] = datetime.datetime.now().strftime("%I:%M:%S %p")
                    st.rerun()
            else:
                st.markdown(f"""
                    <div class='timer-container'>
                        <span style='color:#ff3333; font-size:18px; font-weight:bold;'>Started at: {st.session_state[f'exam_start_{session_uid}']}</span><br>
                        <span style='color:#ffffff; font-size:13px;'>⚠️ Evaluation markers will calculate results in microseconds upon execution submission.</span>
                    </div>
                """, unsafe_allow_html=True)

                official_topics = NCDC_CURRICULUM_MAP.get(selected_subject, ["General Concepts"])
                selected_topic_target = st.selectbox("🎯 Target Challenge Topic Filter:", ["All Topics"] + official_topics)
                
                sheet_data = read_public_sheet(selected_subject)
                active_exam_list = []
                
                if sheet_data is not None and not sheet_data.empty:
                    try:
                        for idx, row in sheet_data.iterrows():
                            q_text = str(row.iloc[0]).strip()
                            raw_meta = str(row.iloc[1]).strip()
                            
                            parts = raw_meta.split("||")
                            if len(parts) >= 5:
                                meta_subject = parts[0].strip()
                                meta_topic = parts[1].strip()
                                meta_solution = parts[2].strip()
                                meta_numerical = parts[3].strip()
                                meta_keywords = parts[4].strip()
                                
                                if meta_subject == selected_subject:
                                    if selected_topic_target == "All Topics" or meta_topic == selected_topic_target:
                                        active_exam_list.append({
                                            "question": q_text, "solution": meta_solution, 
                                            "numerical": meta_numerical, "keywords": meta_keywords, "topic": meta_topic
                                        })
                    except Exception: pass

                if not active_exam_list:
                    active_exam_list = [{
                        "question": f"Calculate the systemic variation patterns for advanced NCDC {selected_subject} criteria.",
                        "solution": "Establish uniform coordinate tracks, configure vector parameters, and compute numerical limits.",
                        "numerical": "1497.6", "keywords": "mass, velocity, pressure, calculate, vector", "topic": "General Concepts"
                    }]

                st.markdown("### ✍️ Active Test Assignment")
                for index, item in enumerate(active_exam_list, 1):
                    st.markdown(f"<div style='background-color:#1e1e1e; padding:15px; border-radius:6px; margin-top:10px; border-left:4px solid #ff3333;'><strong>Question {index}:</strong> {item['question']}</div>", unsafe_allow_html=True)
                
                typed_work = st.text_area("Type your step-by-step structural analytical solution here:")
                uploaded_photo = st.file_uploader("📸 Upload Handwritten Script Photo:", type=["jpg", "jpeg", "png"])

                if st.button("🚀 Transmit Answers Script"):
                    if typed_work.strip() or uploaded_photo is not None:
                        # --- STRICT MICROSECOND GRADING ALGORITHM ---
                        start_eval_time = time.time()
                        
                        keywords_list = [k.strip().lower() for k in active_exam_list[0]['keywords'].split(",") if k.strip()]
                        matched_keys = [k for k in keywords_list if k in typed_work.lower()]
                        
                        # High standards length validation (halfway answers penalty check)
                        expected_min_length = max(60, len(active_exam_list[0]['solution']) // 2)
                        actual_length = len(typed_work.strip())
                        
                        keyword_ratio = len(matched_keys) / len(keywords_list) if keywords_list else 1.0
                        length_ratio = min(1.0, actual_length / expected_min_length) if expected_min_length > 0 else 1.0
                        
                        # Combined strict score evaluation
                        calculated_score = int((keyword_ratio * 60) + (length_ratio * 40))
                        if calculated_score > 100: calculated_score = 100
                        
                        # Exact requested grading scale loops
                        if calculated_score >= 80:
                            grade = "A (Distinction)"
                        elif calculated_score >= 60:
                            grade = "B (Credit)"
                        elif calculated_score >= 50:
                            grade = "C (Pass)"
                        else:
                            grade = "E (Failure)"
                        
                        eval_duration = (time.time() - start_eval_time) * 1000 # Microseconds/milliseconds translation
                        
                        full_structured_sol = f"**[NCDC Solution Blueprint]** Target Numerical: {active_exam_list[0]['numerical']} / Guidelines: {active_exam_list[0]['solution']}"
                        
                        # Commit automatically to Done Exam Vault
                        if session_uid not in st.session_state["exam_vault"]:
                            st.session_state["exam_vault"][session_uid] = []
                            
                        exam_record = {
                            "Subject": selected_subject,
                            "Topic": active_exam_list[0]['topic'],
                            "Date": str(datetime.date.today()),
                            "Questions": active_exam_list[0]['question'],
                            "Your_Work": typed_work,
                            "Grade": grade,
                            "Status": f"Scored: {calculated_score}%",
                            "Feedback_Solution": full_structured_sol
                        }
                        st.session_state["exam_vault"][session_uid].append(exam_record)
                        save_cache_to_disk("db_exams.json", st.session_state["exam_vault"])
                        
                        # --- AUTOMATIC FAILURE PARTNER FORWARDING ENGINE ---
                        if calculated_score < 50:
                            st.error(f"⚠️ Score dropped below 50% ({calculated_score}%). Forwarding exam payload to partner channels.")
                            if session_partner:
                                st.session_state["private_chats"].append({
                                    "sender": "SYSTEM_SHIELD_BOT",
                                    "to": session_partner,
                                    "text": f"🚨 EMERGENCY ACADEMIC ALERT: Your partner '{session_user}' failed a test in {selected_subject} ({active_exam_list[0]['topic']}) with a score of {calculated_score}% (Grade E). Here is their work for immediate peer review revision: '{typed_work}'",
                                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                                save_cache_to_disk("db_p2pchat.json", st.session_state["private_chats"])
                        
                        st.success(f"✔ Transmitted! Evaluated in {eval_duration:.2f} ms. Result: {grade} ({calculated_score}%)")
                        
                        # Instant solution reveal if not perfect 100% score
                        if calculated_score < 100:
                            st.markdown("### 💡 Corrections & Blueprint Feedback")
                            st.markdown(f"<div style='background-color:#112211; padding:15px; border-radius:6px; border:1px solid #22aa22;'>{full_structured_sol}</div>", unsafe_allow_html=True)
                        
                        st.session_state[f"exam_active_{session_uid}"] = False

        # --- PROGRESS TRACKER ---
        elif client_tab_choice == "📊 Progress Tracker Logs":
            st.title("📊 Personal Performance Progress Chart")
            user_history = st.session_state["exam_vault"].get(session_uid, [])
            if not user_history:
                st.info("No records completed to build performance tracking logs yet.")
            else:
                df_logs = pd.DataFrame(user_history)
                st.dataframe(df_logs[["Subject", "Topic", "Date", "Grade", "Status"]])
                try:
                    scores_list = [int(s.split(":")[1].replace("%","").strip()) for s in df_logs["Status"] if "Scored" in s]
                    if scores_list:
                        st.markdown("### 📈 Trend Track Graph Analysis")
                        st.line_chart(scores_list)
                except Exception: pass

        # --- DONE EXAM VAULT WITH EXPORT DOWNLOAD HOOKS ---
        elif client_tab_choice == "📁 Finished Exam Vault":
            st.title("📁 Historic Done Exam Script Vault")
            user_history = st.session_state["exam_vault"].get(session_uid, [])
            if not user_history:
                st.info("Your historical exam script archive is currently empty.")
            else:
                for idx, entry in enumerate(user_history):
                    st.markdown(f"""
                    <div style='background-color:#1e1e1e; padding:16px; border-radius:8px; border:1px solid #333; margin-bottom:12px;'>
                        <h4 style='color:#ff3333; margin:0;'>📝 {entry['Subject']} — {entry['Topic']}</h4>
                        <p style='color:#888; font-size:12px;'>Attempted on: {entry['Date']} | Status: <strong>{entry['Grade']} ({entry.get('Status','')})</strong></p>
                        <hr style='border-color:#333; margin:8px 0;'>
                        <p><strong>Question Paper Profile:</strong><br><code style='color:#ff9999;'>{entry.get('Questions','')}</code></p>
                        <p><strong>Your Submitted Script:</strong><br><i style='color:#aaa;'>"{entry.get('Your_Work','')}"</i></p>
                        <div style='background-color:#112211; padding:12px; border-radius:4px; margin-top:8px;'>
                            <span style='color:#25D366; font-weight:bold;'>💡 Automated Correction Brain Solution:</span><br>
                            <span style='font-size:13px;'>{entry.get('Feedback_Solution','')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    report_string = f"ACADEMIC SHIELD PRO REPORT\nDate: {entry['Date']}\nSubject: {entry['Subject']}\nTopic: {entry['Topic']}\nQuestions: {entry.get('Questions','')}\nScore Rank: {entry['Grade']} ({entry.get('Status','')})\nSolution Blueprint: {entry.get('Feedback_Solution','')}"
                    
                    st.download_button(
                        label="📥 Download Script Data",
                        data=report_string,
                        file_name=f"Exam_Script_{entry['Subject']}_{idx}.txt",
                        mime="text/plain",
                        key=f"dl_{idx}"
                    )

        # --- CHAT & ACCOUNT SETTINGS CHANNELS ---
        elif client_tab_choice.startswith("🌐 General Lounge Chat"):
            st.title("🌐 General Lounge Chat Channel")
            st.session_state["last_read_tracker"][session_user] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
            
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state["general_chat"]:
                align_cls = "chat-right" if msg["sender"] == session_user else "chat-left"
                st.markdown(f"<div class='chat-bubble {align_cls}'><strong>{msg['sender']}</strong>:<br>{msg['text']}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
                
            in_gen_msg = st.text_input("Type general chat string message:", key="in_gen_chat_box")
            if st.button("Send to Lounge Channel"):
                if in_gen_msg.strip():
                    st.session_state["general_chat"].append({"sender": session_user, "text": in_gen_msg.strip(), "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    save_cache_to_disk("db_genchat.json", st.session_state["general_chat"])
                    st.rerun()

        elif client_tab_choice.startswith("🔒 Private Peer Chatroom"):
            st.title("🔒 Isolated Private Chat Room Matrix")
            st.session_state["last_read_tracker"][session_user] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
            
            all_usernames = [u["username"] for k, u in st.session_state["users_registry"].items() if u["username"] != session_user]
            target_p = st.selectbox("Select Target Recipient Buddy to Message:", all_usernames)
            
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            isolated_thread = [m for m in st.session_state["private_chats"] if (m["sender"] == session_user and m["to"] == target_p) or (m["sender"] == target_p and m["to"] == session_user)]
            for msg in isolated_thread:
                align_cls = "chat-right" if msg["sender"] == session_user else "chat-left"
                st.markdown(f"<div class='chat-bubble {align_cls}'><strong>{msg['sender']}</strong>:<br>{msg['text']}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
                
            in_priv_msg = st.text_input("Type secure message string:", key="in_p2p_box")
            if st.button("Send Secure Private Message"):
                if in_priv_msg.strip() and target_p:
                    st.session_state["private_chats"].append({"sender": session_user, "to": target_p, "text": in_priv_msg.strip(), "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    save_cache_to_disk("db_p2pchat.json", st.session_state["private_chats"])
                    st.rerun()

        elif client_tab_choice == "🤝 Partner Connection Hub":
            st.title("🤝 Academic Partners Registry")
            st.markdown(f"Linked Partner Profile Name: **{session_partner if session_partner else 'None Linked'}**")
            new_p_assign = st.text_input("Enter target student username link:")
            if st.button("Bind Accountability Matrix"):
                if new_p_assign.strip():
                    st.session_state["users_registry"][session_uid]["partner"] = new_p_assign.strip()
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success("Sync complete!")
                    st.rerun()

        elif client_tab_choice == "🔑 Change Account Password":
            st.title("🔑 Change Password")
            p_old = st.text_input("Enter Current Password:", type="password")
            p_new = st.text_input("Enter New Password:", type="password")
            if st.button("Commit Password Sync"):
                if p_old == st.session_state["users_registry"][session_uid]["pwd"]:
                    st.session_state["users_registry"][session_uid]["pwd"] = p_new.strip()
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success("Password Updated!")

        elif client_tab_choice == "📩 Submit App Suggestions":
            st.title("📩 Public Feedback Portal")
            in_sug_text = st.text_area("Propose adjustments:")
            if st.button("Submit Suggestion"):
                if in_sug_text.strip():
                    st.session_state["suggestions"].append({"user": session_user, "text": in_sug_text.strip(), "time": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")})
                    save_cache_to_disk("db_suggestions.json", st.session_state["suggestions"])
                    st.success("Logged successfully!")

# =========================================================================
# MODULE C: CENTRAL SYSTEM ADMINISTRATIVE DASHBOARD (ROOT PANEL)
# =========================================================================
elif app_mode == "System Administrator Hub":
    st.subheader("🛡️ Administrative Dashboard Terminal")
    admin_token = st.text_input("Enter Admin Verification Password:", type="password")
    
    if admin_token == "SudaisiAdmin2026":
        st.success("✔ Root Privileges Fully Activated.")
        
        adm_t0, adm_t1, adm_t2, adm_t3 = st.tabs([
            "🛑 Account Flags Control", 
            "📋 Registrations Queue", 
            "🔑 Registration Code Generator", 
            "📢 Global Announcements"
        ])
        
        with adm_t0:
            st.subheader("🛑 Master User Warning Flag Management Engine")
            for uid_key, user_node in list(st.session_state["users_registry"].items()):
                if uid_key == "0000": continue 
                
                col_u1, col_u2, col_u3 = st.columns([4, 4, 4])
                with col_u1:
                    st.markdown(f"👤 **{user_node['username']}** (`ID: {uid_key}`)<br>Active Status Tag: <code style='color:#ff9999;'>{user_node.get('warning_msg','None Active')}</code>", unsafe_allow_html=True)
                with col_u2:
                    warn_input = st.text_input("Set Flag text string:", key=f"w_in_{uid_key}")
                    if st.button("⚠️ Inject/Update Warning", key=f"w_btn_{uid_key}"):
                        st.session_state["users_registry"][uid_key]["warning_msg"] = warn_input
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.rerun()
                with col_u3:
                    if st.button("✅ Drop Warning & Tags Completely", key=f"clr_btn_{uid_key}"):
                        st.session_state["users_registry"][uid_key]["warning_msg"] = ""
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.success("Warning tags completely dropped and synchronized.")
                        st.rerun()
                st.markdown("---")

        with adm_t1:
            st.subheader(f"🔔 Verification Queue Counter: {len(st.session_state['pending_registrations'])}")
            for index, item_node in enumerate(st.session_state["pending_registrations"]):
                st.markdown(f"📌 **Request Profile {index+1}:** User: `{item_node['username']}` | Combo: {item_node['subjects']}")
                if st.button(f"🟢 Approve and Grant Entry ID to {item_node['username']}", key=f"p_app_{index}"):
                    allocated_uid_id = str(6601 + len(st.session_state["users_registry"]))
                    st.session_state["users_registry"][allocated_uid_id] = {
                        "username": item_node["username"], "pwd": item_node["pwd"], "name": item_node["name"],
                        "class": item_node["class"], "school": item_node["school"], "phone": item_node["phone"],
                        "email": item_node["email"], "gender": item_node["gender"], "location": item_node["location"],
                        "subjects": item_node["subjects"], "status": "Approved", "warning_msg": "", "avatar": AVATAR_OPTIONS[0],
                        "partner": ""
                    }
                    st.session_state["pending_registrations"].pop(index)
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    save_cache_to_disk("db_pending.json", st.session_state["pending_registrations"])
                    st.success(f"Activated ID Token: `{allocated_uid_id}`")
                    st.rerun()

        with adm_t2:
            st.subheader("🔑 Access Token Generator")
            st.write("Active Verification Tokens:", st.session_state["generated_registration_codes"])
            
            new_code_token = st.text_input("Create Secret Registration Token String (e.g. SHIELD2026):")
            if st.button("💾 Append Token to System Memory"):
                if new_code_token.strip() and new_code_token.strip() not in st.session_state["generated_registration_codes"]:
                    st.session_state["generated_registration_codes"].append(new_code_token.strip())
                    save_cache_to_disk("db_regcodes.json", st.session_state["generated_registration_codes"])
                    st.success(f"✔ Token '{new_code_token.strip()}' is now active and ready for student registrations!")
                    st.rerun()

        with adm_t3:
            st.subheader("📢 Broadcast Announcements Engine")
            alert_msg = st.text_input("Type critical system update alert:")
            if st.button("Broadcast System Update Everywhere"):
                if alert_msg.strip():
                    st.session_state["global_alerts"].append(alert_msg.strip())
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.success("✔ Notification broadcast injected successfully.")
