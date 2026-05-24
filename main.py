import streamlit as st
import pandas as pd
import datetime
import random
import os
import json
import time

# =========================================================================
# 1. PLATFORM CONFIGURATIONS & CRASH PREVENTION
# =========================================================================
# Crucial: This must always remain the absolute first command executed
st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Injected CSS to apply the realistic WhatsApp Dark Theme and clean structural grids
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
    
    /* --- WhatsApp Layout UI CSS --- */
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
    .admin-broadcast-banner { background-color: #ff3333; color: white; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    
    div.stButton > button { width: 100% !important; font-weight: bold !important; background-color: #1e1e1e !important; color: #ffffff !important; border: 1px solid #444444 !important; border-radius: 4px !important; }
    div.stButton > button:hover { background-color: #ff3333 !important; color: white !important; border-color: #ff3333 !important; }
    
    .metric-card { background-color: #1a1a1a; padding: 15px; border-radius: 6px; border-left: 4px solid #ff3333; margin-bottom: 10px; }
    .notes-box { background-color: #111111; padding: 20px; border: 1px dashed #444; border-radius: 8px; margin-bottom: 15px; }
    .suggestion-card { background-color: #151515; padding: 15px; border-radius: 6px; margin-bottom: 12px; border-left: 3px solid #005c4b; }
    .suggestion-reply-box { background-color: #1c2826; padding: 10px; border-radius: 4px; margin-top: 8px; border-left: 2px solid #ff3333; font-style: italic; color: #e9edef; }
    .directory-card { background-color: #141414; padding: 18px; border-radius: 8px; border: 1px solid #252525; margin-bottom: 12px; }
    .meet-panel-card { background-color: #141a1e; border: 1px solid #ff3333; border-radius: 8px; padding: 15px; margin-bottom: 15px;}
    .hand-raised-badge { background-color: #ffcc00; color: #000000; font-weight: bold; border-radius: 4px; padding: 2px 6px; font-size: 11px; display: inline-block; margin-left: 6px;}
    .sudaisi-branding-footer { text-align: center; padding: 15px; margin-top: 40px; border-top: 1px solid #222; background-color: #0e0e0e; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# 2. CURRICULUM CONFIGURATIONS & ASSET CONSTANTS
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

SHEET_ID = st.secrets.get("SHEET_ID", "1xU80PotVALVM3sWt7PS3kLGbsivqzMvznXq0c8Cu44M")

def read_public_sheet(worksheet_name):
    export_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={worksheet_name.strip()}"
    try:
        df = pd.read_csv(export_url)
        return df if (df is not None and not df.empty) else None
    except Exception:
        return None

def save_cache_to_disk(filename, data):
    try:
        with open(filename, "w") as f: 
            json.dump(data, f, default=str)
    except Exception: 
        pass

def load_cache_from_disk(filename, default_val):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f: 
                return json.load(f)
        except Exception: 
            pass
    return default_val

# =========================================================================
# 3. DEFENSIVE DATA SELF-HEALING ENGINE (ANTI-CRASH FIXES)
# =========================================================================
def sanitize_chat_list(lst):
    if not isinstance(lst, list): 
        return []
    cleaned = []
    for item in lst:
        if isinstance(item, dict): 
            cleaned.append(item)
        elif isinstance(item, str):
            cleaned.append({"sender": "System", "text": item, "timestamp": "00:00 AM"})
    return cleaned

def sanitize_chat_dict(dct):
    if not isinstance(dct, dict): 
        return {}
    cleaned = {}
    for k, v in dct.items():
        if isinstance(v, dict): 
            cleaned[k] = v
    return cleaned

def sanitize_users_registry(dct):
    if not isinstance(dct, dict) or not dct:
        return {
            "0000": {"username": "Admin", "pwd": "SudaisiAdmin2026", "name": "Sudaisi Setra", "class": "Senior Five", "school": "The Amazima School", "phone": "0752047103", "email": "admin@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry", "Biology"], "status": "Approved", "warning_msg": "", "avatar": "SUDAISI_BAKED", "partner": "", "partner_role": "Standalone", "role": "SUPER_ADMIN"},
            "6601": {"username": "Setra stones", "pwd": "Amazima2026", "name": "Setra Stones", "class": "Senior Five", "school": "The Amazima School", "phone": "0752047103", "email": "setra@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry"], "status": "Approved", "warning_msg": "", "avatar": AVATAR_OPTIONS[0], "partner": "", "partner_role": "Standalone", "role": "USER"}
        }
    for uid, node in dct.items():
        if isinstance(node, dict):
            node["partner"] = node.get("partner", "")
            node["partner_role"] = node.get("partner_role", "Standalone")
            node["status"] = node.get("status", "Approved")
            node["warning_msg"] = node.get("warning_msg", "")
            node["role"] = node.get("role", "USER")
    return dct

# Sync and repair file states live on local disks
if "users_registry" not in st.session_state:
    st.session_state["users_registry"] = sanitize_users_registry(load_cache_from_disk("db_users.json", {}))
if "pending_registrations" not in st.session_state: 
    st.session_state["pending_registrations"] = sanitize_chat_list(load_cache_from_disk("db_pending.json", []))
if "general_chat" not in st.session_state: 
    st.session_state["general_chat"] = sanitize_chat_list(load_cache_from_disk("db_genchat.json", []))
if "private_chats" not in st.session_state: 
    st.session_state["private_chats"] = sanitize_chat_list(load_cache_from_disk("db_p2pchat.json", []))
if "suggestions" not in st.session_state: 
    st.session_state["suggestions"] = sanitize_chat_list(load_cache_from_disk("db_suggestions.json", []))
if "global_alerts" not in st.session_state: 
    st.session_state["global_alerts"] = load_cache_from_disk("db_alerts.json", ["🚀 Platform Online. Secure Mirror Systems Functional."])
if "exam_vault" not in st.session_state: 
    st.session_state["exam_vault"] = load_cache_from_disk("db_exams.json", {})
if "last_read_tracker" not in st.session_state: 
    st.session_state["last_read_tracker"] = load_cache_from_disk("db_readtrack.json", {})
if "generated_registration_codes" not in st.session_state: 
    st.session_state["generated_registration_codes"] = load_cache_from_disk("db_regcodes.json", ["SHIELD2026", "ASP2026"])
if "custom_admin_photo" not in st.session_state: 
    st.session_state["custom_admin_photo"] = load_cache_from_disk("db_admin_photo.json", DEFAULT_SUDAISI_IMAGE)
if "mutual_exam_sessions" not in st.session_state: 
    st.session_state["mutual_exam_sessions"] = load_cache_from_disk("db_mutual_exams.json", {})
if "group_discussions" not in st.session_state: 
    st.session_state["group_discussions"] = sanitize_chat_dict(load_cache_from_disk("db_group_discussions.json", {}))
if "user_forum_presence" not in st.session_state: 
    st.session_state["user_forum_presence"] = {}
if "revision_notes_db" not in st.session_state:
    st.session_state["revision_notes_db"] = [
        {"Title": "Pure Mathematics Vectors Blueprint", "Subject": "Mathematics", "Content": "Vectors core revision summary notes: Unit tracks, relative parameters, and Cartesian projections for P425/1 standards."}
                       ]
    # =========================================================================
# 4. MUTAL SESSION AND NOTIFICATION TRACKING ENGINES
# =========================================================================
def push_system_notification(user_id, alert_text):
    """Safely queues background notification pings to specific accounts."""
    if "last_read_tracker" not in st.session_state:
        st.session_state["last_read_tracker"] = {}
    if user_id not in st.session_state["last_read_tracker"]:
        st.session_state["last_read_tracker"][user_id] = []
    
    timestamp = datetime.datetime.now().strftime("%I:%M %p")
    st.session_state["last_read_tracker"][user_id].append({
        "msg": alert_text,
        "time": timestamp,
        "seen": False
    })
    save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])

def create_blank_progress_card(subjects_list):
    """Generates standard tracking records aligned to NCDC parameters."""
    card = {}
    for sub in subjects_list:
        if sub in NCDC_CURRICULUM_MAP:
            card[sub] = {topic: {"status": "Not Started", "score": 0} for topic in NCDC_CURRICULUM_MAP[sub]}
    return card

# =========================================================================
# 5. USER INTERFACE GATEWAYS (LOGIN / REGISTRATION)
# =========================================================================
if "logged_in_uid" not in st.session_state:
    st.session_state["logged_in_uid"] = None

if st.session_state["logged_in_uid"] is None:
    st.markdown("<h1 style='text-align: center; color: #ff3333;'>🛡️ ACADEMIC SHIELD NETWORK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Ugandan Curriculum Core & Multi-User Collab Infrastructure</p>", unsafe_allow_html=True)
    
    auth_mode = st.radio("Select Portal Gate", ["🔑 System Security Login", "📝 Create Candidate Account"], horizontal=True)
    
    if auth_mode == "🔑 System Security Login":
        with st.form("Login Gateway Terminal"):
            input_username = st.text_input("Candidate Username / ID")
            input_password = st.text_input("Security Access Password", type="password")
            submit_login = st.form_submit_button("AUTHORIZE ACCESS")
            
            if submit_login:
                found_uid = None
                for uid, data in st.session_state["users_registry"].items():
                    if data.get("username") == input_username and data.get("pwd") == input_password:
                        found_uid = uid
                        break
                
                if found_uid:
                    user_node = st.session_state["users_registry"][found_uid]
                    if user_node.get("status", "Approved") == "Suspended":
                        st.error("🚫 Access Revoked. This account has been suspended by the Network Administrator.")
                    elif user_node.get("status", "Approved") == "Pending Review":
                        st.warning("⏳ Account Verification Pending. Please await Super Admin activation clearance.")
                    else:
                        st.session_state["logged_in_uid"] = found_uid
                        st.success(f"🔓 Access Granted. Welcome back, {user_node.get('name')}.")
                        st.rerun()
                else:
                    st.error("❌ Credentials Match Failed. Check your configuration values or code keys.")
                    
    elif auth_mode == "📝 Create Candidate Account":
        with st.form("Registration Intake Module"):
            reg_code = st.text_input("Enter Access Code (Obtained from Admin)")
            reg_uid = st.text_input("Desired Unique ID Number (4 Digits)")
            reg_user = st.text_input("Account Username")
            reg_pwd = st.text_input("Secure Password", type="password")
            reg_name = st.text_input("Full Official Name")
            
            reg_class = st.selectbox("Academic Level Class", ["Senior Five", "Senior Six"])
            reg_school = st.text_input("Institution / School Name", value="The Amazima School")
            reg_phone = st.text_input("Active Phone Connection Contact")
            reg_email = st.text_input("Email Coordinate")
            reg_gender = st.selectbox("Gender", ["Male", "Female"])
            reg_loc = st.text_input("Current Geographical Hub / Location")
            
            selected_subs = st.multiselect("Enrolled Academic Subjects", list(NCDC_CURRICULUM_MAP.keys()), default=["Mathematics"])
            
            submit_reg = st.form_submit_button("SUBMIT APPLICATION TO DATABASE")
            
            if submit_reg:
                if reg_code not in st.session_state["generated_registration_codes"]:
                    st.error("❌ Invalid Access Validation Code.")
                elif not reg_uid or not reg_user or not reg_pwd or not reg_name:
                    st.error("❌ Critical fields cannot remain empty.")
                elif reg_uid in st.session_state["users_registry"]:
                    st.error("❌ Identity Conflict: This 4-Digit ID already exists.")
                else:
                    # Construct clean data format ensuring zero crashes down the line
                    new_profile = {
                        "username": reg_user,
                        "pwd": reg_pwd,
                        "name": reg_name,
                        "class": reg_class,
                        "school": reg_school,
                        "phone": reg_phone,
                        "email": reg_email,
                        "gender": reg_gender,
                        "location": reg_loc,
                        "subjects": selected_subs,
                        "status": "Pending Review",
                        "warning_msg": "",
                        "avatar": random.choice(AVATAR_OPTIONS),
                        "partner": "",
                        "partner_role": "Standalone",
                        "role": "USER",
                        "progress": create_blank_progress_card(selected_subs)
                    }
                    st.session_state["users_registry"][reg_uid] = new_profile
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success("🎯 Registration Request Dispatched! Status set to 'Pending Review'. Please wait for Admin Activation.")

else:
    # Fetch active user context using safe fallbacks
    CURRENT_USER_ID = st.session_state["logged_in_uid"]
    USER_DATA = st.session_state["users_registry"].get(CURRENT_USER_ID, {})
    
    # Emergency fallback check if a profile gets modified in the background
    if not USER_DATA:
        st.session_state["logged_in_uid"] = None
        st.rerun()

    # =========================================================================
    # 6. SIDEBAR COMPARTMENT WORKSPACE NAVIGATION
    # =========================================================================
    with st.sidebar:
        st.markdown(f"<h3 style='color: #ff3333;'>🛡️ SHIELD TERMINAL</h3>", unsafe_allow_html=True)
        
        # Display Avatar Asset Customizations
        avatar_src = USER_DATA.get("avatar", AVATAR_OPTIONS[0])
        if avatar_src == "SUDAISI_BAKED":
            avatar_src = st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE)
            
        st.image(avatar_src, width=85)
        st.markdown(f"**User:** {USER_DATA.get('name')}")
        st.markdown(f"**Role:** `{USER_DATA.get('role')}`")
        
        # Display Active Warning Messages if assigned by Admin
        if USER_DATA.get("warning_msg"):
            st.markdown(f"<div class='system-warn-box'>⚠️ ADMIN ALERT:<br>{USER_DATA.get('warning_msg')}</div>", unsafe_allow_html=True)
            
        st.write("---")
        
        # Standardize Application Architecture Navigation Options
        navigation_nodes = [
            "📋 Operational Dashboard",
            "📊 Personal Progress Tracker",
            "📝 Revision Center & Mock Vault",
            "💬 WhatsApp Lounge Chat",
            "🤝 Partner Connection Hub"
        ]
        
        # Insert Privileged Panels if role criteria matches
        if USER_DATA.get("role") in ["ADMIN", "SUPER_ADMIN"]:
            navigation_nodes.append("⚙️ Super Admin Operations")
            
        selected_workspace = st.radio("Navigate Workspace Channels:", navigation_nodes)
        
        st.write("---")
        if st.button("🔴 SECURE LOGOUT"):
            st.session_state["logged_in_uid"] = None
            st.rerun()
            # =========================================================================
    # 7. ROUTER WORKSPACE CHANNELS
    # =========================================================================
    
    # --- CHANNEL 1: OPERATIONAL DASHBOARD HUB ---
    if selected_workspace == "📋 Operational Dashboard":
        st.markdown(f"<h2>📋 Candidate Workspace Dashboard</h2>", unsafe_allow_html=True)
        
        # Display Live Network Alert Broadcasts managed by Admin
        for alert in st.session_state["global_alerts"]:
            st.markdown(f"<div class='admin-broadcast-banner'>📢 NETWORK ANNOUNCEMENT: {alert}</div>", unsafe_allow_html=True)
            
        # Personalized Metrics Row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-card'><h4>🏫 Center Hub</h4><p>{USER_DATA.get('school')}<br>`{USER_DATA.get('class')}`</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><h4>🧬 Registered Focus</h4><p>{', '.join(USER_DATA.get('subjects', []))}</p></div>", unsafe_allow_html=True)
        with col3:
            partner_id = USER_DATA.get("partner", "")
            partner_name = st.session_state["users_registry"].get(partner_id, {}).get("name", "None Assigned") if partner_id else "None Assigned"
            st.markdown(f"<div class='metric-card'><h4>🤝 Academic Sync Partner</h4><p>{partner_name}<br>Mode: `{USER_DATA.get('partner_role')}`</p></div>", unsafe_allow_html=True)

        # 🔔 LIVE NOTIFICATION TERMINAL PANEL
        st.markdown("### 🔔 Live Sync Notifications Panel")
        user_notifications = st.session_state["last_read_tracker"].get(CURRENT_USER_ID, [])
        if not user_notifications:
            st.info("📩 No new network alerts or partner activity pings logged.")
        else:
            for i, note in enumerate(reversed(user_notifications)):
                seen_status = "⭐ New" if not note.get("seen") else "✓ Read"
                st.markdown(f"> **[{note.get('time')}] ({seen_status})** {note.get('msg')}")
            if st.button("🧹 Clear & Mark All Notifications as Read"):
                for note in st.session_state["last_read_tracker"][CURRENT_USER_ID]:
                    note["seen"] = True
                save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
                st.success("Notifications updated.")
                st.rerun()

    # --- CHANNEL 2: ADVANCED PERSONAL PROGRESS TRACKER ---
    elif selected_workspace == "📊 Personal Progress Tracker":
        st.markdown("<h2>📊 High-Standard Syllabus Progress Matrix</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #888;'>Track topic completions aligned with the national NCDC guidelines.</p>", unsafe_allow_html=True)
        
        # Auto-initialize user progress dictionary data structure if missing
        if "progress" not in USER_DATA or not USER_DATA["progress"]:
            USER_DATA["progress"] = create_blank_progress_card(USER_DATA.get("subjects", []))
            st.session_state["users_registry"][CURRENT_USER_ID] = USER_DATA
            save_cache_to_disk("db_users.json", st.session_state["users_registry"])

        user_progress = USER_DATA["progress"]
        
        for sub in USER_DATA.get("subjects", []):
            if sub not in NCDC_CURRICULUM_MAP:
                continue
            with st.expander(f"📚 {sub} Complete Syllabus Matrix Mapping"):
                topics = NCDC_CURRICULUM_MAP[sub]
                
                # Render tracking status toggles per topic block
                for topic in topics:
                    # Defensive setup to prevent internal index crashes
                    if topic not in user_progress.get(sub, {}):
                        if sub not in user_progress:
                            user_progress[sub] = {}
                        user_progress[sub][topic] = {"status": "Not Started", "score": 0}
                    
                    current_topic_data = user_progress[sub][topic]
                    
                    t_col1, t_col2, t_col3 = st.columns([2, 1, 1])
                    with t_col1:
                        st.markdown(f"**{topic}**")
                    with t_col2:
                        status_options = ["Not Started", "In Progress", "Fully Revised & Mastered"]
                        saved_idx = status_options.index(current_topic_data.get("status", "Not Started")) if current_topic_data.get("status") in status_options else 0
                        new_status = st.selectbox(f"Status##{sub}##{topic}", status_options, index=saved_idx, label_visibility="collapsed")
                    with t_col3:
                        new_score = st.number_input(f"Score##{sub}##{topic}", min_value=0, max_value=100, value=int(current_topic_data.get("score", 0)), step=5, label_visibility="collapsed")
                    
                    # Live sync mutations back to database structures
                    user_progress[sub][topic] = {"status": new_status, "score": new_score}
                
                if st.button(f"💾 Save {sub} Progress Metric Logs"):
                    st.session_state["users_registry"][CURRENT_USER_ID]["progress"] = user_progress
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success(f"✓ {sub} parameters successfully backed up to cloud array.")

    # --- CHANNEL 3: EXAM REVISION CENTER & HIGH-PRECISION MOCK VAULT ---
    elif selected_workspace == "📝 Revision Center & Mock Vault":
        st.markdown("<h2>📝 Precision Mock Engine & Resource Vault</h2>", unsafe_allow_html=True)
        
        tab_notes, tab_exam_engine = st.tabs(["📂 Shared Document Center", "⏱️ High-Precision Mock Exam Simulation Engine"])
        
        with tab_notes:
            st.markdown("### 📋 Uploaded Academic Bulletins & PDFs")
            for doc in st.session_state.get("revision_notes_db", []):
                st.markdown(f"""
                <div class='notes-box'>
                    <h4>📌 Subject: {doc.get('Subject')} | {doc.get('Title')}</h4>
                    <p>{doc.get('Content')}</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            st.markdown("### 📤 Contribute Study Bulletin Document Notes")
            with st.form("Document Upload Form"):
                doc_title = st.text_input("Document / Note Title")
                doc_sub = st.selectbox("Related Field Subject", USER_DATA.get("subjects", ["Mathematics"]))
                doc_content = st.text_area("Summary Content Body or Resource Link Coordinates")
                if st.form_submit_button("PUBLISH TO RESOURCE VAULT"):
                    if doc_title and doc_content:
                        st.session_state["revision_notes_db"].append({
                            "Title": doc_title, "Subject": doc_sub, "Content": doc_content
                        })
                        st.success("Document added successfully to system bank.")
                        st.rerun()

        with tab_exam_engine:
            st.markdown("### ⏱️ Live Microsecond Metric Exam Terminal")
            
            # Universal fallback sample sheet data in case cloud source returns empty
            fallback_quiz_data = pd.DataFrame([
                {"Question": "Factorize completely the cubic expression: $x^3 - 6x^2 + 11x - 6 = 0$. Provide roots in order.", "OptionA": "1, 2, 3", "OptionB": "-1, -2, -3", "OptionC": "0, 1, 5", "OptionD": "2, 4, 6", "Answer": "A", "Solution": "By inspection, x=1 is a root. Long division yields (x-1)(x^2-5x+6)=0, hence roots are 1, 2, 3."},
                {"Question": "A particle moves along a straight trajectory such that $s = t^3 - 3t^2 + 2$. Calculate velocity at time $t=3$ seconds.", "OptionA": "5 m/s", "OptionB": "9 m/s", "OptionC": "12 m/s", "OptionD": "15 m/s", "Answer": "B", "Solution": "Velocity v = ds/dt = 3t^2 - 6t. Substituting t=3 values gives: 3(9) - 6(3) = 27 - 18 = 9 m/s."}
            ])
            
            # Attempt to download worksheet data from external Google Sheets database live
            quiz_df = read_public_sheet("QuizBank")
            if quiz_df is None or quiz_df.empty:
                quiz_df = fallback_quiz_data
                st.info("🔗 Syncing with System-Level Failback Examination Vault Arrays.")
            else:
                st.success("✅ Connected Live to Google Sheets Academic Database Network.")
                
            # Initialize unique exam runtime states to prevent interface refreshing from resetting time counters
            if "exam_running" not in st.session_state: st.session_state["exam_running"] = False
            if "start_epoch" not in st.session_state: st.session_state["start_epoch"] = 0.0
            if "selected_answers" not in st.session_state: st.session_state["selected_answers"] = {}

            if not st.session_state["exam_running"]:
                st.markdown("<p style='color: #bbb;'>Ensure you are fully prepared before starting. The system records evaluation precision down to microseconds.</p>", unsafe_allow_html=True)
                if st.button("🚀 INITIATE PRECISION EXAM TERMINAL"):
                    st.session_state["exam_running"] = True
                    st.session_state["start_epoch"] = time.time()
                    st.session_state["selected_answers"] = {}
                    st.rerun()
            else:
                current_elapsed = time.time() - st.session_state["start_epoch"]
                st.markdown(f"""
                <div class='timer-container'>
                    <span style='color: #888; font-size:12px;'>ELAPSED ASSESSMENT RUNTIME</span><br>
                    <span style='font-size: 24px; font-weight: bold; color: #ff3333;'>{current_elapsed:.4f} Seconds</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Render interactive questionnaire elements
                with st.form("Exam Questionnaire Blueprint"):
                    user_selections = {}
                    for idx, row in quiz_df.iterrows():
                        st.markdown(f"#### Q{idx+1}: {row['Question']}")
                        opts = [f"A) {row['OptionA']}", f"B) {row['OptionB']}", f"C) {row['OptionC']}", f"D) {row['OptionD']}"]
                        user_selections[idx] = st.radio(f"Select Answer Choice for Q{idx+1}:", opts, key=f"q_radio_{idx}")
                    
                    submit_exam_btn = st.form_submit_button("🔒 LOCK ANSWERS AND SUBMIT FOR EVALUATION")
                    
                    if submit_exam_btn:
                        end_epoch = time.time()
                        total_time_taken = end_epoch - st.session_state["start_epoch"]
                        st.session_state["exam_running"] = False
                        
                        # Grade processing matrix logic calculations
                        correct_tallies = 0
                        total_questions = len(quiz_df)
                        report_breakdown = []
                        
                        for idx, row in quiz_df.iterrows():
                            chosen_letter = user_selections[idx].split(")")[0].strip()
                            correct_letter = str(row['Answer']).strip()
                            is_correct = (chosen_letter == correct_letter)
                            
                            if is_correct:
                                correct_tallies += 1
                                
                            report_breakdown.append({
                                "Question Number": f"Question {idx+1}",
                                "Your Choice": chosen_letter,
                                "Correct Key": correct_letter,
                                "Evaluation Status": "PASS" if is_correct else "FAIL",
                                "Detailed System Solution Explanations": row['Solution']
                            })
                            
                        score_percentage = (correct_tallies / total_questions) * 100
                        
                        # Apply custom Academic Grading Framework standards
                        if score_percentage >= 80: grade_symbol, comment = "D1 (Distinction Superior)", "Excellent execution! Concept mastery verified."
                        elif score_percentage >= 75: grade_symbol, comment = "D2 (Distinction)", "High precision registered. Strong grasp."
                        elif score_percentage >= 70: grade_symbol, comment = "C3 (Credit)", "Solid execution. Review minor analytical items."
                        elif score_percentage >= 65: grade_symbol, comment = "C4 (Credit)", "Competent performance. Room for speed optimization."
                        elif score_percentage >= 60: grade_symbol, comment = "C5 (Credit)", "Pass mark secured. Focus heavily on core formulas."
                        elif score_percentage >= 50: grade_symbol, comment = "P7 (Pass)", "Marginal performance. Intensive review recommended."
                        else: grade_symbol, comment = "F9 (Fail)", "Sub-optimal score. Revise foundational modules immediately."
                        
                        # Display interactive visual evaluation certificates
                        st.markdown("### 🏆 Official Performance Evaluation Brief")
                        st.metric(label="Calculated Performance Score Matrix", value=f"{score_percentage:.2f}%", delta=grade_symbol)
                        st.markdown(f"**⏱️ Precise Evaluation Runtime Interval:** `{total_time_taken:.6f} Seconds`")
                        st.info(f"💡 **Network Assessor Commentary:** {comment}")
                        
                        # Display clear dynamic answer verification sheets
                        report_df = pd.DataFrame(report_breakdown)
                        st.dataframe(report_df)
                        
                        # Generate file download payload feature mechanics
                        csv_payload = report_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 DOWNLOAD PERFORMANCE EXAM SHEET (CSV)",
                            data=csv_payload,
                            file_name=f"Exam_Report_{CURRENT_USER_ID}_{int(time.time())}.csv",
                            mime="text/csv"
                        )
                        st.form_submit_button("RE-ENTER PRACTICE HUB")
                        # --- CHANNEL 4: WHATSAPP LOUNGE INDUSTRIAL DISCUSSION ENGINE ---
    elif selected_workspace == "💬 WhatsApp Lounge Chat":
        st.markdown("<h2>💬 WhatsApp Lounge Communication Engine</h2>", unsafe_allow_html=True)
        
        chat_mode = st.radio("Select Communication Channel Matrix:", ["🌍 Global Network Mainframe", "🔒 Private Peer-to-Peer Link"], horizontal=True)
        
        # Helper component to display realistic WhatsApp formatted bubbles
        def render_whatsapp_bubble(msg_obj, active_user_name):
            sender = msg_obj.get("sender", "System")
            text = msg_obj.get("text", "")
            timestamp = msg_obj.get("timestamp", "00:00 AM")
            media = msg_obj.get("media_link", "")
            audio = msg_obj.get("audio_duration", "")
            
            is_me = (sender == active_user_name)
            bubble_alignment_class = "chat-right" if is_me else "chat-left"
            
            media_html = f"<div class='chat-media-box'>📁 Attached File Coordinate:<br><a href='{media}' target='_blank' style='color:#53bdeb;'>{media}</a></div>" if media else ""
            audio_html = f"<div class='audio-note-box'>🎵 <b>Voice Note Simulation</b> ({audio}) ───🔊</div>" if audio else ""
            ticks_html = " <span class='whatsapp-ticks'>✓✓</span>" if is_me else ""
            
            st.markdown(f"""
            <div class='chat-bubble {bubble_alignment_class}'>
                <span style='font-size: 11px; font-weight: bold; color: #ff3333; display: block;'>{sender}</span>
                {text}
                {media_html}
                {audio_html}
                <span class='chat-timestamp'>{timestamp}{ticks_html}</span>
            </div>
            """, unsafe_allow_html=True)

        if chat_mode == "🌍 Global Network Mainframe":
            st.markdown("### 🌍 Main Discussion Frame")
            
            # WhatsApp Layout Scroll Wrapper Box
            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            for msg in st.session_state["general_chat"]:
                render_whatsapp_bubble(msg, USER_DATA.get("name"))
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Interactive Input Terminal Form
            with st.form("Global Chat Transmitter", clear_on_submit=True):
                msg_txt = st.text_input("Type Message...", placeholder="Share insights or calculations...")
                
                col_m1, col_m2 = st.columns(2)
                with col_m1: attachment_url = st.text_input("Attach Reference URL Link (Optional)")
                with col_m2: simulated_audio_length = st.text_input("Simulate Voice Note Duration (e.g. 0:42) (Optional)")
                
                if st.form_submit_button("SEND MESSAGE"):
                    if msg_txt or attachment_url or simulated_audio_length:
                        new_msg = {
                            "sender": USER_DATA.get("name"),
                            "text": msg_txt,
                            "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                            "media_link": attachment_url,
                            "audio_duration": simulated_audio_length
                        }
                        st.session_state["general_chat"].append(new_msg)
                        save_cache_to_disk("db_genchat.json", st.session_state["general_chat"])
                        st.rerun()
                        
        elif chat_mode == "🔒 Private Peer-to-Peer Link":
            partner_id = USER_DATA.get("partner", "")
            if not partner_id:
                st.warning("⚠️ No active synchronization partner linked to your profile node. Pair up in the Partner Connection Hub.")
            else:
                partner_profile = st.session_state["users_registry"].get(partner_id, {})
                st.markdown(f"### 🔒 Secure Tunnel Link: `{USER_DATA.get('name')}` ⇄ `{partner_profile.get('name', 'Unknown')}`")
                
                # Filter private message logs matching specifically this paired link ID
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
                for msg in st.session_state["private_chats"]:
                    msg_sender = msg.get("sender")
                    # Display message only if sent between the active user and their designated partner
                    if msg_sender in [USER_DATA.get("name"), partner_profile.get("name")]:
                        render_whatsapp_bubble(msg, USER_DATA.get("name"))
                st.markdown("</div>", unsafe_allow_html=True)
                
                with st.form("Private Tunnel Transmitter", clear_on_submit=True):
                    p_text = st.text_input("Type Private Message...")
                    if st.form_submit_button("TRANSMIT PRIVATE DATA"):
                        if p_text:
                            new_p_msg = {
                                "sender": USER_DATA.get("name"),
                                "text": p_text,
                                "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                                "media_link": "", "audio_duration": ""
                            }
                            st.session_state["private_chats"].append(new_p_msg)
                            save_cache_to_disk("db_p2pchat.json", st.session_state["private_chats"])
                            push_system_notification(partner_id, f"📥 New encrypted message received from your partner {USER_DATA.get('name')}.")
                            st.rerun()

    # --- CHANNEL 5: PARTNER CONNECTION HUB ---
    elif selected_workspace == "🤝 Partner Connection Hub":
        st.markdown("<h2>🤝 Academic Collaboration & Partner Pairing Hub</h2>", unsafe_allow_html=True)
        
        # Display Current Pairing Configuration Status Card
        p_id = USER_DATA.get("partner", "")
        if p_id:
            p_node = st.session_state["users_registry"].get(p_id, {})
            st.success(f"🔗 Secure Link Active! Paired Profile Name: {p_node.get('name')} | Mode: {USER_DATA.get('partner_role')}")
            if st.button("💔 SEVER CONNECTION LINK"):
                # Cleanly unpair both accounts simultaneously in database
                st.session_state["users_registry"][CURRENT_USER_ID]["partner"] = ""
                if p_id in st.session_state["users_registry"]:
                    st.session_state["users_registry"][p_id]["partner"] = ""
                save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                st.success("Connection severed cleanly. System parameters returned to standalone configuration.")
                st.rerun()
        else:
            st.info("📡 Status: Standalone Mode. Select an unlinked peer below to spin up a collaborative sync link.")
            
            # Generate options of other available registered students across the platform
            available_candidates = {uid: node.get("name") for uid, node in st.session_state["users_registry"].items() if uid != CURRENT_USER_ID and not node.get("partner")}
            
            if not available_candidates:
                st.warning("No unlinked candidates currently available for connection matching on the network.")
            else:
                target_peer_uid = st.selectbox("Select Candidate Peer Link Target:", list(available_candidates.keys()), format_func=lambda x: available_candidates[x])
                chosen_role_mode = st.selectbox("Assign Collaboration Framework Mode:", ["Mutual Study Partners", "Mentor-Mentee Framework", "Assessor-Candidate Pairing"])
                
                if st.button("🔗 INITIALIZE SECURE SYNC LINK"):
                    st.session_state["users_registry"][CURRENT_USER_ID]["partner"] = target_peer_uid
                    st.session_state["users_registry"][CURRENT_USER_ID]["partner_role"] = chosen_role_mode
                    
                    st.session_state["users_registry"][target_peer_uid]["partner"] = CURRENT_USER_ID
                    st.session_state["users_registry"][target_peer_uid]["partner_role"] = chosen_role_mode
                    
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    push_system_notification(target_peer_uid, f"✨ Connection Established! You have been linked with {USER_DATA.get('name')} as {chosen_role_mode}.")
                    st.success("Connection established successfully.")
                    st.rerun()

    # --- CHANNEL 6: SUPER ADMIN PRIVILEGED MANAGEMENT OPERATIONS ---
    elif selected_workspace == "⚙️ Super Admin Operations" and USER_DATA.get("role") in ["ADMIN", "SUPER_ADMIN"]:
        st.markdown("<h2>⚙️ Network Command Center & Super Privileges</h2>", unsafe_allow_html=True)
        
        adm_tab1, adm_tab2, adm_tab3 = st.tabs(["🔒 Candidate Registry Control", "📢 Broadcast Operations", "🛠️ Engine Settings"])
        
        with adm_tab1:
            st.markdown("### 📋 System Accounts Registry Matrix")
            
            # Render complete directory control panels for every registered profile account
            for uid, node in list(st.session_state["users_registry"].items()):
                st.markdown(f"""
                <div class='directory-card'>
                    <b>ID:</b> <code>{uid}</code> | <b>Name:</b> {node.get('name')} | <b>Username:</b> {node.get('username')}<br>
                    <b>Status Flag:</b> <code>{node.get('status')}</code> | <b>Assigned Security Role:</b> <code>{node.get('role')}</code><br>
                    <b>Active Warning Notice:</b> <span style='color:#ff9999;'>{node.get('warning_msg', 'None Listed')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Single-user override action controller row
                c_a1, c_a2, c_a3, c_a4 = st.columns(4)
                with c_a1:
                    if st.button("🟢 APPROVE / ACTIVATE", key=f"app_{uid}"):
                        st.session_state["users_registry"][uid]["status"] = "Approved"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        push_system_notification(uid, "🟢 Your account registration application has been fully approved by the network administrator.")
                        st.success(f"Account {uid} set to Approved.")
                        st.rerun()
                with c_a2:
                    if st.button("🟡 SUSPEND ACCESS", key=f"susp_{uid}"):
                        st.session_state["users_registry"][uid]["status"] = "Suspended"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.warning(f"Account {uid} suspended.")
                        st.rerun()
                with c_a3:
                    warn_input = st.text_input("Enter Warning Alert Text", key=f"txt_{uid}", placeholder="Issue system citation...")
                    if st.button("⚠️ DISPATCH ALERT", key=f"warn_{uid}"):
                        st.session_state["users_registry"][uid]["warning_msg"] = warn_input
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        push_system_notification(uid, f"⚠️ Official Admin Warning Issued: {warn_input}")
                        st.success("Warning pinned to user node.")
                        st.rerun()
                with c_a4:
                    if st.button("🔴 PURGE ACCOUNT", key=f"del_{uid}"):
                        if uid in ["0000", "6601"]:
                            st.error("Protected Core Identity Node. Cannot delete system origin files.")
                        else:
                            del st.session_state["users_registry"][uid]
                            save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                            st.error(f"Profile {uid} wiped cleanly from system database registries.")
                            st.rerun()
                st.markdown("<hr style='border: 1px solid #222; margin:10px 0;'>", unsafe_allow_html=True)

        with adm_tab2:
            st.markdown("### 📢 Public System Announcements Panel")
            new_alert = st.text_input("Draft Global Ticker Broadcast System Message")
            if st.button("🚀 TRANSMIT SYSTEM BROADCAST"):
                if new_alert:
                    st.session_state["global_alerts"].insert(0, new_alert)
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.success("Broadcast broadcasted to all terminals live.")
                    st.rerun()
            st.markdown("#### Active Announcement History Threads")
            for idx, item in enumerate(st.session_state["global_alerts"]):
                st.markdown(f"- {item}")
                if st.button(f"🗑️ Delete Alert ID {idx}", key=f"del_al_{idx}"):
                    st.session_state["global_alerts"].pop(idx)
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.rerun()

        with adm_tab3:
            st.markdown("### 🛠️ Core Administrative Asset Refactoring")
            
            # Dynamic Admin Photo Overrider Configuration Option
            admin_photo_url = st.text_input("Update Super Admin Photo URL Coordinate Asset:", value=st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE))
            if st.button("💾 SAVE ADMIN AVATAR IMAGE"):
                st.session_state["custom_admin_photo"] = admin_photo_url
                save_cache_to_disk("db_admin_photo.json", admin_photo_url)
                st.success("Admin photo asset configurations updated successfully.")
                st.rerun()
                
            st.markdown("---")
            st.markdown("#### 🔑 Access Registration Keys Authority Matrix")
            st.write(st.session_state["generated_registration_codes"])
            new_code_string = st.text_input("Generate New Valid Network Registration Key Code")
            if st.button("➕ COMPARTMENTALIZE KEY CODE"):
                if new_code_string and new_code_string not in st.session_state["generated_registration_codes"]:
                    st.session_state["generated_registration_codes"].append(new_code_string)
                    save_cache_to_disk("db_regcodes.json", st.session_state["generated_registration_codes"])
                    st.success(f"Access code key validation token `{new_code_string}` appended successfully.")
                    st.rerun()

    # =========================================================================
    # 8. SYSTEM INTEGRITY BRANDING MATRIX FOOTER
    # =========================================================================
    st.markdown(f"""
    <div class='sudaisi-branding-footer'>
        <p style='color: #444; font-size: 11px; margin: 0;'>🛡️ Academic Shield Network Infrastructure Engine v4.26 • Core Engineering Configured by Sudaisi Setra</p>
    </div>
    """, unsafe_allow_html=True)
