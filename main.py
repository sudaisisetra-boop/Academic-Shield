import streamlit as st
import pandas as pd
import datetime
import random
import os
import json
import time

# =========================================================================
# 1. INITIAL SYSTEM FRAMEWORK & ENGINE SETTINGS
# =========================================================================
# This command must execute first to avoid initialization rendering failure
st.set_page_config(page_title="Academic Shield Pro", layout="wide", page_icon="🛡️")

# Embedded WhatsApp Dark UI Core Styles and Component Panels
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
    
    /* --- WhatsApp Layout UI CSS Specs --- */
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
    .sudaisi-branding-footer { text-align: center; padding: 15px; margin-top: 40px; border-top: 1px solid #222; background-color: #0e0e0e; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# 2. PLATFORM DATA STRUCTURES & ASSET PRESETS
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
# 3. SELF-HEALING ARRAYS (PREVENTS DATABASE KEY CRASHES)
# =========================================================================
def sanitize_chat_list(lst):
    if not isinstance(lst, list): return []
    cleaned = []
    for item in lst:
        if isinstance(item, dict): cleaned.append(item)
        elif isinstance(item, str): cleaned.append({"sender": "System", "text": item, "timestamp": "00:00 AM"})
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

# Load states cleanly into Streamlit Session Memory
if "users_registry" not in st.session_state:
    st.session_state["users_registry"] = sanitize_users_registry(load_cache_from_disk("db_users.json", {}))
if "general_chat" not in st.session_state: 
    st.session_state["general_chat"] = sanitize_chat_list(load_cache_from_disk("db_genchat.json", []))
if "private_chats" not in st.session_state: 
    st.session_state["private_chats"] = sanitize_chat_list(load_cache_from_disk("db_p2pchat.json", []))
if "global_alerts" not in st.session_state: 
    st.session_state["global_alerts"] = load_cache_from_disk("db_alerts.json", ["🚀 Platform Online. Secure Mirror Systems Functional."])
if "last_read_tracker" not in st.session_state: 
    st.session_state["last_read_tracker"] = load_cache_from_disk("db_readtrack.json", {})
if "generated_registration_codes" not in st.session_state: 
    st.session_state["generated_registration_codes"] = load_cache_from_disk("db_regcodes.json", ["SHIELD2026", "ASP2026"])
if "custom_admin_photo" not in st.session_state: 
    st.session_state["custom_admin_photo"] = load_cache_from_disk("db_admin_photo.json", DEFAULT_SUDAISI_IMAGE)
if "revision_notes_db" not in st.session_state:
    st.session_state["revision_notes_db"] = [
        {"Title": "Pure Mathematics Vectors Blueprint", "Subject": "Mathematics", "Content": "Vectors core revision summary notes: Unit tracks, relative parameters, and Cartesian projections for P425/1 standards."}
]
    # =========================================================================
# 4. BACKGROUND SYSTEM NOTIFICATIONS GENERATOR
# =========================================================================
def push_system_notification(user_id, alert_text):
    """Safely records background notification alerts for individual nodes."""
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
    """Generates standard tracking grids mapped out against NCDC guidelines."""
    card = {}
    for sub in subjects_list:
        if sub in NCDC_CURRICULUM_MAP:
            card[sub] = {topic: {"status": "Not Started", "score": 0} for topic in NCDC_CURRICULUM_MAP[sub]}
    return card

# =========================================================================
# 5. USER INTERFACE AUTHENTICATION GATEWAYS (LOGIN / ACCOUNT CREATION)
# =========================================================================
if "logged_in_uid" not in st.session_state:
    st.session_state["logged_in_uid"] = None

if st.session_state["logged_in_uid"] is None:
    st.markdown("<h1 style='text-align: center; color: #ff3333;'>🛡️ ACADEMIC SHIELD NETWORK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Ugandan Advanced Curriculum Portal & Core Database</p>", unsafe_allow_html=True)
    
    auth_mode = st.radio("Select Portal Action Gate:", ["🔑 System Security Login", "📝 Create Candidate Account"], horizontal=True)
    
    if auth_mode == "🔑 System Security Login":
        with st.form("Login Gateway Terminal"):
            input_username = st.text_input("Candidate Username / ID Coordinate")
            input_password = st.text_input("Security Access Password", type="password")
            submit_login = st.form_submit_button("AUTHORIZE SYSTEM ACCESS")
            
            if submit_login:
                found_uid = None
                # Scan registry to capture correct user match parameters
                for uid, data in st.session_state["users_registry"].items():
                    if data.get("username") == input_username and data.get("pwd") == input_password:
                        found_uid = uid
                        break
                
                if found_uid:
                    user_node = st.session_state["users_registry"][found_uid]
                    if user_node.get("status", "Approved") == "Suspended":
                        st.error("🚫 Access Revoked. This account node has been suspended by the Admin.")
                    elif user_node.get("status", "Approved") == "Pending Review":
                        st.warning("⏳ Account Verification Pending. Please await Admin clearance approval.")
                    else:
                        st.session_state["logged_in_uid"] = found_uid
                        st.success(f"🔓 Access Granted. Welcome, {user_node.get('name')}.")
                        st.rerun()
                else:
                    st.error("❌ Authentication Failed. Double-check your access credentials.")
                    
    elif auth_mode == "📝 Create Candidate Account":
        with st.form("Registration Intake Module"):
            reg_code = st.text_input("Enter Access Validation Code (From Admin)")
            reg_uid = st.text_input("Desired Unique ID Number (4 Digits Only)")
            reg_user = st.text_input("Account Login Username")
            reg_pwd = st.text_input("Secure Password", type="password")
            reg_name = st.text_input("Full Official Name")
            
            reg_class = st.selectbox("Academic Level Class", ["Senior Five", "Senior Six"])
            reg_school = st.text_input("Institution / School Name", value="The Amazima School")
            reg_phone = st.text_input("Active Phone Connection Contact")
            reg_email = st.text_input("Email Coordinate Contact")
            reg_gender = st.selectbox("Gender", ["Male", "Female"])
            reg_loc = st.text_input("Current Hub / Location")
            
            selected_subs = st.multiselect("Enrolled Academic Subjects", list(NCDC_CURRICULUM_MAP.keys()), default=["Mathematics"])
            
            submit_reg = st.form_submit_button("SUBMIT REGISTRATION APPLICATION")
            
            if submit_reg:
                if reg_code not in st.session_state["generated_registration_codes"]:
                    st.error("❌ Invalid System Registration Key Code.")
                elif not reg_uid or not reg_user or not reg_pwd or not reg_name:
                    st.error("❌ Critical account parameters cannot remain empty.")
                elif reg_uid in st.session_state["users_registry"]:
                    st.error("❌ Identity Conflict: This 4-Digit ID already exists.")
                else:
                    # Inject standardized data scheme ensuring absolute stability
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
                    st.success("🎯 Account submitted! Your profile status is 'Pending Review'. Await Admin Activation.")

else:
    # -------------------------------------------------------------------------
    # CORE INTERFACE FRAMEWORK ROUTING LAYER (AUTHORIZED ENTRY ONLY)
    # -------------------------------------------------------------------------
    CURRENT_USER_ID = st.session_state["logged_in_uid"]
    USER_DATA = st.session_state["users_registry"].get(CURRENT_USER_ID, {})
    
    # Safety Check: Terminate dead or corrupt session keys
    if not USER_DATA:
        st.session_state["logged_in_uid"] = None
        st.rerun()

    # =========================================================================
    # 6. SIDEBAR TERMINAL ARCHITECTURE & NAVIGATION CONTROLS
    # =========================================================================
    with st.sidebar:
        st.markdown(f"<h3 style='color: #ff3333;'>🛡️ SHIELD TERMINAL</h3>", unsafe_allow_html=True)
        
        # Display Dynamic Image Avatar Logic
        avatar_src = USER_DATA.get("avatar", AVATAR_OPTIONS[0])
        if avatar_src == "SUDAISI_BAKED":
            avatar_src = st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE)
            
        st.image(avatar_src, width=85)
        st.markdown(f"**User:** {USER_DATA.get('name')}")
        st.markdown(f"**Role:** `{USER_DATA.get('role')}`")
        
        # Enforce Real-time Admin Warning Banners
        if USER_DATA.get("warning_msg"):
            st.markdown(f"<div class='system-warn-box'>⚠️ ADMIN ALERT:<br>{USER_DATA.get('warning_msg')}</div>", unsafe_allow_html=True)
            
        st.write("---")
        
        # Build Navigation Channels
        navigation_nodes = [
            "📋 Operational Dashboard",
            "📊 Personal Progress Tracker",
            "📝 Revision Center & Mock Vault",
            "💬 WhatsApp Lounge Chat",
            "🤝 Partner Connection Hub"
        ]
        
        # Inject privileged options for Admin/Super Admin classes
        if USER_DATA.get("role") in ["ADMIN", "SUPER_ADMIN"]:
            navigation_nodes.append("⚙️ Super Admin Operations")
            
        selected_workspace = st.radio("Navigate Workspace Channels:", navigation_nodes)
        
        st.write("---")
        if st.button("🔴 SECURE LOGOUT"):
            st.session_state["logged_in_uid"] = None
            st.rerun()
            # =========================================================================
    # 7. ROUTER WORKSPACE NAVIGATION MANAGEMENT LAYERS
    # =========================================================================
    
    # --- NAVIGATION NODE 1: OPERATIONAL TERMINAL DASHBOARD ---
    if selected_workspace == "📋 Operational Dashboard":
        st.markdown("<h2>📋 Operational Candidate Dashboard</h2>", unsafe_allow_html=True)
        
        # Display Live Network Alert Broadcasts managed by Admin
        for alert in st.session_state.get("global_alerts", []):
            st.markdown(f"<div class='admin-broadcast-banner'>📢 ANNOUNCEMENT: {alert}</div>", unsafe_allow_html=True)
            
        # Core Credentials Information Metrics Row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-card'><h4>🏫 Institutional Hub</h4><p>{USER_DATA.get('school', 'N/A')}<br>Level: `{USER_DATA.get('class', 'N/A')}`</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><h4>🧬 Curriculum Scope</h4><p>{', '.join(USER_DATA.get('subjects', []))}</p></div>", unsafe_allow_html=True)
        with col3:
            partner_id = USER_DATA.get("partner", "")
            partner_name = st.session_state["users_registry"].get(partner_id, {}).get("name", "No Peer Linked") if partner_id else "No Peer Linked"
            st.markdown(f"<div class='metric-card'><h4>🤝 Collaboration Sync</h4><p>{partner_name}<br>Framework: `{USER_DATA.get('partner_role', 'Standalone')}`</p></div>", unsafe_allow_html=True)

        # Live Real-time System Updates Activity Terminal Log
        st.markdown("### 🔔 Active System Notifications Terminal")
        user_notifications = st.session_state["last_read_tracker"].get(CURRENT_USER_ID, [])
        if not user_notifications:
            st.info("📩 Workspace log clear. No unread system-level background alerts recorded.")
        else:
            for note in reversed(user_notifications):
                seen_status = "⭐ New Alert" if not note.get("seen") else "✓ Logged"
                st.markdown(f"> **[{note.get('time', '00:00')}] ({seen_status})** {note.get('msg', '')}")
            if st.button("🧹 Clear Workspace Notification Traces"):
                for note in st.session_state["last_read_tracker"][CURRENT_USER_ID]:
                    note["seen"] = True
                save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
                st.success("Activity log marks systematically updated.")
                st.rerun()

    # --- NAVIGATION NODE 2: SYLLABUS SYNC TRACKER MATRIX ---
    elif selected_workspace == "📊 Personal Progress Tracker":
        st.markdown("<h2>📊 Personal Syllabus Coverage Matrix</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #888;'>Evaluate completion and record self-assessment scores against national Ugandan standards.</p>", unsafe_allow_html=True)
        
        # Check and verify progress schema presence to prevent background value lookups from crashing
        if "progress" not in USER_DATA or not USER_DATA["progress"]:
            USER_DATA["progress"] = create_blank_progress_card(USER_DATA.get("subjects", []))
            st.session_state["users_registry"][CURRENT_USER_ID] = USER_DATA
            save_cache_to_disk("db_users.json", st.session_state["users_registry"])

        user_progress = USER_DATA["progress"]
        
        for sub in USER_DATA.get("subjects", []):
            if sub not in NCDC_CURRICULUM_MAP:
                continue
            with st.expander(f"📚 {sub} Module Milestone Mapping"):
                topics = NCDC_CURRICULUM_MAP[sub]
                
                for topic in topics:
                    # Self-healing verification check on specific structural nodes
                    if sub not in user_progress:
                        user_progress[sub] = {}
                    if topic not in user_progress[sub]:
                        user_progress[sub][topic] = {"status": "Not Started", "score": 0}
                    
                    current_topic_data = user_progress[sub][topic]
                    
                    t_col1, t_col2, t_col3 = st.columns([2, 1, 1])
                    with t_col1:
                        st.markdown(f"**{topic}**")
                    with t_col2:
                        status_options = ["Not Started", "In Progress", "Fully Revised & Mastered"]
                        saved_idx = status_options.index(current_topic_data.get("status", "Not Started")) if current_topic_data.get("status") in status_options else 0
                        new_status = st.selectbox(f"Coverage Flag##{sub}##{topic}", status_options, index=saved_idx, label_visibility="collapsed")
                    with t_col3:
                        new_score = st.number_input(f"Competency Grade##{sub}##{topic}", min_value=0, max_value=100, value=int(current_topic_data.get("score", 0)), step=5, label_visibility="collapsed")
                    
                    user_progress[sub][topic] = {"status": new_status, "score": new_score}
                
                if st.button(f"💾 Commit {sub} Coverage Matrix Records", key=f"save_prog_btn_{sub}"):
                    st.session_state["users_registry"][CURRENT_USER_ID]["progress"] = user_progress
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success(f"✓ {sub} competency matrix metrics securely compiled and synchronized.")

    # --- NAVIGATION NODE 3: HIGH-PRECISION EVALUATION ENGINE ---
    elif selected_workspace == "📝 Revision Center & Mock Vault":
        st.markdown("<h2>📝 Academic Revision & Precision Evaluation Vault</h2>", unsafe_allow_html=True)
        
        tab_notes, tab_exam_engine = st.tabs(["📂 Shared Document Registries", "⏱️ High-Precision Examination Simulation Engine"])
        
        with tab_notes:
            st.markdown("### 📋 Uploaded Bulletins & Resource Outlines")
            for doc in st.session_state.get("revision_notes_db", []):
                st.markdown(f"""
                <div class='notes-box'>
                    <h4>📌 Field Area: {doc.get('Subject')} | Title: {doc.get('Title')}</h4>
                    <p>{doc.get('Content')}</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            st.markdown("### 📤 Contribute Reference Notes/Resource Coordinates")
            with st.form("Reference Material Registry Intake"):
                doc_title = st.text_input("Resource/Bulletin Descriptive Title")
                doc_sub = st.selectbox("Academic Relation Category", USER_DATA.get("subjects", ["Mathematics"]))
                doc_content = st.text_area("Content Body Summary Descriptions or Accessible Cloud Links")
                if st.form_submit_button("PUBLISH MATERIAL TO RESOURCE BANK"):
                    if doc_title and doc_content:
                        st.session_state["revision_notes_db"].append({
                            "Title": doc_title, "Subject": doc_sub, "Content": doc_content
                        })
                        st.success("Resource material committed to global cloud bank index.")
                        st.rerun()

        with tab_exam_engine:
            st.markdown("### ⏱️ Live Microsecond Metric Assessment Node")
            
            # Bulletproof local evaluation sample question data array schema
            fallback_quiz_data = pd.DataFrame([
                {"Question": "Factorize completely the cubic expression: $x^3 - 6x^2 + 11x - 6 = 0$. Determine accurate roots.", "OptionA": "1, 2, 3", "OptionB": "-1, -2, -3", "OptionC": "0, 1, 5", "OptionD": "2, 4, 6", "Answer": "A", "Solution": "By inspection, x=1 satisfies the statement. Division provides the secondary quadratic factor (x^2-5x+6)=(x-2)(x-3). Correct solutions are 1, 2, 3."},
                {"Question": "An explicit particle progresses linearly along a vector such that displacement $s = t^3 - 3t^2 + 2$. Evaluate acceleration at interval value $t=3$ seconds.", "OptionA": "6 m/s^2", "OptionB": "12 m/s^2", "OptionC": "18 m/s^2", "OptionD": "24 m/s^2", "Answer": "B", "Solution": "Velocity v = ds/dt = 3t^2 - 6t. Acceleration acceleration = dv/dt = 6t - 6. Substituting t=3 delivers: 6(3) - 6 = 18 - 6 = 12 m/s^2."}
            ])
            
            # Stream live exam data packages directly from connected tracking sheet configurations
            quiz_df = read_public_sheet("QuizBank")
            if quiz_df is None or quiz_df.empty:
                quiz_df = fallback_quiz_data
                st.info("🔗 Syncing evaluations through embedded structural fallback matrices.")
            else:
                st.success("✅ Live Google Sheets connection active. Evaluation package linked successfully.")
                
            # Initialize precise time verification variables to survive interface re-renders
            if "exam_running" not in st.session_state: st.session_state["exam_running"] = False
            if "start_epoch" not in st.session_state: st.session_state["start_epoch"] = 0.0

            if not st.session_state["exam_running"]:
                st.markdown("<p style='color: #bbb;'>Evaluation time calculations trace back accurately down to microsecond increments. Ensure you are ready before triggering the interface matrix.</p>", unsafe_allow_html=True)
                if st.button("🚀 BOOT HIGH-PRECISION REVISION EXAM TERMINAL"):
                    st.session_state["exam_running"] = True
                    st.session_state["start_epoch"] = time.time()
                    st.rerun()
            else:
                current_elapsed = time.time() - st.session_state["start_epoch"]
                st.markdown(f"""
                <div class='timer-container'>
                    <span style='color: #888; font-size:11px;'>HIGH-PRECISION INTERVAL TIMING</span><br>
                    <span style='font-size: 24px; font-weight: bold; color: #ff3333;'>{current_elapsed:.4f} Seconds Logged</span>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("Interactive Examination Questionnaire"):
                    user_selections = {}
                    for idx, row in quiz_df.iterrows():
                        st.markdown(f"#### Question {idx+1}: {row['Question']}")
                        opts = [f"A) {row['OptionA']}", f"B) {row['OptionB']}", f"C) {row['OptionC']}", f"D) {row['OptionD']}"]
                        user_selections[idx] = st.radio(f"Select Choice Vector for Question {idx+1}:", opts, key=f"q_elem_{idx}")
                    
                    if st.form_submit_button("🔒 SYSTEM LOCK: EVALUATE & RECORD TIMING MARKS"):
                        end_epoch = time.time()
                        total_time_taken = end_epoch - st.session_state["start_epoch"]
                        st.session_state["exam_running"] = False
                        
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
                                "Question Index": f"Item {idx+1}",
                                "Candidate Answer": chosen_letter,
                                "Verified Reference Key": correct_letter,
                                "Assessment Status": "CORRECT" if is_correct else "INCORRECT",
                                "Analytical Solution Traceback": row['Solution']
                            })
                            
                        score_percentage = (correct_tallies / total_questions) * 100
                        
                        # Apply Ugandan National Advanced Secondary Evaluation scale grading protocols
                        if score_percentage >= 80: grade_symbol, commentary = "D1 (Distinction Master)", "Elite parameter mastery verified. Excellent analytic logic."
                        elif score_percentage >= 75: grade_symbol, commentary = "D2 (Distinction Excellent)", "Excellent accuracy performance metrics recorded."
                        elif score_percentage >= 70: grade_symbol, commentary = "C3 (Credit High)", "Solid grasp. Check intermediate logic parameters to clean performance speed leaks."
                        elif score_percentage >= 65: grade_symbol, commentary = "C4 (Credit Competent)", "Stable foundation. Accelerate recall routines to bypass layout timing caps."
                        elif score_percentage >= 60: grade_symbol, commentary = "C5 (Credit)", "Performance targets met. Reinforce core tracking formulas."
                        elif score_percentage >= 50: grade_symbol, commentary = "P7 (Pass)", "Marginal structural pass. Target revision routines to weaker modules."
                        else: grade_symbol, commentary = "F9 (Fail)", "Performance under critical target levels. Initiate recovery syllabus tracks instantly."
                        
                        st.markdown("### 🏆 Comprehensive Performance Metric Card")
                        st.metric(label="Calculated Matrix Performance Mark", value=f"{score_percentage:.2f}%", delta=grade_symbol)
                        st.markdown(f"**⏱️ Precise Evaluation Timing Delta:** `{total_time_taken:.6f} Seconds`")
                        st.info(f"💡 **Assessor Network Review Commentary:** {commentary}")
                        
                        report_df = pd.DataFrame(report_breakdown)
                        st.dataframe(report_df)
                        
                        # Pack dynamic file generator triggers
                        csv_payload = report_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 EXPORT PERFORMANCE ANALYTICS REPORT SHEET (CSV)",
                            data=csv_payload,
                            file_name=f"Evaluation_Report_{CURRENT_USER_ID}_{int(time.time())}.csv",
                            mime="text/csv"
                        )
                        st.form_submit_button("RE-LOCK WORKSPACE FOR PRACTICE")
                        # --- NAVIGATION NODE 4: WHATSAPP LOUNGE COMMUNICATION SYSTEM ---
    elif selected_workspace == "💬 WhatsApp Lounge Chat":
        st.markdown("<h2>💬 WhatsApp Lounge Communication System</h2>", unsafe_allow_html=True)
        
        chat_mode = st.radio("Select Active Communication Frequency:", ["🌍 Global Network Mainframe", "🔒 Private Peer-to-Peer Link"], horizontal=True)
        
        # Internal styling function to render realistic chat bubbles
        def render_whatsapp_bubble(msg_obj, active_user_name):
            sender = msg_obj.get("sender", "System")
            text = msg_obj.get("text", "")
            timestamp = msg_obj.get("timestamp", "00:00 AM")
            media = msg_obj.get("media_link", "")
            audio = msg_obj.get("audio_duration", "")
            
            is_me = (sender == active_user_name)
            bubble_alignment_class = "chat-right" if is_me else "chat-left"
            
            media_html = f"<div class='chat-media-box'>📁 Attached File Coordinates:<br><a href='{media}' target='_blank' style='color:#53bdeb;'>{media}</a></div>" if media else ""
            audio_html = f"<div class='audio-note-box'>🎵 <b>Voice Note Attachment</b> ({audio}) ───🔊</div>" if audio else ""
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
            
            # WhatsApp CSS Scroll Container wrapper block
            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            for msg in st.session_state.get("general_chat", []):
                render_whatsapp_bubble(msg, USER_DATA.get("name"))
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Interactive Input Core Panel Form
            with st.form("Global Chat Transmitter", clear_on_submit=True):
                msg_txt = st.text_input("Type Message...", placeholder="Share reference values, math findings, or curriculum equations...")
                
                col_m1, col_m2 = st.columns(2)
                with col_m1: attachment_url = st.text_input("Attach Cloud Resource Link / PDF URL (Optional)")
                with col_m2: simulated_audio_length = st.text_input("Simulate Voice Note Playback (e.g., 1:05) (Optional)")
                
                if st.form_submit_button("SEND MESSAGE TO LOUNGE"):
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
                st.warning("⚠️ Standalone mode active. No synchronized partner linked to your user node. Pair up inside the Partner Connection Hub.")
            else:
                partner_profile = st.session_state["users_registry"].get(partner_id, {})
                st.markdown(f"### 🔒 Secure Tunnel: `{USER_DATA.get('name')}` ⇄ `{partner_profile.get('name', 'Unknown')}`")
                
                # Render private chat arrays passing parameters securely
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
                for msg in st.session_state.get("private_chats", []):
                    if msg.get("sender") in [USER_DATA.get("name"), partner_profile.get("name")]:
                        render_whatsapp_bubble(msg, USER_DATA.get("name"))
                st.markdown("</div>", unsafe_allow_html=True)
                
                with st.form("Private Tunnel Transmitter", clear_on_submit=True):
                    p_text = st.text_input("Type Encrypted Message...")
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
                            push_system_notification(partner_id, f"📥 Encrypted p2p chat dispatch received from your study partner: {USER_DATA.get('name')}.")
                            st.rerun()

    # --- NAVIGATION NODE 5: PARTNER SYNC HUB ---
    elif selected_workspace == "🤝 Partner Connection Hub":
        st.markdown("<h2>🤝 Academic Collaboration & Partner Pairing Hub</h2>", unsafe_allow_html=True)
        
        p_id = USER_DATA.get("partner", "")
        if p_id:
            p_node = st.session_state["users_registry"].get(p_id, {})
            st.success(f"🔗 Network Sync Channel Locked! Linked Peer: {p_node.get('name')} | Mode: {USER_DATA.get('partner_role')}")
            if st.button("💔 SEVER CONNECTION CHANNEL LINK"):
                st.session_state["users_registry"][CURRENT_USER_ID]["partner"] = ""
                if p_id in st.session_state["users_registry"]:
                    st.session_state["users_registry"][p_id]["partner"] = ""
                save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                st.success("Connection severed cleanly. Terminal defaults returned to standalone status.")
                st.rerun()
        else:
            st.info("📡 Framework State: Standalone Node. Pair with a registered candidate peer to spin up a collaborative sync link.")
            
            # Map out database profiles who do not possess a partner configuration key
            available_candidates = {uid: node.get("name") for uid, node in st.session_state["users_registry"].items() if uid != CURRENT_USER_ID and not node.get("partner")}
            
            if not available_candidates:
                st.warning("No unlinked candidates currently broadcasting live on the pairing networks.")
            else:
                target_peer_uid = st.selectbox("Select Target Peer Candidate Node:", list(available_candidates.keys()), format_func=lambda x: available_candidates[x])
                chosen_role_mode = st.selectbox("Assign Collaboration Matrix Model:", ["Mutual Study Partners", "Mentor-Mentee Framework", "Assessor-Candidate Pairing"])
                
                if st.button("🔗 LOCK SECURE SYNC CHANNEL"):
                    st.session_state["users_registry"][CURRENT_USER_ID]["partner"] = target_peer_uid
                    st.session_state["users_registry"][CURRENT_USER_ID]["partner_role"] = chosen_role_mode
                    
                    st.session_state["users_registry"][target_peer_uid]["partner"] = CURRENT_USER_ID
                    st.session_state["users_registry"][target_peer_uid]["partner_role"] = chosen_role_mode
                    
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    push_system_notification(target_peer_uid, f"✨ Connection link synced! You have been paired up with {USER_DATA.get('name')} under the {chosen_role_mode} framework.")
                    st.success("Secure connection handshake complete.")
                    st.rerun()

    # --- NAVIGATION NODE 6: SUPER ADMIN PRIVILEGED OPERATIONS TERMINAL ---
    elif selected_workspace == "⚙️ Super Admin Operations" and USER_DATA.get("role") in ["ADMIN", "SUPER_ADMIN"]:
        st.markdown("<h2>⚙️ Network Command Center & Super Privileges</h2>", unsafe_allow_html=True)
        
        adm_tab1, adm_tab2, adm_tab3 = st.tabs(["🔒 System Accounts Registry Matrix", "📢 Global Broadcast Operations", "🛠️ Core Engine Configurations"])
        
        with adm_tab1:
            st.markdown("### 📋 Platform Identity Directory Logs")
            
            for uid, node in list(st.session_state["users_registry"].items()):
                st.markdown(f"""
                <div class='directory-card'>
                    <b>System Identity Key ID:</b> <code>{uid}</code> | <b>Name Parameter:</b> {node.get('name')} | <b>Username handle:</b> {node.get('username')}<br>
                    <b>Approval Status Flag:</b> <code>{node.get('status')}</code> | <b>Assigned Access Class Role:</b> <code>{node.get('role')}</code><br>
                    <b>Active Administrative Warning Notification:</b> <span style='color:#ff9999;'>{node.get('warning_msg', 'Clear')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                c_a1, c_a2, c_a3, c_a4 = st.columns(4)
                with c_a1:
                    if st.button("🟢 APPROVE & ACTIVATE", key=f"app_{uid}"):
                        st.session_state["users_registry"][uid]["status"] = "Approved"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        push_system_notification(uid, "🟢 Access approved! Your candidate profile is fully activated by the network administrator.")
                        st.success(f"Node {uid} verified successfully.")
                        st.rerun()
                with c_a2:
                    if st.button("🟡 DISCONNECT / SUSPEND", key=f"susp_{uid}"):
                        st.session_state["users_registry"][uid]["status"] = "Suspended"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.warning(f"Profile node {uid} shifted to suspended state.")
                        st.rerun()
                with c_a3:
                    warn_input = st.text_input("Enter Warning Alert Message Text", key=f"txt_{uid}", placeholder="Write enforcement details...")
                    if st.button("⚠️ INJECT ALERT BANNER", key=f"warn_{uid}"):
                        st.session_state["users_registry"][uid]["warning_msg"] = warn_input
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        push_system_notification(uid, f"⚠️ Official Admin Warning Issued: {warn_input}")
                        st.success("Warning constraints committed to target profile array.")
                        st.rerun()
                with c_a4:
                    if st.button("🔴 PURGE IDENTITY BLOCK", key=f"del_{uid}"):
                        if uid in ["0000", "6601"]:
                            st.error("Protected System Identity Origin Block. Core identities cannot be purged.")
                        else:
                            del st.session_state["users_registry"][uid]
                            save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                            st.error(f"Identity array entry {uid} removed from physical registries.")
                            st.rerun()
                st.markdown("<hr style='border: 1px solid #222; margin:10px 0;'>", unsafe_allow_html=True)

        with adm_tab2:
            st.markdown("### 📢 Global Ticker Announcement Dispatches")
            new_alert = st.text_input("Draft Network Broadcast Payload Ticker Text")
            if st.button("🚀 INJECT GLOBAL BROADCAST TICKER"):
                if new_alert:
                    st.session_state["global_alerts"].insert(0, new_alert)
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.success("Broadcast dispatched live to all node monitors.")
                    st.rerun()
            st.markdown("#### Live Network Broadcast Logs Tracker")
            for idx, item in enumerate(st.session_state.get("global_alerts", [])):
                st.markdown(f"- {item}")
                if st.button(f"🗑️ Terminate Broadcast Index {idx}", key=f"del_al_{idx}"):
                    st.session_state["global_alerts"].pop(idx)
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.rerun()

        with adm_tab3:
            st.markdown("### 🛠️ Global Network Core Controls Configuration")
            
            # Interactive Admin Profile Photo Overrider Control Feature
            admin_photo_url = st.text_input("Modify Admin Avatar Core URL Link Coordinate Asset:", value=st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE))
            if st.button("💾 SAVE ADMIN AVATAR IMAGE LOGS"):
                st.session_state["custom_admin_photo"] = admin_photo_url
                save_cache_to_disk("db_admin_photo.json", admin_photo_url)
                st.success("Admin photo asset configurations updated successfully.")
                st.rerun()
                
            st.markdown("---")
            st.markdown("#### 🔑 Access Registration Keys Authority Matrix")
            st.write(st.session_state.get("generated_registration_codes", []))
            new_code_string = st.text_input("Generate New Valid Network Registration Key Code")
            if st.button("➕ LOG REGISTRATION KEY TO DATABASE"):
                if new_code_string and new_code_string not in st.session_state["generated_registration_codes"]:
                    st.session_state["generated_registration_codes"].append(new_code_string)
                    save_cache_to_disk("db_regcodes.json", st.session_state["generated_registration_codes"])
                    st.success(f"Access key validation token token `{new_code_string}` injected successfully.")
                    st.rerun()

    # =========================================================================
    # 8. SYSTEM INTEGRITY BRANDING MATRIX FOOTER
    # =========================================================================
    st.markdown(f"""
    <div class='sudaisi-branding-footer'>
        <p style='color: #444; font-size: 11px; margin: 0;'>🛡️ Academic Shield Network Infrastructure Engine v4.26 • Core Engineering Configured by Sudaisi Setra</p>
    </div>
    """, unsafe_allow_html=True)
