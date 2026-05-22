import streamlit as st
import pandas as pd
import datetime
import random
import os
import json
import time

# =========================================================================
# 1. PLATFORM CONFIGURATIONS, SECURITY HEADERS & WHATSAPP VISUAL STYLING
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
    
    /* --- WhatsApp Realistic Layout CSS --- */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 15px;
        background-color: #0b141a; 
        background-image: url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png');
        background-repeat: repeat;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #222;
    }
    .chat-bubble {
        padding: 8px 12px;
        border-radius: 7px;
        margin-bottom: 10px;
        max-width: 65%;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 14.5px;
        line-height: 1.4;
        position: relative;
        box-shadow: 0 1px 0.5px rgba(0,0,0,0.13);
    }
    .chat-left { 
        background-color: #202c33; 
        color: #e9edef; 
        margin-right: auto; 
        text-align: left; 
        border-top-left-radius: 0px;
    }
    .chat-right { 
        background-color: #005c4b; 
        color: #e9edef; 
        margin-left: auto; 
        text-align: left; 
        border-top-right-radius: 0px;
    }
    .chat-timestamp {
        font-size: 10px;
        color: rgba(233, 237, 239, 0.6);
        text-align: right;
        margin-top: 4px;
        display: block;
    }
    .chat-media-box {
        margin-top: 6px;
        padding: 4px;
        background-color: rgba(0,0,0,0.15);
        border-radius: 4px;
        font-size: 12px;
    }
    
    .system-warn-box { background-color: #3b1111; border: 2px solid #ff3333; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #ff9999; font-weight: bold;}
    .top-profile-pic { border-radius: 50%; border: 2px solid #ff3333; object-fit: cover; width: 55px; height: 55px; }
    .admin-broadcast-banner { background-color: #ff3333; color: white; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    
    div.stButton > button { width: 100% !important; font-weight: bold !important; background-color: #1e1e1e !important; color: #ffffff !important; border: 1px solid #444444 !important; border-radius: 4px !important; }
    div.stButton > button:hover { background-color: #ff3333 !important; color: white !important; border-color: #ff3333 !important; }
    
    .metric-card { background-color: #1a1a1a; padding: 15px; border-radius: 6px; border-left: 4px solid #ff3333; margin-bottom: 10px; }
    .notes-box { background-color: #111111; padding: 20px; border: 1px dashed #444; border-radius: 8px; margin-bottom: 15px; }
    .suggestion-card { background-color: #151515; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #005c4b; }
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

DEFAULT_SUDAISI_IMAGE = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=200"
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
        "6601": {"username": "Setra stones", "pwd": "Amazima2026", "name": "Setra Stones", "class": "Senior Five", "school": "St Marys", "phone": "0752047103", "email": "setra@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry"], "status": "Approved", "warning_msg": "", "avatar": AVATAR_OPTIONS[0], "partner": ""}
    })

if "pending_registrations" not in st.session_state: st.session_state["pending_registrations"] = load_cache_from_disk("db_pending.json", [])
if "general_chat" not in st.session_state: st.session_state["general_chat"] = load_cache_from_disk("db_genchat.json", [])
if "private_chats" not in st.session_state: st.session_state["private_chats"] = load_cache_from_disk("db_p2pchat.json", [])
if "suggestions" not in st.session_state: st.session_state["suggestions"] = load_cache_from_disk("db_suggestions.json", [])
if "global_alerts" not in st.session_state: st.session_state["global_alerts"] = load_cache_from_disk("db_alerts.json", ["🚀 Platform Online. Secure Mirror Systems Functional."])
if "exam_vault" not in st.session_state: st.session_state["exam_vault"] = load_cache_from_disk("db_exams.json", {})
if "last_read_tracker" not in st.session_state: st.session_state["last_read_tracker"] = load_cache_from_disk("db_readtrack.json", {})
if "generated_registration_codes" not in st.session_state: st.session_state["generated_registration_codes"] = load_cache_from_disk("db_regcodes.json", ["SHIELD2026", "ASP2026"])
if "custom_admin_photo" not in st.session_state: st.session_state["custom_admin_photo"] = load_cache_from_disk("db_admin_photo.json", DEFAULT_SUDAISI_IMAGE)

if "revision_notes_db" not in st.session_state:
    st.session_state["revision_notes_db"] = [
        {"Title": "Pure Mathematics Vectors Blueprint", "Subject": "Mathematics", "Content": "Vectors core revision summary notes: Unit tracks, relative parameters, and Cartesian projections for P425/1 standards."}
    ]

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
                st.sidebar.error(f"❌ Access Terminated! Status: {user_account_status}. Contact administration.")
            else:
                is_authenticated = True
                session_user = login_user
                session_uid = login_uid
                session_class = node.get("class", "Senior Five")
                session_partner = node.get("partner", "")
                allowed_subjects = node["subjects"]
                current_avatar_url = node.get("avatar", AVATAR_OPTIONS[0])

# --- UNIFIED PERMANENT TOP PICTURE SYNC FRAME ---
col_head_title, col_head_pic = st.columns([11, 1])
with col_head_title:
    st.markdown("<h2 style='color:#ff3333; margin:0;'>🛡️ Academic Shield Pro</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#aaaaaa; font-style:italic; margin:0;'>“Conceptual Mastery Terminal Engine”</h5>", unsafe_allow_html=True)

with col_head_pic:
    admin_img = st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE)
    if not admin_img.strip():
        admin_img = DEFAULT_SUDAISI_IMAGE
    if session_user == "Admin" or current_avatar_url == "SUDAISI_BAKED":
        st.image(admin_img, width=55)
    else:
        st.image(current_avatar_url if current_avatar_url else AVATAR_OPTIONS[0], width=55)

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
            "📚 Read Revision Notes",
            "🤝 Partner Connection Hub", 
            f"🌐 General Lounge Chat {gen_badge}", 
            f"🔒 Private Peer Chatroom {p2p_badge}", 
            "📊 Progress Tracker Logs", 
            "📁 Finished Exam Vault", 
            "🔑 Change Account Password", 
            "📩 Submit App Suggestions"
        ])

        # --- EXAM CENTER WITH INSTATED EVALUATION LOGIC & 2-QUESTION BATCHING ---
        if client_tab_choice == "📝 Access Exam Center":
            st.title("📝 Precision Topic Exam Center")
            
            if f"exam_active_{session_uid}" not in st.session_state:
                st.session_state[f"exam_active_{session_uid}"] = False
            if f"exam_submitted_{session_uid}" not in st.session_state:
                st.session_state[f"exam_submitted_{session_uid}"] = False
            if f"current_exam_batch_{session_uid}" not in st.session_state:
                st.session_state[f"current_exam_batch_{session_uid}"] = 0
            if f"last_instant_feedback_{session_uid}" not in st.session_state:
                st.session_state[f"last_instant_feedback_{session_uid}"] = ""

            if not st.session_state[f"exam_active_{session_uid}"]:
                st.markdown("### 🛑 Security Access Gateway Check")
                st.info("Exam questions are safely concealed. Confirm authorization parameters below to display items.")
                if st.button("👉 YES, I am here to take a test!"):
                    st.session_state[f"exam_active_{session_uid}"] = True
                    st.session_state[f"exam_submitted_{session_uid}"] = False
                    st.session_state[f"current_exam_batch_{session_uid}"] = 0
                    st.session_state[f"last_instant_feedback_{session_uid}"] = ""
                    st.session_state[f"exam_start_{session_uid}"] = datetime.datetime.now().strftime("%I:%M:%S %p")
                    st.rerun()
            else:
                st.markdown(f"""
                    <div class='timer-container'>
                        <span style='color:#ff3333; font-size:18px; font-weight:bold;'>Started at: {st.session_state[f'exam_start_{session_uid}']}</span><br>
                        <span style='color:#ffffff; font-size:13px;'>⚠️ Evaluation markers calculate results in microseconds. Displaying 2 items per batch.</span>
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
                    active_exam_list = [
                        {"question": "Calculate fluid velocity mechanics variation patterns instance Alpha.", "solution": "Establish uniform coordinate tracks, configure vector parameters.", "numerical": "1497.6", "keywords": "velocity, parameters", "topic": "General Concepts"},
                        {"question": "Calculate fluid velocity mechanics variation patterns instance Beta.", "solution": "Configure vector parameters, and compute numerical limits.", "numerical": "1177.2", "keywords": "vector, limits", "topic": "General Concepts"}
                    ]

                # --- 2-QUESTION BATCH SLICING ---
                batch_start = st.session_state[f"current_exam_batch_{session_uid}"] * 2
                if batch_start >= len(active_exam_list):
                    batch_start = 0
                    st.session_state[f"current_exam_batch_{session_uid}"] = 0
                    
                current_two_items = active_exam_list[batch_start:batch_start + 2]

                st.markdown("### ✍️ Active Test Assignment (2 Questions Active)")
                for index, item in enumerate(current_two_items, 1):
                    st.markdown(f"<div style='background-color:#1e1e1e; padding:15px; border-radius:6px; margin-top:10px; border-left:4px solid #ff3333;'><strong>Question {index}:</strong> {item['question']}</div>", unsafe_allow_html=True)
                
                typed_work = st.text_area("Type your step-by-step structural analytical solutions for both items here:", key=f"exam_text_{batch_start}")
                uploaded_photo = st.file_uploader("📸 Upload Handwritten Script Photo:", type=["jpg", "jpeg", "png"], key=f"exam_img_{batch_start}")

                # --- INSTANT ERROR CHECK & IMMEDIATE CORRECTION ENGINE ---
                if not st.session_state[f"exam_submitted_{session_uid}"]:
                    if st.button("🚀 Transmit Answers Script"):
                        if typed_work.strip() or uploaded_photo is not None:
                            start_eval_time = time.time()
                            
                            all_keywords = ",".join([item['keywords'] for item in current_two_items])
                            keywords_list = [k.strip().lower() for k in all_keywords.split(",") if k.strip()]
                            matched_keys = [k for k in keywords_list if k in typed_work.lower()]
                            
                            combined_solution_len = sum([len(item['solution']) for item in current_two_items])
                            expected_min_length = max(60, combined_solution_len // 2)
                            actual_length = len(typed_work.strip())
                            
                            keyword_ratio = len(matched_keys) / len(keywords_list) if keywords_list else 1.0
                            length_ratio = min(1.0, actual_length / expected_min_length) if expected_min_length > 0 else 1.0
                            
                            calculated_score = int((keyword_ratio * 60) + (length_ratio * 40))
                            if calculated_score > 100: calculated_score = 100
                            
                            if calculated_score >= 80: grade = "A (Distinction)"
                            elif calculated_score >= 60: grade = "B (Credit)"
                            elif calculated_score >= 50: grade = "C (Pass)"
                            else: grade = "E (Failure)"
                            
                            eval_duration = (time.time() - start_eval_time) * 1000
                            
                            blueprints = " | ".join([f"[Q{i+1} Numerical Answer: {item['numerical']} -> Marking Guide Checklist: {item['solution']}]" for i, item in enumerate(current_two_items)])
                            full_structured_sol = f"**[OFFICIAL NCDC SOLUTION BLUEPRINT]** {blueprints}"
                            
                            if session_uid not in st.session_state["exam_vault"]:
                                st.session_state["exam_vault"][session_uid] = []
                                
                            exam_record = {
                                "Subject": selected_subject, 
                                "Topic": current_two_items[0]['topic'], 
                                "Date": str(datetime.date.today()),
                                "Questions": " & ".join([item['question'] for item in current_two_items]), 
                                "Your_Work": typed_work, 
                                "Grade": grade,
                                "Status": f"Scored: {calculated_score}%", 
                                "Score_Raw": calculated_score, 
                                "Feedback_Solution": full_structured_sol
                            }
                            st.session_state["exam_vault"][session_uid].append(exam_record)
                            save_cache_to_disk("db_exams.json", st.session_state["exam_vault"])
                            
                            if calculated_score < 50:
                                if session_partner:
                                    st.session_state["private_chats"].append({
                                        "sender": "SYSTEM_SHIELD_BOT", "to": session_partner,
                                        "text": f"🚨 EMERGENCY ACADEMIC ALERT: Your partner '{session_user}' failed a test batch in {selected_subject} ({current_two_items[0]['topic']}) with a score of {calculated_score}% (Grade E).",
                                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "media": None
                                    })
                                    save_cache_to_disk("db_p2pchat.json", st.session_state["private_chats"])
                            
                            st.session_state[f"last_instant_feedback_{session_uid}"] = full_structured_sol
                            st.session_state[f"exam_submitted_{session_uid}"] = True
                            st.rerun()
                else:
                    st.markdown(f"### 📊 Initial Evaluation Breakdown Result")
                    latest_rec = st.session_state["exam_vault"][session_uid][-1]
                    st.info(f"**Grade:** {latest_rec['Grade']} | **Status:** {latest_rec['Status']}")
                    
                    # Force render instant solutions immediately below sub status layout
                    st.markdown("### 💡 INSTANT NCDC STANDARD CORRECTIVE SOLUTIONS")
                    feedback_to_show = st.session_state[f"last_instant_feedback_{session_uid}"] if st.session_state[f"last_instant_feedback_{session_uid}"] else latest_rec['Feedback_Solution']
                    st.markdown(f"""
                        <div style='background-color:#112211; padding:18px; border-radius:6px; border:2px solid #22aa22; color:#ddffdd;'>
                            <strong>Marking Keys & Detailed Blueprint Explanations:</strong><br><br>
                            {feedback_to_show}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    if st.button("🔄 Load Next 2 Random Questions"):
                        st.session_state[f"current_exam_batch_{session_uid}"] += 1
                        st.session_state[f"exam_submitted_{session_uid}"] = False
                        st.session_state[f"last_instant_feedback_{session_uid}"] = ""
                        st.rerun()

        # --- REVISION NOTES HUB (CATCH TYPEERROR) ---
        elif client_tab_choice == "📚 Read Revision Notes":
            st.title("📚 Academic Revision Notes Hub")
            
            try:
                notes_filtered = [n for n in st.session_state.get("revision_notes_db", []) if isinstance(n, dict) and n.get("Subject") == selected_subject]
            except Exception:
                notes_filtered = []
            
            if not notes_filtered:
                st.info(f"No active summary study materials filed for {selected_subject} yet.")
            else:
                for idx, note in enumerate(notes_filtered):
                    st.markdown(f"""
                    <div class="notes-box">
                        <h4 style="color:#ff3333; margin:0;">📄 {note.get('Title','Untitled Note')}</h4>
                        <p style="color:#888; font-size:12px;">Subject Category: {note.get('Subject','')}</p>
                        <p style="color:#ddd; font-size:14px; line-height:1.5;">{note.get('Content','')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    note_payload = f"ACADEMIC SHIELD PRO STUDY GUIDE\nTitle: {note.get('Title')}\nSubject: {note.get('Subject')}\nContent:\n{note.get('Content')}"
                    st.download_button(
                        label="📥 Download This Study Note (One-Tap)",
                        data=note_payload,
                        file_name=f"Revision_Note_{str(note.get('Title')).replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"dl_note_{idx}"
                    )

        # --- PROGRESS TRACKER LOGS (CATCH INDEXERROR & PARSE SAFE) ---
        elif client_tab_choice == "📊 Progress Tracker Logs":
            st.title("📊 Crystal-Clear Performance Analytics")
            user_history = st.session_state["exam_vault"].get(session_uid, [])
            
            if not user_history:
                st.info("No records completed to build analytics tracks yet.")
            else:
                col_m1, col_m2, col_m3 = st.columns(3)
                scores_list = []
                
                for entry in user_history:
                    if "Score_Raw" in entry:
                        scores_list.append(int(entry["Score_Raw"]))
                    elif "Status" in entry and ":" in str(entry["Status"]):
                        try:
                            raw_val = str(entry["Status"]).split(":")[1].replace("%","").strip()
                            scores_list.append(int(raw_val))
                        except Exception:
                            scores_list.append(0)
                    else:
                        scores_list.append(0)
                
                with col_m1:
                    st.markdown(f'<div class="metric-card"><h5>📝 Total Exams Attempted</h5><h2>{len(user_history)} Items</h2></div>', unsafe_allow_html=True)
                with col_m2:
                    avg_score = sum(scores_list)/len(scores_list) if scores_list else 0
                    st.markdown(f'<div class="metric-card"><h5>📈 Mean Mastery Percentage</h5><h2>{avg_score:.1f}%</h2></div>', unsafe_allow_html=True)
                with col_m3:
                    highest = max(scores_list) if scores_list else 0
                    st.markdown(f'<div class="metric-card"><h5>🏆 Peak Evaluation Score</h5><h2>{highest}% Target</h2></div>', unsafe_allow_html=True)
                
                if scores_list:
                    st.markdown("### 📈 Sequential Score Growth Trend Chart")
                    chart_df = pd.DataFrame({"Your Score (%)": scores_list})
                    chart_df.index = [f"Exam #{i+1}" for i in range(len(scores_list))]
                    st.line_chart(chart_df, y="Your Score (%)")
                
                st.markdown("### 📋 Historic Registry Log Columns")
                df_logs = pd.DataFrame(user_history)
                display_cols = [c for c in ["Subject", "Topic", "Date", "Grade", "Status"] if c in df_logs.columns]
                st.dataframe(df_logs[display_cols], use_container_width=True)

        # --- FINISHED EXAM INTERACTIVE VAULT PORTAL ---
        elif client_tab_choice == "📁 Finished Exam Vault":
            st.title("📁 Historic Interactive Done Exam Script Vault")
            user_history = st.session_state["exam_vault"].get(session_uid, [])
            
            if not user_history:
                st.info("Your historical completed script archive is currently empty.")
            else:
                st.markdown("##### 🎯 Choose a completed exam script instance to review configurations:")
                exam_options = [f"[{entry.get('Date','')} ] {entry.get('Subject','')} — {entry.get('Topic','')} ({entry.get('Grade','')})" for entry in user_history]
                selected_exam_index = st.selectbox("Select Done Exam Assignment:", range(len(exam_options)), format_func=lambda x: exam_options[x])
                
                target_entry = user_history[selected_exam_index]
                st.markdown("---")
                
                v_tab1, v_tab2, v_tab3 = st.tabs(["📊 Attained Scores & Script", "💡 NCDC Solution Brain", "📥 Download Package File"])
                
                with v_tab1:
                    st.markdown(f"#### 📝 Evaluation Performance Metrics")
                    st.markdown(f"- **Subject Profile:** {target_entry.get('Subject','')}\n- **Topic Focus Layer:** {target_entry.get('Topic','')}\n- **Execution Status Score:** `{target_entry.get('Status','')}`\n- **Assigned Grade Rank:** `{target_entry.get('Grade','')}`")
                    st.markdown("##### 👤 Your Submitted Answers Draft:")
                    st.info(target_entry.get('Your_Work',''))
                    
                with v_tab2:
                    st.markdown("#### 💡 Corrective Action Model Blueprint")
                    st.markdown(f"<div style='background-color:#112211; padding:15px; border-radius:6px; border:1px solid #22aa22;'>{target_entry.get('Feedback_Solution','No custom feedback filed.')}</div>", unsafe_allow_html=True)
                    
                with v_tab3:
                    st.markdown("#### 📥 Instant Structural Script Exporter")
                    st.write("Generate a local text copy of this complete evaluation model record safely.")
                    report_string = f"ACADEMIC SHIELD PRO REPORT\nDate: {target_entry.get('Date','')}\nSubject: {target_entry.get('Subject','')}\nTopic: {target_entry.get('Topic','')}\nQuestions: {target_entry.get('Questions','')}\nScore Rank: {target_entry.get('Grade','')} ({target_entry.get('Status','')})\nSolution Blueprint: {target_entry.get('Feedback_Solution','')}"
                    
                    st.download_button(
                        label="📥 Click to Download Complete Script Log",
                        data=report_string,
                        file_name=f"ASP_Script_{target_entry.get('Subject','')}_{str(target_entry.get('Topic','')).replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"vault_dl_{selected_exam_index}"
                    )

        # --- WHATSAPP DESIGN INTERACTIVE GENERAL LOUNGE CHAT ---
        elif client_tab_choice.startswith("🌐 General Lounge Chat"):
            st.title("🌐 General Lounge Chat Channel")
            st.session_state["last_read_tracker"][session_user] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
            
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state["general_chat"]:
                align_cls = "chat-right" if msg["sender"] == session_user else "chat-left"
                media_html = f"<div class='chat-media-box'>📎 Attached File Component: {msg['media']}</div>" if msg.get("media") else ""
                st.markdown(f"""
                <div class='chat-bubble {align_cls}'>
                    <strong>{msg['sender']}</strong><br>
                    {msg['text']}
                    {media_html}
                    <span class='chat-timestamp'>{msg.get('timestamp','')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
                
            col_in_txt, col_in_media = st.columns([3, 1])
            with col_in_txt:
                in_gen_msg = st.text_input("Type general chat string message:", key="in_gen_chat_box")
            with col_in_media:
                gen_media_file = st.file_uploader("📎 Upload Media", type=["jpg","png","pdf","txt","zip"], key="gen_media_upload")
                
            if st.button("Send to Lounge Channel"):
                if in_gen_msg.strip() or gen_media_file is not None:
                    m_name = gen_media_file.name if gen_media_file else None
                    st.session_state["general_chat"].append({
                        "sender": session_user, "text": in_gen_msg.strip(), 
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p"), "media": m_name
                    })
                    save_cache_to_disk("db_genchat.json", st.session_state["general_chat"])
                    st.rerun()

        # --- WHATSAPP DESIGN INTERACTIVE PRIVATE PEER CHAT ---
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
                media_html = f"<div class='chat-media-box'>📎 Attached File Component: {msg['media']}</div>" if msg.get("media") else ""
                st.markdown(f"""
                <div class='chat-bubble {align_cls}'>
                    <strong>{msg['sender']}</strong><br>
                    {msg['text']}
                    {media_html}
                    <span class='chat-timestamp'>{msg.get('timestamp','')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
                
            col_priv_txt, col_priv_media = st.columns([3, 1])
            with col_priv_txt:
                in_priv_msg = st.text_input("Type secure message string:", key="in_p2p_box")
            with col_priv_media:
                priv_media_file = st.file_uploader("📎 Upload Media", type=["jpg","png","pdf","txt","zip"], key="priv_media_upload")
                
            if st.button("Send Secure Private Message"):
                if (in_priv_msg.strip() or priv_media_file is not None) and target_p:
                    m_name = priv_media_file.name if priv_media_file else None
                    st.session_state["private_chats"].append({
                        "sender": session_user, "to": target_p, "text": in_priv_msg.strip(), 
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p"), "media": m_name
                    })
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
        
        adm_t0, adm_t1, adm_t2, adm_t3, adm_t4, adm_t5 = st.tabs([
            "🛑 Account Flags Control", 
            "📋 Registrations Queue", 
            "🔑 Registration Code Generator", 
            "📢 Global Announcements",
            "📩 View User Suggestions",
            "📸 Change Master Profile Photo"
        ])
        
        with adm_t0:
            st.subheader("🛑 Master User Account Management Hub")
            for uid_key, user_node in list(st.session_state["users_registry"].items()):
                if uid_key == "0000": continue 
                
                st.markdown(f"👤 **{user_node['username']}** (ID: `{uid_key}`) | Current Status: `{user_node.get('status','Approved')}`")
                
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                with col_btn1:
                    if st.button("🚫 Ban Account", key=f"ban_{uid_key}"):
                        st.session_state["users_registry"][uid_key]["status"] = "Banned"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.warning(f"User {uid_key} has been Banned.")
                        st.rerun()
                with col_btn2:
                    if st.button("🔒 Lock Account", key=f"lock_{uid_key}"):
                        st.session_state["users_registry"][uid_key]["status"] = "Locked"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.warning(f"User {uid_key} has been Locked.")
                        st.rerun()
                with col_btn3:
                    if st.button("❌ Delete User", key=f"del_{uid_key}"):
                        del st.session_state["users_registry"][uid_key]
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.error(f"User {uid_key} removed permanently.")
                        st.rerun()
                with col_btn4:
                    if st.button("✅ Reset Status", key=f"rst_{uid_key}"):
                        st.session_state["users_registry"][uid_key]["status"] = "Approved"
                        st.session_state["users_registry"][uid_key]["warning_msg"] = ""
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.success(f"User {uid_key} reset cleanly.")
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
            
            new_code_token = st.text_input("Create Secret Registration Token String:")
            if st.button("💾 Append Token to System Memory"):
                if new_code_token.strip() and new_code_token.strip() not in st.session_state["generated_registration_codes"]:
                    st.session_state["generated_registration_codes"].append(new_code_token.strip())
                    save_cache_to_disk("db_regcodes.json", st.session_state["generated_registration_codes"])
                    st.success(f"✔ Token active for student registrations!")
                    st.rerun()

        with adm_t3:
            st.subheader("📢 Broadcast Announcements Engine")
            alert_msg = st.text_input("Type critical system update alert:")
            if st.button("Broadcast System Update Everywhere"):
                if alert_msg.strip():
                    st.session_state["global_alerts"].append(alert_msg.strip())
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.success("✔ Notification broadcast injected successfully.")

        with adm_t4:
            st.subheader("📩 Incoming Student Suggestion Logs")
            sug_list = st.session_state.get("suggestions", [])
            if not sug_list:
                st.info("No app feedback has been logged yet.")
            else:
                for item in sug_list:
                    st.markdown(f"""
                    <div class="suggestion-card">
                        <strong>User:</strong> {item.get('user','Anonymous')} | <span style='color:#888;'>{item.get('time','')}</span><br>
                        <p style='margin-top:5px; color:#ddd;'>{item.get('text','')}</p>
                    </div>
                    """, unsafe_allow_html=True)

        with adm_t5:
            st.subheader("📸 Change Master UI Profile Image")
            uploaded_img_url = st.text_input("Profile Picture Image URL:", value=st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE))
            
            if st.button("💾 Apply Image Link Across UI Panels"):
                if uploaded_img_url.strip():
                    st.session_state["custom_admin_photo"] = uploaded_img_url.strip()
                    save_cache_to_disk("db_admin_photo.json", st.session_state["custom_admin_photo"])
                    st.success("✔ Master photo link saved permanently to cache arrays!")
                    time.sleep(0.5)
                    st.rerun()
