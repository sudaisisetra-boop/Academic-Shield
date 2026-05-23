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

# Injected CSS to hide default branding headers/footers and power custom WhatsApp elements
st.markdown("""
    <head>
        <link rel="manifest" href="manifest.json">
        <meta name="theme-color" content="#ff3333">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    </head>
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
    .whatsapp-ticks {
        color: #53bdeb !important;
        margin-left: 3px;
        font-weight: bold;
    }
    .chat-media-box {
        margin-top: 6px;
        padding: 6px;
        background-color: rgba(0,0,0,0.25);
        border-radius: 6px;
        font-size: 13px;
        border-left: 3px solid #ff3333;
    }
    .audio-note-box {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(0,0,0,0.15);
        padding: 8px;
        border-radius: 6px;
        margin-top: 5px;
        border-left: 3px solid #53bdeb;
    }
    
    .system-warn-box { background-color: #3b1111; border: 2px solid #ff3333; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #ff9999; font-weight: bold;}
    .top-profile-pic { border-radius: 50%; border: 2px solid #ff3333; object-fit: cover; width: 55px; height: 55px; }
    .admin-broadcast-banner { background-color: #ff3333; color: white; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    
    div.stButton > button { width: 100% !important; font-weight: bold !important; background-color: #1e1e1e !important; color: #ffffff !important; border: 1px solid #444444 !important; border-radius: 4px !important; }
    div.stButton > button:hover { background-color: #ff3333 !important; color: white !important; border-color: #ff3333 !important; }
    
    .metric-card { background-color: #1a1a1a; padding: 15px; border-radius: 6px; border-left: 4px solid #ff3333; margin-bottom: 10px; }
    .notes-box { background-color: #111111; padding: 20px; border: 1px dashed #444; border-radius: 8px; margin-bottom: 15px; }
    .suggestion-card { background-color: #151515; padding: 15px; border-radius: 6px; margin-bottom: 12px; border-left: 3px solid #005c4b; }
    .suggestion-reply-box { background-color: #1c2826; padding: 10px; border-radius: 4px; margin-top: 8px; border-left: 2px solid #ff3333; font-style: italic; color: #e9edef; }
    .directory-card { background-color: #141414; padding: 18px; border-radius: 8px; border: 1px solid #252525; margin-bottom: 12px; }
    
    .partner-live-badge { background-color: #005c4b; color: #ffffff; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    .partner-vs-box { background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; margin-top: 15px; }
    
    /* Meet Panel Styling */
    .meet-panel-card { background-color: #141a1e; border: 1px solid #ff3333; border-radius: 8px; padding: 15px; margin-bottom: 15px;}
    .hand-raised-badge { background-color: #ffcc00; color: #000000; font-weight: bold; border-radius: 4px; padding: 2px 6px; font-size: 11px; display: inline-block; margin-left: 6px;}

    .sudaisi-branding-footer {
        text-align: center;
        padding: 15px;
        margin-top: 40px;
        border-top: 1px solid #222;
        background-color: #0e0e0e;
        border-radius: 4px;
    }
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
        "0000": {"username": "Admin", "pwd": "SudaisiAdmin2026", "name": "Sudaisi Setra", "class": "Senior Five", "school": "St Marys", "phone": "0752047103", "email": "admin@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry", "Biology"], "status": "Approved", "warning_msg": "", "avatar": "SUDAISI_BAKED", "partner": "", "partner_role": "Standalone", "role": "SUPER_ADMIN"},
        "6601": {"username": "Setra stones", "pwd": "Amazima2026", "name": "Setra Stones", "class": "Senior Five", "school": "St Marys", "phone": "0752047103", "email": "setra@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry"], "status": "Approved", "warning_msg": "", "avatar": AVATAR_OPTIONS[0], "partner": "", "partner_role": "Standalone", "role": "USER"}
    })

if "0000" in st.session_state["users_registry"]:
    st.session_state["users_registry"]["0000"]["role"] = "SUPER_ADMIN"
    st.session_state["users_registry"]["0000"]["status"] = "Approved"

if "pending_registrations" not in st.session_state: st.session_state["pending_registrations"] = load_cache_from_disk("db_pending.json", [])
if "general_chat" not in st.session_state: st.session_state["general_chat"] = load_cache_from_disk("db_genchat.json", [])
if "private_chats" not in st.session_state: st.session_state["private_chats"] = load_cache_from_disk("db_p2pchat.json", [])
if "suggestions" not in st.session_state: st.session_state["suggestions"] = load_cache_from_disk("db_suggestions.json", [])
if "global_alerts" not in st.session_state: st.session_state["global_alerts"] = load_cache_from_disk("db_alerts.json", ["🚀 Platform Online. Secure Mirror Systems Functional."])
if "exam_vault" not in st.session_state: st.session_state["exam_vault"] = load_cache_from_disk("db_exams.json", {})
if "last_read_tracker" not in st.session_state: st.session_state["last_read_tracker"] = load_cache_from_disk("db_readtrack.json", {})
if "generated_registration_codes" not in st.session_state: st.session_state["generated_registration_codes"] = load_cache_from_disk("db_regcodes.json", ["SHIELD2026", "ASP2026"])
if "custom_admin_photo" not in st.session_state: st.session_state["custom_admin_photo"] = load_cache_from_disk("db_admin_photo.json", DEFAULT_SUDAISI_IMAGE)

if "mutual_exam_sessions" not in st.session_state:
    st.session_state["mutual_exam_sessions"] = load_cache_from_disk("db_mutual_exams.json", {})

if "group_discussions" not in st.session_state:
    st.session_state["group_discussions"] = load_cache_from_disk("db_group_discussions.json", {})
if "user_forum_presence" not in st.session_state:
    st.session_state["user_forum_presence"] = {}

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
session_partner_role = "Standalone"
allowed_subjects = ["Mathematics", "Physics", "Chemistry"]
current_avatar_url = AVATAR_OPTIONS[0]
user_account_status = "Approved"
account_warning_text = ""
user_role = "USER"

st.sidebar.title("🔐 ASP Access Interface")
app_mode = st.sidebar.radio("Select Portal Target Module", ["Login Page Panel", "Registration Terminal", "System Administrator Hub"])

if "nav_target_override" in st.session_state:
    client_default_nav = st.session_state.pop("nav_target_override")
else:
    client_default_nav = "📝 Access Exam Center"

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
        session_partner_role = "Standalone"
        allowed_subjects = ["Mathematics", "Physics", "Chemistry", "Biology"]
        current_avatar_url = "SUDAISI_BAKED"
        user_account_status = "Approved"
        user_role = "SUPER_ADMIN"
    elif login_uid in st.session_state["users_registry"]:
        node = st.session_state["users_registry"][login_uid]
        if node["username"] == login_user and node["pwd"] == login_pwd:
            user_account_status = node.get("status", "Approved")
            account_warning_text = node.get("warning_msg", "")
            
            if user_account_status in ["Banned", "Locked"] and node.get("role") != "SUPER_ADMIN":
                st.sidebar.error(f"❌ Access Terminated! Status: {user_account_status}. Contact administration.")
            else:
                is_authenticated = True
                session_user = login_user
                session_uid = login_uid
                session_class = node.get("class", "Senior Five")
                session_partner = node.get("partner", "")
                session_partner_role = node.get("partner_role", "Standalone")
                allowed_subjects = node["subjects"]
                current_avatar_url = node.get("avatar", AVATAR_OPTIONS[0])
                user_role = node.get("role", "USER")

col_head_title, col_head_pic = st.columns([11, 1])
with col_head_title:
    st.markdown("<h2 style='color:#ff3333; margin:0;'>🛡️ Academic Shield Pro</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#aaaaaa; font-style:italic; margin:0;'>“Conceptual Mastery Terminal Engine”</h5>", unsafe_allow_html=True)

with col_head_pic:
    admin_img = st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE)
    if not admin_img.strip():
        admin_img = DEFAULT_SUDAISI_IMAGE
    if session_user == "Admin" or current_avatar_url == "SUDAISI_BAKED" or user_role == "SUPER_ADMIN":
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
                "avatar": AVATAR_OPTIONS[0], "partner": "", "partner_role": "Standalone", "role": "USER", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            }
            st.session_state["pending_registrations"].append(new_request)
            save_cache_to_disk("db_pending.json", st.session_state["pending_registrations"])
            st.success("✔ Payload captured! Awaiting Admin activation check.")

# =========================================================================
# MODULE B: LOGIN PAGE PANEL & CLIENT WORKSPACE
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
        unread_p2p_cnt = sum(1 for m in st.session_state["private_chats"] if isinstance(m, dict) and m.get("to") == session_user and m.get("timestamp", "") > u_last)
        unread_gen_cnt = sum(1 for m in st.session_state["general_chat"] if isinstance(m, dict) and m.get("sender") != session_user and m.get("timestamp", "") > u_last)
        
        p2p_badge = f"🟢 {unread_p2p_cnt}" if unread_p2p_cnt > 0 else ""
        gen_badge = f"💬 {unread_gen_cnt}" if unread_gen_cnt > 0 else ""
        
        selected_subject = st.sidebar.selectbox("📚 Select Academic Subject Field", allowed_subjects)
        
        workspace_list = [
            "📝 Access Exam Center", 
            "🔊 Subject Group Discussion Arena",
            "🤝 Synchronized Partner Exam Center",
            "📚 Read Revision Notes",
            "👥 Global Student Directory",
            "🤝 Partner Connection Hub", 
            f"🌐 General Lounge Chat {gen_badge}", 
            f"🔒 Private Peer Chatroom {p2p_badge}", 
            "📊 Progress Tracker Logs", 
            "📁 Finished Exam Vault", 
            "🔑 Change Account Password", 
            "📩 Submit App Suggestions"
        ]
        
        if client_default_nav not in workspace_list:
            client_default_nav = "📝 Access Exam Center"
            
        client_tab_choice = st.sidebar.radio("Workspace Channels", workspace_list, index=workspace_list.index(client_default_nav) if client_default_nav in workspace_list else 0)

        # Unified Automated Microsecond Scoring and Grading Engine
        def run_microsecond_scoring_engine(typed_work, current_two_items):
            all_keywords = ",".join([item.get('keywords', '') for item in current_two_items if isinstance(item, dict)])
            keywords_list = [k.strip().lower() for k in all_keywords.split(",") if k.strip()]
            matched_keys = [k for k in keywords_list if k in typed_work.lower()]
            
            combined_solution_len = sum([len(item.get('solution', '')) for item in current_two_items if isinstance(item, dict)])
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
            
            blueprints = " | ".join([f"[Q{i+1} Numerical Answer: {item.get('numerical','')} -> Marking Guide Checklist: {item.get('solution','')}]" for i, item in enumerate(current_two_items) if isinstance(item, dict)])
            return calculated_score, grade, f"**[OFFICIAL NCDC SOLUTION BLUEPRINT]** {blueprints}"

        # --- EXAM CENTER ---
        if client_tab_choice == "📝 Access Exam Center":
            st.title("📝 Precision Topic Exam Center")
            
            if f"exam_active_{session_uid}" not in st.session_state: st.session_state[f"exam_active_{session_uid}"] = False
            if f"exam_submitted_{session_uid}" not in st.session_state: st.session_state[f"exam_submitted_{session_uid}"] = False
            if f"current_exam_batch_{session_uid}" not in st.session_state: st.session_state[f"current_exam_batch_{session_uid}"] = 0
            if f"last_instant_feedback_{session_uid}" not in st.session_state: st.session_state[f"last_instant_feedback_{session_uid}"] = ""

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
                                if parts[0].strip() == selected_subject:
                                    if selected_topic_target == "All Topics" or parts[1].strip() == selected_topic_target:
                                        active_exam_list.append({
                                            "question": q_text, "solution": parts[2].strip(), 
                                            "numerical": parts[3].strip(), "keywords": parts[4].strip(), "topic": parts[1].strip()
                                        })
                    except Exception: pass

                if not active_exam_list:
                    active_exam_list = [
                        {"question": "Calculate fluid velocity mechanics variation patterns instance Alpha.", "solution": "Establish uniform coordinate tracks, configure vector parameters.", "numerical": "1497.6", "keywords": "velocity, parameters", "topic": "General Concepts"},
                        {"question": "Calculate fluid velocity mechanics variation patterns instance Beta.", "solution": "Configure vector parameters, and compute numerical limits.", "numerical": "1177.2", "keywords": "vector, limits", "topic": "General Concepts"}
                    ]

                batch_start = st.session_state[f"current_exam_batch_{session_uid}"] * 2
                if batch_start >= len(active_exam_list):
                    batch_start = 0
                    st.session_state[f"current_exam_batch_{session_uid}"] = 0
                    
                current_two_items = active_exam_list[batch_start:batch_start + 2]

                st.markdown("### ✍️ Active Test Assignment (2 Questions Active)")
                for index, item in enumerate(current_two_items, 1):
                    st.markdown(f"<div style='background-color:#1e1e1e; padding:15px; border-radius:6px; margin-top:10px; border-left:4px solid #ff3333;'><strong>Question {index}:</strong> {item.get('question','')}</div>", unsafe_allow_html=True)
                
                typed_work = st.text_area("Type your step-by-step structural analytical solutions for both items here:", key=f"exam_text_{batch_start}")
                uploaded_photo = st.file_uploader("📸 Upload Handwritten Script Photo:", type=["jpg", "jpeg", "png"], key=f"exam_img_{batch_start}")

                if not st.session_state[f"exam_submitted_{session_uid}"]:
                    if st.button("🚀 Transmit Answers Script"):
                        if typed_work.strip() or uploaded_photo is not None:
                            calc_score, grade, full_structured_sol = run_microsecond_scoring_engine(typed_work, current_two_items)
                            
                            if session_uid not in st.session_state["exam_vault"]: st.session_state["exam_vault"][session_uid] = []
                            st.session_state["exam_vault"][session_uid].append({
                                "Subject": selected_subject, "Topic": current_two_items[0].get('topic','General'), "Date": str(datetime.date.today()),
                                "Questions": " & ".join([item.get('question','') for item in current_two_items if isinstance(item, dict)]), "Your_Work": typed_work, 
                                "Grade": grade, "Status": f"Scored: {calc_score}%", "Score_Raw": calc_score, "Feedback_Solution": full_structured_sol
                            })
                            save_cache_to_disk("db_exams.json", st.session_state["exam_vault"])
                            
                            st.session_state[f"last_instant_feedback_{session_uid}"] = full_structured_sol
                            st.session_state[f"exam_submitted_{session_uid}"] = True
                            st.rerun()
                else:
                    st.markdown("### 📊 Initial Evaluation Breakdown Result")
                    latest_rec = st.session_state["exam_vault"][session_uid][-1]
                    st.info(f"**Grade:** {latest_rec.get('Grade')} | **Status:** {latest_rec.get('Status')}")
                    st.markdown(f"""
                        <div style='background-color:#112211; padding:18px; border-radius:6px; border:2px solid #22aa22; color:#ddffdd;'>
                            <strong>Marking Keys & Detailed Blueprint Explanations:</strong><br><br>
                            {st.session_state[f"last_instant_feedback_{session_uid}"]}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🔄 Load Next 2 Random Questions"):
                        st.session_state[f"current_exam_batch_{session_uid}"] += 1
                        st.session_state[f"exam_submitted_{session_uid}"] = False
                        st.rerun()

        # --- 🔊 SUBJECT GROUP DISCUSSION ARENA ---
        elif client_tab_choice == "🔊 Subject Group Discussion Arena":
            st.title(f"🔊 Collaborative Discussion Panel — {selected_subject}")
            
            if selected_subject not in st.session_state["group_discussions"]:
                st.session_state["group_discussions"][selected_subject] = {
                    "leader": "",
                    "messages": [],
                    "active_question": None,
                    "reveal_solution": False,
                    "hands_raised": []
                }
            
            grp = st.session_state["group_discussions"][selected_subject]
            
            if grp["leader"] != "" and session_user != grp["leader"] and st.session_state["user_forum_presence"].get(f"{session_user}_{selected_subject}") is None:
                st.markdown("<div class='system-warn-box'>🛰️ CHATROOM GATEWAY ENTRY GATE</div>", unsafe_allow_html=True)
                st.info(f"An active study cluster session is currently run by Group Leader: @{grp['leader']}. Select your interaction profile mode to continue down-loop:")
                col_join1, col_join2 = st.columns(2)
                with col_join1:
                    if st.button("🔥 Actively Engage & Participate"):
                        st.session_state["user_forum_presence"][f"{session_user}_{selected_subject}"] = "Active Participant"
                        st.rerun()
                with col_join2:
                    if st.button("👁️ Stay as Passive Observer"):
                        st.session_state["user_forum_presence"][f"{session_user}_{selected_subject}"] = "Observer Only"
                        st.rerun()
                st.stop()
            
            if not grp["leader"]:
                st.info("No active session leader assigned for this subject channel. Open the link to assume leadership responsibilities.")
                if st.button("👑 Initialize Open Discussion Session & Become Leader"):
                    grp["leader"] = session_user
                    st.session_state["user_forum_presence"][f"{session_user}_{selected_subject}"] = "Session Leader"
                    save_cache_to_disk("db_group_discussions.json", st.session_state["group_discussions"])
                    st.rerun()
            else:
                st.success(f"👑 Ongoing Live Session Leader: **@{grp['leader']}**")
                if session_user == grp["leader"]:
                    if st.button("🛑 Abandon/Close Session Leadership"):
                        grp["leader"] = ""
                        grp["active_question"] = None
                        grp["reveal_solution"] = False
                        save_cache_to_disk("db_group_discussions.json", st.session_state["group_discussions"])
                        st.rerun()
            
            st.markdown("<div class='meet-panel-card'><h4>📺 Interactive Collaboration Utilities Panel</h4>", unsafe_allow_html=True)
            col_meet1, col_meet2, col_meet3 = st.columns([3, 3, 6])
            
            with col_meet1:
                if session_user in grp["hands_raised"]:
                    if st.button("✋ Lower Hand (Google Meet Style)"):
                        grp["hands_raised"].remove(session_user)
                        save_cache_to_disk("db_group_discussions.json", st.session_state["group_discussions"])
                        st.rerun()
                else:
                    if st.button("✋ Raise Hand to Speak/Answer"):
                        grp["hands_raised"].append(session_user)
                        save_cache_to_disk("db_group_discussions.json", st.session_state["group_discussions"])
                        st.rerun()
                        
            with col_meet2:
                if grp["hands_raised"] and session_user == grp["leader"]:
                    if st.button("♻️ Flush/Clear Raise Hand Queue"):
                        grp["hands_raised"] = []
                        save_cache_to_disk("db_group_discussions.json", st.session_state["group_discussions"])
                        st.rerun()
                        
            with col_meet3:
                if grp["hands_raised"]:
                    hands_str = ", ".join([f"@{u}" for u in grp["hands_raised"]])
                    st.markdown(f"**Speaker Queue:** <span class='hand-raised-badge'>Active Nodes</span> {hands_str}", unsafe_allow_html=True)
                else:
                    st.write("Speaker Queue is clear.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if session_user == grp["leader"]:
                st.markdown("### 🎛️ Leader Question Stream Controllers")
                col_lq1, col_lq2 = st.columns(2)
                with col_lq1:
                    if st.button("🎯 Inject 1 Live Random Exam Question onto Dashboard"):
                        sheet_data = read_public_sheet(selected_subject)
                        pool = []
                        if sheet_data is not None and not sheet_data.empty:
                            try:
                                for idx, row in sheet_data.iterrows():
                                    parts = str(row.iloc[1]).split("||")
                                    if len(parts) >= 5 and parts[0].strip() == selected_subject:
                                        pool.append({"question": str(row.iloc[0]), "solution": parts[2].strip(), "numerical": parts[3].strip(), "keywords": parts[4].strip(), "topic": parts[1].strip()})
                            except Exception: pass
                        if not pool:
                            pool = [{"question": "Evaluate core subject system properties variant matrix alpha.", "solution": "Apply standard NCDC vector projections.", "numerical": "99.4", "keywords": "vector", "topic": "General"}]
                        
                        grp["active_question"] = random.choice(pool)
                        grp["reveal_solution"] = False
                        save_cache_to_disk("db_group_discussions.json", st.session_state["group_discussions"])
                        st.rerun()
                with col_lq2:
                    if grp["active_question"]:
                        if st.button("🔓 Force-Reveal Full NCDC Working Answers Block"):
                            grp["reveal_solution"] = True
                            save_cache_to_disk("db_group_discussions.json", st.session_state["group_discussions"])
                            st.rerun()
            
            if grp.get("active_question"):
                st.markdown(f"""
                <div style='background-color:#161b22; padding:20px; border-radius:8px; border-left:5px solid #ff3333; margin-bottom:15px;'>
                    <span style='color:#ff3333; font-weight:bold; font-size:12px;'>📡 SHARED GROUP BILLBOARD LIVE TOPIC: {grp['active_question'].get('topic')}</span>
                    <h4 style='margin:8px 0; color:#ffffff;'>{grp['active_question'].get('question')}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                if grp.get("reveal_solution"):
                    st.markdown(f"""
                    <div style='background-color:#0f2619; border:1px solid #2ea44f; padding:15px; border-radius:6px; color:#c9d1d9; margin-bottom:15px;'>
                        <strong style='color:#2ea44f;'>✅ MASTER SOLUTION WORKINGS BLUEPRINT KEY:</strong><br><br>
                        <strong>Numerical Metric Target Answer:</strong> {grp['active_question'].get('numerical')}<br>
                        <strong>NCDC Standard Evaluation Rubric Workings:</strong> {grp['active_question'].get('solution')}
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("### 💬 Shared Workspace Stream Channel")
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in grp.get("messages", []):
                if isinstance(msg, dict):
                    m_sender = msg.get("sender", "Anonymous")
                    m_text = msg.get("text", "")
                    m_ts = msg.get("timestamp", "")
                    m_media = msg.get("media", None)
                    m_audio = msg.get("audio_note", False)
                    m_react = msg.get("reactions", {})
                    
                    side_class = "chat-right" if m_sender == session_user else "chat-left"
                    ticks = '<span class="whatsapp-ticks">✓✓</span>' if m_sender == session_user else ''
                    
                    media_html = ""
                    if m_media:
                        media_html = f'<div class="chat-media-box">📁 <strong>{m_media.get("type")}:</strong> {m_media.get("name")}</div>'
                    elif m_audio:
                        media_html = '<div class="audio-note-box">🎵 🎤 ⚡ Audio Note Transmitted File Message Playback [0:08]</div>'
                        
                    react_html = ""
                    if m_react:
                        react_html = f"<div style='font-size:12px; margin-top:4px; background:rgba(255,255,255,0.1); display:inline-block; padding:2px 5px; border-radius:10px;'>{' '.join([f'{u}:{e}' for u, e in m_react.items()])}</div>"
                        
                    st.markdown(f'<div class="chat-bubble {side_class}"><strong>@{m_sender}:</strong> {m_text}{media_html}{react_html}<span class="chat-timestamp">{m_ts} {ticks}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            with st.form("group_message_form", clear_on_submit=True):
                grp_txt = st.text_input("Type contribution ideas / texts / WhatsApp GIFs codes...", key="grp_txt_in")
                grp_file = st.file_uploader("📎 Upload target payload arrays:", type=["jpg", "jpeg", "png", "pdf", "txt", "xlsx"], key="grp_file_in")
                audio_checkbox_payload = st.checkbox("🎤 Trigger Audio Message Capture Mic", key="grp_audio_mic")
                
                st.markdown("**Select WhatsApp Reaction/Sticker:**")
                react_selection = st.selectbox("Choose reaction node to apply:", ["None", "👍 Like", "❤️ Heart", "😂 Laugh", "😮 Wow", "⭐ [Sticker]", "🎬 [GIF Data]"])
                
                grp_submit_trigger = st.form_submit_button("Transmit Packet to Shared Stream Room 🚀")
                
                if grp_submit_trigger:
                    if grp_txt.strip() or grp_file is not None or audio_checkbox_payload or react_selection != "None":
                        meta_pack = {"name": grp_file.name, "type": f"{grp_file.name.split('.')[-1].upper()} Item"} if grp_file else None
                        txt_val = grp_txt.strip()
                        
                        if not txt_val and audio_checkbox_payload:
                            txt_val = "🎙️ Transmitted Audio Message Packet Layer"
                        elif not txt_val and react_selection != "None":
                            txt_val = f"Shared Reaction Node {react_selection}"
                            
                        react_map = {session_user: react_selection.split(" ")[0]} if react_selection != "None" else {}
                        
                        grp["messages"].append({
                            "sender": session_user, "text": txt_val if txt_val else "📄 Checked in.",
                            "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                            "media": meta_pack, "audio_note": audio_checkbox_payload, "reactions": react_map
                        })
                        save_cache_to_disk("db_group_discussions.json", st.session_state["group_discussions"])
                        st.rerun()

        # --- 🤝 SYNCHRONIZED PARTNER EXAM CENTER ---
        elif client_tab_choice == "🤝 Synchronized Partner Exam Center":
            st.title("🤝 Real-Time Mutual Partner Exam Center")
            
            if not session_partner:
                st.warning("⚠️ Terminal Lock: Establish an active link inside the Partner Connection Hub to use this sync system.")
            else:
                sorted_pair = sorted([session_user, session_partner])
                session_key = f"cluster_{sorted_pair[0]}_{sorted_pair[1]}"
                
                if session_key not in st.session_state["mutual_exam_sessions"]:
                    st.session_state["mutual_exam_sessions"][session_key] = {
                        "subject": "Mathematics", "topic": "General Concepts",
                        "questions": [], "active": False, "submissions": {}, "timestamp": time.time()
                    }
                
                cluster = st.session_state["mutual_exam_sessions"][session_key]
                
                st.markdown(f"""
                    <div class="partner-live-badge">🟢 Connected Tunnel: {session_user} ⇄ {session_partner}</div>
                    <p>Current Role: <strong>{session_partner_role}</strong></p>
                """, unsafe_allow_html=True)
                
                if session_partner_role == "Session Leader":
                    st.markdown("### 👑 Leader Admin Control Console")
                    sync_sub = st.selectbox("Configure Mutual Subject Target:", allowed_subjects, index=allowed_subjects.index(cluster.get("subject", allowed_subjects[0])) if cluster.get("subject") in allowed_subjects else 0)
                    official_topics = NCDC_CURRICULUM_MAP.get(sync_sub, ["General Concepts"])
                    sync_top = st.selectbox("Configure Mutual Topic Target:", official_topics, index=official_topics.index(cluster.get("topic", official_topics[0])) if cluster.get("topic") in official_topics else 0)
                    
                    if st.button("🎲 Generate & Sync Mutual Exam Questions"):
                        sheet_data = read_public_sheet(sync_sub)
                        pool = []
                        if sheet_data is not None and not sheet_data.empty:
                            try:
                                for idx, row in sheet_data.iterrows():
                                    parts = str(row.iloc[1]).split("||")
                                    if len(parts) >= 5 and parts[0].strip() == sync_sub and parts[1].strip() == sync_top:
                                        pool.append({"question": str(row.iloc[0]), "solution": parts[2].strip(), "numerical": parts[3].strip(), "keywords": parts[4].strip(), "topic": sync_top})
                            except Exception: pass
                        
                        if len(pool) < 2:
                            pool = [
                                {"question": f"[{sync_top}] Sync Problem Item Challenge Protocol Alpha.", "solution": "Uniform vector matrix analysis.", "numerical": "44.2", "keywords": "matrix, analysis", "topic": sync_top},
                                {"question": f"[{sync_top}] Sync Problem Item Challenge Protocol Beta.", "solution": "Execute derivative limits trace maps.", "numerical": "180", "keywords": "derivative, trace", "topic": sync_top}
                            ]
                        
                        sampled_items = random.sample(pool, 2) if len(pool) >= 2 else pool[:2]
                        st.session_state["mutual_exam_sessions"][session_key] = {
                            "subject": sync_sub, "topic": sync_top, "questions": sampled_items,
                            "active": True, "submissions": {}, "timestamp": time.time()
                        }
                        save_cache_to_disk("db_mutual_exams.json", st.session_state["mutual_exam_sessions"])
                        st.success("✔ Mutual payload successfully broadcast to both partner phones!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("⌛ Awaiting Session Leader to generate or change mutual exam payload arrays...")
                    if st.button("🔄 Poll/Refresh Partner Stream Updates"): st.rerun()
                
                if cluster.get("active") and cluster.get("questions"):
                    st.markdown("---")
                    st.error(f"🚨 LIVE EXAM RUNNING: {cluster.get('subject')} -> {cluster.get('topic')}")
                    
                    for idx, q in enumerate(cluster.get("questions", []), 1):
                        st.markdown(f"<div style='background-color:#121212; padding:15px; border-radius:6px; margin-bottom:10px; border-left:4px solid #ff3333;'><strong>Mutual Item {idx}:</strong> {q.get('question','')}</div>", unsafe_allow_html=True)
                    
                    user_typed = st.text_area("Your Script Work Submissions Matrix Block:", key="mutual_user_work")
                    uploaded_photo = st.file_uploader("📸 Optional Handwritten Verification Image Capture File Upload:", type=["jpg", "jpeg", "png"], key="mutual_user_img")
                    
                    submissions_map = cluster.get("submissions", {})
                    if session_user not in submissions_map:
                        if st.button("🚀 Commit Mutual Script Submission"):
                            if user_typed.strip() or uploaded_photo is not None:
                                score, grade, feedback = run_microsecond_scoring_engine(user_typed, cluster.get("questions", []))
                                
                                if session_uid not in st.session_state["exam_vault"]: st.session_state["exam_vault"][session_uid] = []
                                st.session_state["exam_vault"][session_uid].append({
                                    "Subject": cluster.get("subject"), "Topic": cluster.get("topic"), "Date": str(datetime.date.today()),
                                    "Questions": " [MUTUAL] " + " & ".join([i.get('question','') for i in cluster.get("questions", []) if isinstance(i, dict)]), "Your_Work": user_typed, 
                                    "Grade": grade, "Status": f"Scored: {score}%", "Score_Raw": score, "Feedback_Solution": feedback
                                })
                                save_cache_to_disk("db_exams.json", st.session_state["exam_vault"])
                                
                                if "submissions" not in st.session_state["mutual_exam_sessions"][session_key]:
                                    st.session_state["mutual_exam_sessions"][session_key]["submissions"] = {}
                                st.session_state["mutual_exam_sessions"][session_key]["submissions"][session_user] = {
                                    "score": score, "grade": grade, "work": user_typed, "feedback": feedback
                                }
                                save_cache_to_disk("db_mutual_exams.json", st.session_state["mutual_exam_sessions"])
                                st.success("Submission cataloged! Waiting for partner tracking evaluation layers...")
                                time.sleep(1)
                                st.rerun()
                    else:
                        st.success("✔ Your work structural response is transmitted successfully.")
                    
                    st.markdown("<div class='partner-vs-box'><h3>📊 Cross-Terminal Live Scoreboard Grid</h3>", unsafe_allow_html=True)
                    col_user1, col_user2 = st.columns(2)
                    with col_user1:
                        st.markdown(f"#### 👤 Your Terminal ({session_user})")
                        if session_user in submissions_map:
                            sub = submissions_map[session_user]
                            st.metric("Your Score Metric", f"{sub.get('score')}%", sub.get('grade'))
                        else:
                            st.warning("Pending submission...")
                    with col_user2:
                        st.markdown(f"#### 👥 Partner Terminal ({session_partner})")
                        if session_partner in submissions_map:
                            sub = submissions_map[session_partner]
                            st.metric("Partner Score Metric", f"{sub.get('score')}%", sub.get('grade'))
                        else:
                            st.warning("Partner still writing scripts loops...")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    if session_user in submissions_map:
                        with st.expander("👁 Review NCDC Blueprint Analytical Correction Sheet Keys"):
                            st.markdown(submissions_map[session_user].get("feedback", ""))

        # --- REVISION NOTES HUB ---
        elif client_tab_choice == "📚 Read Revision Notes":
            st.title("📚 Academic Revision Notes Hub")
            notes_filtered = [n for n in st.session_state.get("revision_notes_db", []) if isinstance(n, dict) and n.get("Subject") == selected_subject]
            
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
                    
                    st.download_button(
                        label="📥 Download This Study Note (One-Tap)",
                        data=f"ACADEMIC SHIELD PRO STUDY GUIDE\nTitle: {note.get('Title')}\nSubject: {note.get('Subject')}\nContent:\n{note.get('Content')}",
                        file_name=f"Revision_Note_{str(note.get('Title')).replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"dl_note_{idx}"
                    )

        # --- GLOBAL STUDENT DIRECTORY ---
        elif client_tab_choice == "👥 Global Student Directory":
            st.title("👥 Global Student Directory Panel")
            
            for uid, node in st.session_state["users_registry"].items():
                if uid == session_uid: continue
                    
                st.markdown(f"""
                <div class="directory-card">
                    <h3 style="color:#ff3333; margin:0;">👤 {node.get('name', 'Anonymous Student')} (@{node.get('username')})</h3>
                    <p style="margin:4px 0;">🏫 <strong>Institution:</strong> {node.get('school')} | <strong>Grade Class:</strong> {node.get('class')}</p>
                    <p style="margin:4px 0;">📍 <strong>District Area:</strong> {node.get('location', 'Kampala')} | <strong>Gender:</strong> {node.get('gender')}</p>
                    <p style="margin:4px 0; color:#aaaaaa;">📚 <strong>Subject Combination Combo:</strong> {", ".join(node.get('subjects', []))}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_dir_chat, col_dir_pair, _ = st.columns([2, 3, 5])
                with col_dir_chat:
                    if st.button(f"💬 Chat with {node.get('username')}", key=f"dir_chat_{uid}"):
                        st.session_state["users_registry"][session_uid]["partner"] = node.get("username")
                        st.session_state["users_registry"][session_uid]["partner_role"] = "Session Leader"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.session_state["nav_target_override"] = f"🔒 Private Peer Chatroom {p2p_badge}"
                        st.rerun()
                with col_dir_pair:
                    if st.button(f"🤝 Request Partnership / Connect", key=f"dir_pair_{uid}"):
                        st.session_state["users_registry"][session_uid]["partner"] = node.get("username")
                        st.session_state["users_registry"][session_uid]["partner_role"] = "Session Leader"
                        
                        for sub_uid, sub_node in st.session_state["users_registry"].items():
                            if sub_node.get("username") == node.get("username"):
                                st.session_state["users_registry"][sub_uid]["partner"] = session_user
                                st.session_state["users_registry"][sub_uid]["partner_role"] = "Session Follower"
                                
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.success(f"✔ Synchronized Partner link established with {node.get('username')}!")
                        time.sleep(1)
                        st.rerun()
                st.markdown("<hr style='border: 1px solid #1a1a1a; margin: 10px 0 25px 0;'>", unsafe_allow_html=True)

        # --- PARTNER CONNECTION HUB ---
        elif client_tab_choice == "🤝 Partner Connection Hub":
            st.title("🤝 Elite Academic Partner Pairing Hub")
            
            current_p = st.session_state["users_registry"][session_uid].get("partner", "")
            if current_p:
                st.success(f"⚡ Currently paired with academic wingman: **{current_p}** | Assigned Tag Position: {session_partner_role}")
                if st.button("💔 Break Pair Connection"):
                    st.session_state["users_registry"][session_uid]["partner"] = ""
                    st.session_state["users_registry"][session_uid]["partner_role"] = "Standalone"
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.rerun()
            else:
                st.info("Status: Standalone independent terminal.")
                potential_partners = [u["username"] for k, u in st.session_state["users_registry"].items() if k != session_uid and u["username"] != "Admin"]
                if potential_partners:
                    chosen_p = st.selectbox("Select target account to pair links:", potential_partners)
                    if st.button("🔗 Establish Unified Connection Link"):
                        st.session_state["users_registry"][session_uid]["partner"] = chosen_p
                        st.session_state["users_registry"][session_uid]["partner_role"] = "Session Leader"
                        
                        for sub_uid, sub_node in st.session_state["users_registry"].items():
                            if sub_node.get("username") == chosen_p:
                                st.session_state["users_registry"][sub_uid]["partner"] = session_user
                                st.session_state["users_registry"][sub_uid]["partner_role"] = "Session Follower"
                                
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.success(f"Pairing link initialized with {chosen_p}!")
                        st.rerun()

        # --- GLOBAL LOUNGE CHAT ---
        elif client_tab_choice.startswith("🌐 General Lounge Chat"):
            st.title("🌐 General Lounge Peer Chatroom")
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state["general_chat"]:
                if isinstance(msg, dict):
                    msg_sender = msg.get("sender", "Anonymous")
                    msg_text = msg.get("text", "")
                    msg_timestamp = msg.get("timestamp", "")
                    msg_media = msg.get("media", None)
                    msg_audio = msg.get("audio_note", False)
                    
                    side_class = "chat-right" if msg_sender == session_user else "chat-left"
                    ticks = '<span class="whatsapp-ticks">✓✓</span>' if msg_sender == session_user else ''
                    
                    media_html = ""
                    if msg_media:
                        media_html = f'<div class="chat-media-box">📁 <strong>{msg_media.get("type", "File")}:</strong> {msg_media.get("name", "Document")}</div>'
                    elif msg_audio:
                        media_html = '<div class="audio-note-box">🎵 🎤 ⚡ Audio Note Transmitted File Message Playback [0:05]</div>'
                    
                    st.markdown(f'<div class="chat-bubble {side_class}"><strong>{msg_sender}:</strong> {msg_text}{media_html}<span class="chat-timestamp">{msg_timestamp} {ticks}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            with st.form("gen_message_form", clear_on_submit=True):
                gen_text_input = st.text_input("Type community broadcast chat message...")
                gen_audio_trigger = st.checkbox("🎤 Add Audio Mic Notes", key="gen_mic_bool")
                gen_file = st.file_uploader("📎 Attach Rich Media Payload:", type=["jpg", "jpeg", "png", "mp4", "mp3", "pdf", "txt"])
                gen_submit_trigger = st.form_submit_button("Send 🚀")
                
                if gen_submit_trigger:
                    if gen_text_input.strip() or gen_file is not None or gen_audio_trigger:
                        media_meta = {"name": gen_file.name, "type": f"{gen_file.name.split('.')[-1].upper()} Document"} if gen_file else None
                        txt_display = gen_text_input.strip()
                        if not txt_display and gen_audio_trigger:
                            txt_display = "🎙️ Sent a localized voice message layer."
                        
                        st.session_state["general_chat"].append({"sender": session_user, "text": txt_display if txt_display else "📁 Shared an attachment payload.", "timestamp": datetime.datetime.now().strftime("%I:%M %p"), "media": media_meta, "audio_note": gen_audio_trigger})
                        st.session_state["last_read_tracker"][session_user] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_cache_to_disk("db_genchat.json", st.session_state["general_chat"])
                        save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
                        st.rerun()

        # --- PRIVATE CHATROOM ---
        elif client_tab_choice.startswith("🔒 Private Peer Chatroom"):
            st.title("🔒 Private Partner Chatroom")
            if not session_partner.strip(): 
                st.warning("⚠️ Access Locked: Pair inside Partner Hub channels to map out secure chat routes.")
            else:
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                for msg in st.session_state["private_chats"]:
                    if isinstance(msg, dict):
                        msg_sender = msg.get("sender", "")
                        msg_to = msg.get("to", "")
                        msg_text = msg.get("text", "")
                        msg_timestamp = msg.get("timestamp", "")
                        msg_media = msg.get("media", None)
                        msg_audio = msg.get("audio_note", False)
                        
                        if (msg_sender == session_user and msg_to == session_partner) or (msg_sender == session_partner and msg_to == session_user) or (msg_sender == "SYSTEM_SHIELD_BOT" and msg_to == session_user):
                            side_class = "chat-right" if msg_sender == session_user else "chat-left"
                            ticks = '<span class="whatsapp-ticks">✓✓</span>' if msg_sender == session_user else ''
                            
                            media_html = ""
                            if msg_media:
                                media_html = f'<div class="chat-media-box">📁 <strong>{msg_media.get("type", "File")}:</strong> {msg_media.get("name", "Media")}</div>'
                            elif msg_audio:
                                media_html = '<div class="audio-note-box">🎵 🎤 ⚡ Audio Note Transmitted File Message Playback [0:06]</div>'
                                
                            st.markdown(f'<div class="chat-bubble {side_class}"><strong>{msg_sender}:</strong> {msg_text}{media_html}<span class="chat-timestamp">{msg_timestamp} {ticks}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.form("p2p_message_form", clear_on_submit=True):
                    p2p_text_input = st.text_input("Type confidential messaging nodes...")
                    p2p_audio_trigger = st.checkbox("🎤 Add Audio Mic Notes", key="p2p_mic_bool")
                    p2p_file = st.file_uploader("📎 Upload Rich Media Files to Partner Channel:", type=["jpg", "jpeg", "png", "mp4", "mp3", "pdf", "txt"])
                    p2p_submit_trigger = st.form_submit_button("Send 🔐")
                    
                    if p2p_submit_trigger:
                        if p2p_text_input.strip() or p2p_file is not None or p2p_audio_trigger:
                            media_meta = {"name": p2p_file.name, "type": f"{p2p_file.name.split('.')[-1].upper()} Media"} if p2p_file else None
                            txt_display = p2p_text_input.strip()
                            if not txt_display and p2p_audio_trigger:
                                txt_display = "🎙️ Sent a confidential secure audio track node."
                                
                            st.session_state["private_chats"].append({"sender": session_user, "to": session_partner, "text": txt_display if txt_display else "📁 Sent a multi-media payload.", "timestamp": datetime.datetime.now().strftime("%I:%M %p"), "media": media_meta, "audio_note": p2p_audio_trigger})
                            st.session_state["last_read_tracker"][session_user] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            save_cache_to_disk("db_p2pchat.json", st.session_state["private_chats"])
                            save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
                            st.rerun()

        # --- PROGRESS TRACKER LOGS & UPGRADED STANDINGS ---
        elif client_tab_choice == "📊 Progress Tracker Logs":
            st.title("📊 Performance Growth Metrics Analytics")
            user_history = st.session_state["exam_vault"].get(session_uid, [])
            
            if not user_history: st.info("No records completed to build analytics tracks yet.")
            else:
                col_m1, col_m2, col_m3 = st.columns(3)
                scores_list = [int(str(e.get("Status","")).split(":")[1].replace("%","").strip()) if "Status" in e and ":" in str(e.get("Status","")) else int(e.get("Score_Raw",0)) for e in user_history if isinstance(e, dict)]
                
                if scores_list:
                    with col_m1: st.markdown(f'<div class="metric-card"><h5>📝 Total Exams Attempted</h5><h2>{len(user_history)} Items</h2></div>', unsafe_allow_html=True)
                    with col_m2: st.markdown(f'<div class="metric-card"><h5>📈 Mean Mastery Percentage</h5><h2>{sum(scores_list)/len(scores_list):.1f}%</h2></div>', unsafe_allow_html=True)
                    with col_m3: st.markdown(f'<div class="metric-card"><h5>🏆 Peak Evaluation Score</h5><h2>{max(scores_list)}% Target</h2></div>', unsafe_allow_html=True)
                    
                    st.line_chart(pd.DataFrame({"Your Score (%)": scores_list}, index=[f"Exam #{i+1}" for i in range(len(scores_list))]), y="Your Score (%)")
                st.dataframe(pd.DataFrame(user_history)[[c for c in ["Subject", "Topic", "Date", "Grade", "Status"] if c in pd.DataFrame(user_history).columns]])

            # Real-Time Upgraded Dream League Standing Tables Core Matrix Block
            st.markdown("---")
            st.markdown("### 🏆 Live Dynamic Community Tournament Standings")
            
            # Master Array calculations for tournament participants
            standings_data = [
                {"Rank": 1, "Club Squad": "Setra FC 👑", "P": 6, "W": 5, "D": 1, "L": 0, "GF": 16, "GA": 4, "GD": +12, "PTS": 16, "Form Matrix": "🟢 🟢 🟢 🟡 🟢 🟢"},
                {"Rank": 2, "Club Squad": "Victoria FC", "P": 6, "W": 4, "D": 0, "L": 2, "GF": 11, "GA": 7, "GD": +4, "PTS": 12, "Form Matrix": "🟢 🔴 🟢 🟢 🔴 🟢"},
                {"Rank": 3, "Club Squad": "Chelsea Lite FC", "P": 6, "W": 2, "D": 1, "L": 3, "GF": 8, "GA": 10, "GD": -2, "PTS": 7, "Form Matrix": "🔴 🟡 🟢 🔴 🟢 🔴"},
                {"Rank": 4, "Club Squad": "Smur FC", "P": 6, "W": 0, "D": 0, "L": 6, "GF": 2, "GA": 16, "GD": -14, "PTS": 0, "Form Matrix": "🔴 🔴 🔴 🔴 🔴 🔴"}
            ]
            st.table(pd.DataFrame(standings_data).set_index("Rank"))

        # --- FINISHED EXAM VAULT ---
        elif client_tab_choice == "📁 Finished Exam Vault":
            st.title("📁 Secure Script Archives Vault")
            user_history = st.session_state["exam_vault"].get(session_uid, [])
            if not user_history: st.info("Vault registry empty.")
            else:
                for idx, entry in enumerate(user_history[::-1]):
                    if isinstance(entry, dict):
                        with st.expander(f"📚 {entry.get('Subject')} : {entry.get('Topic')} — [{entry.get('Date')}] — Grade {entry.get('Grade')}"):
                            st.write(f"**Questions Explored:** {entry.get('Questions')}")
                            st.code(f"Your Work Submission Payload:\n{entry.get('Your_Work')}", language="text")
                            st.markdown(f"<div style='background-color:#112211; padding:10px; border-radius:4px; border:1px solid green;'>{entry.get('Feedback_Solution')}</div>", unsafe_allow_html=True)

        # --- CHANGE PASSWORD ---
        elif client_tab_choice == "🔑 Change Account Password":
            st.title("🔑 Update Security Credentials")
            old_p = st.text_input("Enter Current Password:", type="password")
            new_p = st.text_input("Enter New Password:", type="password")
            if st.button("🔐 Rewrite Secure Memory Block"):
                if old_p == st.session_state["users_registry"][session_uid]["pwd"]:
                    st.session_state["users_registry"][session_uid]["pwd"] = new_p
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success("Credentials successfully updated in the secure storage matrix.")

        # --- SUBMIT APP SUGGESTIONS ---
        elif client_tab_choice == "📩 Submit App Suggestions":
            st.title("📩 System Improvement Feedback Channel")
            sug_text = st.text_area("Propose new system updates directly to Admin:")
            if st.button("🚀 Transmit Feedback Packet"):
                if sug_text.strip():
                    st.session_state["suggestions"].append({"id": str(random.randint(10000, 99999)), "User": session_user, "Text": sug_text.strip(), "Time": datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"), "Reply": ""})
                    save_cache_to_disk("db_suggestions.json", st.session_state["suggestions"])
                    st.success("Recommendation saved to the admin queue loops.")
                    st.rerun()
            
            st.markdown("<div class='notes-box'>📢 Permanently Public Suggestions & Admin Responses", unsafe_allow_html=True)
            if not st.session_state["suggestions"]: st.info("No logs found in public feedback frameworks.")
            else:
                for s in st.session_state["suggestions"][::-1]:
                    if isinstance(s, dict):
                        reply_chunk = f"<div class='suggestion-reply-box'><strong>✍️ Admin Response:</strong> {s.get('Reply')}</div>" if s.get('Reply') else "<p style='font-size:12px; color:#666;'>Log Status: Awaiting review...</p>"
                        st.markdown(f'<div class="suggestion-card"><strong>From terminal: {s.get("User")} ({s.get("Time")})</strong><p style="color:#ddd; margin:6px 0;">{s.get("Text")}</p>{reply_chunk}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================
# MODULE C: SYSTEM ADMINISTRATOR HUB (PROTECTED CONTROLS)
# =========================================================================
elif app_mode == "System Administrator Hub":
    st.title("🛡️ System Administrator Core Controller Hub")
    if user_role != "SUPER_ADMIN" and session_user != "Admin":
        st.error("🛑 ACCESS DENIED: High Clearance Required.")
    else:
        st.success("⚡ Identity Match Cleared: Welcome back, Super Administrator.")
        adm_tab = st.tabs(["👥 Student Terminals Registry", "📥 Enrollment Queue Requests", "📢 Live Broadcast Systems", "🖼️ Profile Sync Frame", "📩 User Suggestion Feedback Queue"])
        
        with adm_tab[0]:
            for uid, node in list(st.session_state["users_registry"].items()):
                with st.expander(f"👤 Account: {node.get('name','')} (UID: {uid}) [{node.get('role', 'USER')}]"):
                    st.write(f"**Username:** {node.get('username','')} | **Password Matrix:** {node.get('pwd','')}")
                    st.write(f"**Institution:** {node.get('school','')} | **Authorized Subject Arrays:** {node.get('subjects',[])}")
                    if uid != "0000":
                        current_status = node.get("status","Approved")
                        status_options = ["Approved", "Locked", "Banned"]
                        if current_status not in status_options:
                            status_options.append(current_status)
                        new_stat = st.selectbox(f"Operational State (UID {uid}):", status_options, index=status_options.index(current_status), key=f"adm_stat_{uid}")
                        warn_in = st.text_input(f"Inject warning marquee (UID {uid}):", value=node.get("warning_msg",""), key=f"adm_warn_{uid}")
                        if st.button(f"💾 Lock Changes (UID {uid})"):
                            st.session_state["users_registry"][uid]["status"] = new_stat
                            st.session_state["users_registry"][uid]["warning_msg"] = warn_in
                            save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                            st.success("Registers updated.")
                            st.rerun()

        with adm_tab[1]:
            if not st.session_state["pending_registrations"]: st.info("Queue empty.")
            else:
                for idx, req in enumerate(st.session_state["pending_registrations"]):
                    if isinstance(req, dict):
                        st.markdown(f"**Candidate:** {req.get('name','')} | **Class:** {req.get('class','')} | **School:** {req.get('school','')}")
                        col_acc, col_rej = st.columns(2)
                        with col_acc:
                            if st.button(f"✔ Grant Access (Index {idx})"):
                                new_uid = str(random.randint(1000, 9999))
                                st.session_state["users_registry"][new_uid] = {"username": req.get("username",""), "pwd": req.get("pwd",""), "name": req.get("name",""), "class": req.get("class",""), "school": req.get("school",""), "phone": req.get("phone",""), "email": req.get("email",""), "gender": req.get("gender",""), "location": req.get("location", "Kampala"), "subjects": req.get("subjects",[]), "status": "Approved", "warning_msg": "", "avatar": req.get("avatar",AVATAR_OPTIONS[0]), "partner": "", "partner_role": "Standalone", "role": "USER"}
                                st.session_state["pending_registrations"].pop(idx)
                                save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                                save_cache_to_disk("db_pending.json", st.session_state["pending_registrations"])
                                st.success(f"Approved! Access Token: [{new_uid}]")
                                st.rerun()

        with adm_tab[2]:
            bc_text = st.text_input("Type new live alert banner context string:")
            if st.button("🚀 Push Live Global System Broadcast Alert"):
                st.session_state["global_alerts"].append(bc_text.strip())
                save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                st.success("Alert broadcasted.")

        with adm_tab[3]:
            new_pic_url = st.text_input("Paste photo direct source URL link:", value=st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE))
            if st.button("💾 Apply Global Structural Photo Re-Write"):
                st.session_state["custom_admin_photo"] = new_pic_url.strip()
                save_cache_to_disk("db_admin_photo.json", st.session_state["custom_admin_photo"])
                st.success("System picture sync matrix updated instantly.")

        with adm_tab[4]:
            st.subheader("📩 Incoming Suggestions & Interactive Feedback Queue")
            if not st.session_state["suggestions"]: st.info("No active feedback packets logged by standard users yet.")
            else:
                for idx, s in enumerate(st.session_state["suggestions"]):
                    if isinstance(s, dict):
                        st.markdown(f'<div style="background-color:#1e1e1e; padding:12px; border-radius:4px; margin-bottom:6px; border-left:3px solid #ff3333;"><strong>Sender:</strong> {s.get("User","")} | <strong>Content:</strong> {s.get("Text","")}<br><strong>Current Reply:</strong> {s.get("Reply", "None")}</div>', unsafe_allow_html=True)
                        reply_text_input = st.text_input(f"Draft permanent public response layer:", value=s.get("Reply", ""), key=f"rep_input_{s.get('id', idx)}")
                        if st.button(f"🚀 Broadcast Official Reply (Item {idx+1})", key=f"rep_btn_{s.get('id', idx)}"):
                            st.session_state["suggestions"][idx]["Reply"] = reply_text_input.strip()
                            save_cache_to_disk("db_suggestions.json", st.session_state["suggestions"])
                            st.success("✔ Reply compiled and synced live!")
                            time.sleep(1)
                            st.rerun()

# =========================================================================
# 5. UNIVERSAL IMMUTABLE BRANDING FOOTER LAYER
# =========================================================================
st.markdown("""
    <div class="sudaisi-branding-footer">
        <p style="color: #ffffff; font-family: 'Courier New', Courier, monospace; font-size: 13px; margin: 0; text-align: center;">
            Created by <span style="color: #ff3333; font-weight: bold;">Sudaisi Setra</span>
        </p>
    </div>
""", unsafe_allow_html=True)
