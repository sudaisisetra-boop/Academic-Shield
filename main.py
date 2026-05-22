import streamlit as st
import pandas as pd
import datetime
import random
import os
import json

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
        <meta http-equiv="X-Frame-Options" content="DENY">
        <meta http-equiv="X-Content-Type-Options" content="nosniff">
    </head>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .timer-container {
        background-color: #111111;
        padding: 12px;
        border-radius: 8px;
        border: 2px solid #ff3333;
        text-align: center;
        margin-bottom: 10px;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 12px;
        margin-bottom: 8px;
        max-width: 75%;
        display: block;
    }
    .chat-left { background-color: #262730; color: white; margin-right: auto; text-align: left; }
    .chat-right { background-color: #ff3333; color: white; margin-left: auto; text-align: right; }
    .illustration-box { border: 2px dashed #444; border-radius: 6px; padding: 10px; margin: 10px 0; text-align: center; background-color: #1a1a1a; }
    .partner-alert-box { background-color: #111111; border: 2px solid #ff3333; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .fallback-alert-box { background-color: #1a1510; border: 1px dashed #ffa500; padding: 12px; border-radius: 6px; margin: 10px 0; }
    .top-profile-pic { border-radius: 50%; border: 2px solid #ff3333; object-fit: cover; width: 60px; height: 60px; }
    
    div.stButton > button {
        width: 100% !important;
        font-weight: bold !important;
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
        border-radius: 4px !important;
    }
    div.stButton > button:hover {
        background-color: #ff3333 !important;
        color: white !important;
        border-color: #ff3333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# 2. INBUILT NCDC OFFICIAL CURRICULUM DIRECTORY
# =========================================================================
NCDC_CURRICULUM_MAP = {
    "Mathematics": [
        "Numerical Concepts", "Equations and Inequalities", "Coordinate Geometry 1", 
        "Partial Fractions", "Trigonometry", "Descriptive Statistics", 
        "Scatter Diagrams and Correlations", "Dynamics 1", "Probability Theory", 
        "Differentiation 1", "Integration 1", "Permutations and Combinations", 
        "Series", "Random Variables", "Probability Distributions", "Error Analysis",
        "Vectors", "Differentiation 2", "Integration 2", "Dynamics 2", 
        "Trapezium Rule", "Sampling Distribution", "Iterative Methods", 
        "Coordinate Geometry 2", "Complex Numbers", "Differential Equations"
    ],
    "Physics": [
        "Measurement and Dimensions of Physical Quantities", "Statics", "Linear Motion", 
        "Motion Under Gravity", "Work, Energy and Power", "Solid Friction", 
        "Fluid Mechanics", "Mechanical Properties of Matter", "Thermometry", 
        "Heat Quantities", "Transfer of Heat", "Behaviour of Gases", "Thermodynamics", 
        "Reflection of Light", "Refraction of Light", "Optical Instruments", 
        "Electrostatics", "Capacitors"
    ],
    "Chemistry": [
        "Moles and Equations", "Atomic and Electronic Structure", "Bonding and Structure", 
        "Periodicity I (Trends & Group 2)", "Thermochemistry (Hess & Born-Haber)", 
        "Organic Chemistry I (Alkanes/Alkenes/Benzene)", "Equilibria I (Salt Hydrolysis/Buffers)", 
        "Equilibria II (Colligative)", "Organic Chemistry II (Alcohols/Carbonyls/Acids)", 
        "Electrochemistry (Cells & Faraday)", "Periodicity II (Group 14, 17, d-Block)", 
        "Organic Chemistry III (Amines/Polymers)", "Reaction Kinetics"
    ],
    "Biology": [
        "Cell Biology", "Nutrition", "Transport", "Respiration", "Homeostasis", 
        "Coordination", "Inheritance and Evolution", "Growth and Development", "Ecology"
    ],
    "S4_Mathematics": [
        "Three-Dimensional Geometry", "Loci and Modern Geometry", 
        "Advanced Statistics", "Probability", "Matrices and Linear Transformations"
    ],
    "S4_Physics": [
        "Electronics", "Radioactivity and Nuclear Physics", "Electromagnetism"
    ],
    "S4_Chemistry": [
        "Rates of Chemical Reactions and Reversible Reactions", "Organic Chemistry", "Electrolysis and Redox Reactions"
    ],
    "S4_Biology": [
        "Growth and Development in Plants and Animals", "Genetics", "Evolution"
    ]
}

# =========================================================================
# 3. FILE SYSTEM CONTROL & DATABASE MIRROR PROTECTION
# =========================================================================
SUDAISI_IMAGE_STREAM = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAFA3PEY8OF5GXFpmZ2hkb6b/2wBDNWZpboaFl6b/"

AVATAR_OPTIONS = [
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    "https://cdn-icons-png.flaticon.com/512/4140/4140037.png",
    "https://cdn-icons-png.flaticon.com/512/4140/4140048.png",
    "https://cdn-icons-png.flaticon.com/512/4139/4139981.png",
    "https://cdn-icons-png.flaticon.com/512/1999/1999625.png"
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
        with open(filename, "w") as f: 
            json.dump(data, f, default=str)
        backup_filename = f"backup_mirror_{filename}"
        with open(backup_filename, "w") as f_b:
            json.dump(data, f_b, default=str)
    except Exception: 
        pass

def load_cache_from_disk(filename, default_val):
    for target_file in [filename, f"backup_mirror_{filename}"]:
        if os.path.exists(target_file):
            try:
                with open(target_file, "r") as f: return json.load(f)
            except Exception: continue
    return default_val

# Database Instantiations
if "users_registry" not in st.session_state:
    st.session_state["users_registry"] = load_cache_from_disk("db_users.json", {
        "0000": {"username": "Admin", "pwd": "SudaisiAdmin2026", "name": "Sudaisi Setra", "class": "Senior Five", "school": "St Marys", "phone": "0752047103", "email": "admin@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry", "Biology"], "expiry": "2030-01-01", "status": "Approved", "avatar": "SUDAISI_BAKED", "partner": "Gideon Cheps"},
        "6601": {"username": "Setra stones", "pwd": "Amazima2026", "name": "Setra Stones", "class": "Senior Five", "school": "St Marys", "phone": "0752047103", "email": "setra@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry"], "expiry": "2030-01-01", "status": "Approved", "avatar": AVATAR_OPTIONS[0], "partner": ""},
        "6602": {"username": "Gideon Cheps", "pwd": "Gideon2026", "name": "Gideon Cheps", "class": "Senior Five", "school": "St Marys", "phone": "0700000000", "email": "gideon@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry"], "expiry": str(datetime.date.today() + datetime.timedelta(days=14)), "status": "Approved", "avatar": AVATAR_OPTIONS[1], "partner": "Admin"}
    })

if "pending_registrations" not in st.session_state: st.session_state["pending_registrations"] = load_cache_from_disk("db_pending.json", [])
if "general_chat" not in st.session_state: st.session_state["general_chat"] = load_cache_from_disk("db_genchat.json", [])
if "private_chats" not in st.session_state: st.session_state["private_chats"] = load_cache_from_disk("db_p2pchat.json", [])
if "suggestions" not in st.session_state: st.session_state["suggestions"] = load_cache_from_disk("db_suggestions.json", [])
if "global_alerts" not in st.session_state: st.session_state["global_alerts"] = load_cache_from_disk("db_alerts.json", ["🚀 Platform Online. Hardened Dual Mirror Protection Active."])
if "revision_notes" not in st.session_state: st.session_state["revision_notes"] = load_cache_from_disk("db_notes.json", {"Mathematics": [], "Physics": [], "Chemistry": [], "Biology": [], "S4_General": []})
if "exam_vault" not in st.session_state: st.session_state["exam_vault"] = load_cache_from_disk("db_exams.json", {})

if "generated_registration_codes" not in st.session_state:
    st.session_state["generated_registration_codes"] = load_cache_from_disk("db_regcodes.json", ["SHIELD2026", "ASP2026"])

if "online_users" not in st.session_state: st.session_state["online_users"] = {}
if "live_exam_invites" not in st.session_state: st.session_state["live_exam_invites"] = load_cache_from_disk("db_invites.json", {})

# =========================================================================
# 4. PORTAL INTERFACE MATRIX ROUTING
# =========================================================================
st.sidebar.title("🔐 ASP Access Interface")
app_mode = st.sidebar.radio("Select Portal Target Module", ["Login Page Panel", "Registration Terminal", "System Administrator Hub"])

col_head_title, col_head_pic = st.columns([11, 1])
with col_head_title:
    st.markdown("<h2 style='color:#ff3333; margin:0;'>🛡️ Academic Shield Pro</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#aaaaaa; font-style:italic; margin:0;'>“Conceptual Mastery and Real Testing Engine”</h5>", unsafe_allow_html=True)

# =========================================================================
# MODULE A: REGISTRATION TERMINAL
# =========================================================================
if app_mode == "Registration Terminal":
    st.subheader("📋 Student Account Registration Desk")
    st.info("💰 Notice: Send confirmation fee of 2000 UGX to mobile money line 0752047103 to finalize loops.")
    
    st.markdown("#### 👤 Select Your Profile Avatar Character")
    chosen_avatar_idx = st.slider("Slide to cycle through profile mascots:", 1, len(AVATAR_OPTIONS), 1)
    selected_avatar_url = AVATAR_OPTIONS[chosen_avatar_idx - 1]
    st.image(selected_avatar_url, width=75)
    
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
                "avatar": selected_avatar_url, "partner": "", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            }
            st.session_state["pending_registrations"].append(new_request)
            save_cache_to_disk("db_pending.json", st.session_state["pending_registrations"])
            st.success("✔ Payload captured! Awaiting Admin activation check.")

# =========================================================================
# MODULE B: LOGIN PAGE PANEL & CLIENT WORKSPACE
# =========================================================================
elif app_mode == "Login Page Panel":
    st.sidebar.subheader("🔒 Enter Active Credentials")
    login_uid = st.sidebar.text_input("User ID Code Token:")
    login_user = st.sidebar.text_input("Username:")
    login_pwd = st.sidebar.text_input("Password:", type="password")
    
    is_authenticated = False
    session_class = "Senior Five"
    session_partner = ""
    current_avatar_url = AVATAR_OPTIONS[0]
    
    if login_uid == "0000" and login_user == "Admin" and login_pwd == "SudaisiAdmin2026":
        is_authenticated = True
        session_user = "Admin"
        session_uid = "0000"
        session_class = "Senior Five"
        session_partner = st.session_state["users_registry"]["0000"].get("partner", "")
        allowed_subjects = ["Mathematics", "Physics", "Chemistry", "Biology"]
        current_avatar_url = "SUDAISI_BAKED"
    elif login_uid in st.session_state["users_registry"]:
        node = st.session_state["users_registry"][login_uid]
        if node["username"] == login_user and node["pwd"] == login_pwd:
            expiry_date = datetime.datetime.strptime(str(node["expiry"]), "%Y-%m-%d").date() if isinstance(node["expiry"], str) else node["expiry"]
            if datetime.date.today() > expiry_date:
                st.sidebar.error("❌ Account Locked! Access window expired.")
            elif node["status"] != "Approved":
                st.sidebar.error("❌ Access Suspended.")
            else:
                is_authenticated = True
                session_user = login_user
                session_uid = login_uid
                session_class = node.get("class", "Senior Five")
                session_partner = node.get("partner", "")
                allowed_subjects = node["subjects"]
                current_avatar_url = node.get("avatar", AVATAR_OPTIONS[0])

    with col_head_pic:
        if current_avatar_url == "SUDAISI_BAKED" or session_user == "Admin":
            st.markdown(f'<img src="{SUDAISI_IMAGE_STREAM}" class="top-profile-pic"/>', unsafe_allow_html=True)
        else:
            st.markdown(f'<img src="{current_avatar_url}" class="top-profile-pic"/>', unsafe_allow_html=True)

    if not is_authenticated:
        st.markdown("<div style='text-align:center; margin-top:12%;'><h3>🛡️ ASP PORTAL SECURITY SCREEN</h3><p>Provide your configurations to populate your dashboard matrix.</p></div>", unsafe_allow_html=True)
    else:
        st.session_state["online_users"][session_user] = datetime.datetime.now().strftime("%I:%M:%S %p")
        st.sidebar.success(f"Scholar: {session_user} ({session_class})")
        selected_subject = st.sidebar.selectbox("📚 Select Academic Subject Field", allowed_subjects)
        
        client_tab_choice = st.sidebar.radio("Navigate Workspace Pages", [
            "📝 Access Exam Center", "🤝 Partner Connection Hub", "📖 Revision Notes Portal", 
            "🌐 General Lounge Chat", "🔒 Private Peer Chatroom", "📊 Progress Tracker Logs", 
            "📁 Finished Exam Vault", "📩 Submit App Suggestions"
        ])

        if session_user in st.session_state["live_exam_invites"]:
            invite = st.session_state["live_exam_invites"][session_user]
            if invite["status"] == "pending":
                st.markdown(f"""
                <div class="partner-alert-box">
                    <h4 style="color:#ff3333; margin:0;">🔔 LIVE PARTNER EXAM CALL CONFLICT</h4>
                    <p style="margin:5px 0;">Your partner <strong>{invite['sender']}</strong> wants to sit a live <strong>{invite['subject']} ({invite['grade']})</strong> exam with you right now!</p>
                </div>
                """, unsafe_allow_html=True)
                col_acc, col_dec = st.columns(2)
                if col_acc.button("✅ Accept Invite", key="acc_shared_ex"):
                    st.session_state["live_exam_invites"][session_user]["status"] = "accepted"
                    save_cache_to_disk("db_invites.json", st.session_state["live_exam_invites"])
                    st.rerun()
                if col_dec.button("❌ Decline", key="dec_shared_ex"):
                    st.session_state["live_exam_invites"][session_user]["status"] = "declined"
                    save_cache_to_disk("db_invites.json", st.session_state["live_exam_invites"])
                    st.rerun()

        # =========================================================================
        # RE-ENGINEERED HIGH-DENSITY ASSESSMENT CENTER WITH CURRICULUM PRE-LOADS
        # =========================================================================
        if client_tab_choice == "📝 Access Exam Center":
            st.title("📝 Precision Topic Exam Center")
            
            lookup_key = f"S4_{selected_subject}" if session_class == "Senior Four" else selected_subject
            
            official_topics = NCDC_CURRICULUM_MAP.get(lookup_key, ["General Concepts"])
            dropdown_options = ["All Topics / Mix Scenario"] + official_topics
            
            selected_topic_target = st.selectbox("🎯 Target Challenge Topic Filter:", dropdown_options)
            
            sheet_data = read_public_sheet(lookup_key)
            
            parsed_questions_bank = []
            answer_keys = {}
            illustrations = {}
            
            if sheet_data is not None and not sheet_data.empty:
                sheet_data.columns = [str(c).strip() for c in sheet_data.columns]
                for idx, row in sheet_data.iterrows():
                    q_text = str(row.iloc[0]).strip()
                    parsed_questions_bank.append(row)
                    if len(row) > 1 and pd.notna(row.iloc[1]): answer_keys[q_text] = str(row.iloc[1]).strip().lower()
                    if len(row) > 2 and pd.notna(row.iloc[2]): illustrations[q_text] = str(row.iloc[2]).strip()

            filtered_pool = []
            fallback_triggered = False
            fallback_reason = ""

            if selected_topic_target == "All Topics / Mix Scenario":
                filtered_pool = [str(r.iloc[0]).strip() for r in parsed_questions_bank]
            else:
                for row_node in parsed_questions_bank:
                    if len(row_node) > 3 and pd.notna(row_node.iloc[3]):
                        cell_topics = str(row_node.iloc[3]).strip()
                        if selected_topic_target.lower() in cell_topics.lower():
                            filtered_pool.append(str(row_node.iloc[0]).strip())
                
                if not filtered_pool:
                    for row_node in parsed_questions_bank:
                        q_string = str(row_node.iloc[0]).strip()
                        if selected_topic_target.lower() in q_string.lower():
                            filtered_pool.append(q_string)
                    if filtered_pool:
                        fallback_triggered = True
                        fallback_reason = "Keyword Connection Extraction Match"

                if not filtered_pool:
                    filtered_pool = [str(r.iloc[0]).strip() for r in parsed_questions_bank]
                    if filtered_pool:
                        fallback_triggered = True
                        fallback_reason = "Random Global Subject Pool Injection"

            if not filtered_pool:
                filtered_pool = [
                    f"Analyze the real-world operational challenges connected with {selected_topic_target} in Uganda [NCDC Core Scenario Level A].", 
                    f"Formulate a definitive mathematical or experimental layout modeling {selected_topic_target} applications [NCDC Core Scenario Level B]."
                ]
                fallback_triggered = True
                fallback_reason = "System Synthetic Scenario Generator Engine"

            if fallback_triggered:
                st.markdown(f"""
                <div class="fallback-alert-box">
                    <span style="color:#ffa500; font-weight:bold;">📢 CURRICULUM FALLBACK SIGNAL ACTIVE</span><br>
                    <span style="font-size:13px; color:#ddd;">Specific questions for <strong>{selected_topic_target}</strong> are being finalized. To preserve your learning momentum, the system used its <strong>{fallback_reason}</strong> engine to keep you moving!</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### ✍️ Generate Targeted Assessment Paper")
            col_tr1, col_tr2 = st.columns([2, 2])
            with col_tr1:
                run_exam_trigger = st.button("🚀 Pull 2 Precision Scenario Questions")
            with col_tr2:
                if session_partner:
                    is_partner_online = session_partner in st.session_state["online_users"]
                    status_color = "#39ff14" if is_partner_online else "#ff3333"
                    st.markdown(f"Partner Link: **{session_partner}** (<span style='color:{status_color}; font-weight:bold;'>{'ONLINE' if is_partner_online else 'OFFLINE'}</span>)", unsafe_allow_html=True)

            if run_exam_trigger:
                st.session_state[f"seed_mod_{lookup_key}"] = random.randint(1, 99999)
                if session_partner and session_partner in st.session_state["online_users"]:
                    st.session_state["live_exam_invites"][session_partner] = {
                        "sender": session_user, "subject": selected_subject, 
                        "grade": session_class, "status": "pending", "seed": st.session_state[f"seed_mod_{lookup_key}"]
                    }
                    save_cache_to_disk("db_invites.json", st.session_state["live_exam_invites"])
                st.rerun()

            random.seed(st.session_state.get(f"seed_mod_{lookup_key}", 42))
            active_exam_items = random.sample(filtered_pool, min(len(filtered_pool), 2))
            
            for index, question_text in enumerate(active_exam_items, 1):
                st.markdown(f"<div style='background-color:#1e1e1e; padding:15px; border-radius:6px; margin-top:15px; border-left:4px solid #ff3333;'><strong style='color:#ff3333;'>Item {index}:</strong> {question_text}</div>", unsafe_allow_html=True)
                if question_text in illustrations:
                    img_url = illustrations[question_text]
                    if img_url.startswith("http"):
                        st.markdown(f'<div class="illustration-box"><img src="{img_url}" style="max-height:280px; border-radius:4px;"/></div>', unsafe_allow_html=True)
                
            st.markdown("##### ⏱️ Task Section Layout Countdown Indicators (25 Minutes Max Per Element)")
            timer_columns = st.columns(2)
            for idx in range(2):
                with timer_columns[idx]:
                    st.markdown("""<div class="timer-container"><span style='font-size:10px; color:#aaa;'>ITEM LIMIT</span><h4 style='color:#ff3333; margin:0;'>25:00</h4></div>""", unsafe_allow_html=True)
            
            st.markdown("---")
            st.write("✍️ **Hand in Finished Work Sheet Script**")
            typed_work = st.text_area("Type paragraph explanations or calculation proofs:")
            uploaded_img = st.file_uploader("Upload script image captures:", type=["jpg","jpeg","png"])
            
            if st.button("🚀 Transmit Answers Script"):
                if not typed_work.strip() and not uploaded_img:
                    st.warning("Please supply data fields before triggering.")
                else:
                    score_counter = 0
                    has_keys_at_all = False
                    for item_q in active_exam_items:
                        if item_q in answer_keys:
                            has_keys_at_all = True
                            if answer_keys[item_q] in typed_work.lower(): score_counter += 50
                                
                    if session_uid not in st.session_state["exam_vault"]: st.session_state["exam_vault"][session_uid] = []
                    if has_keys_at_all:
                        final_grade = min(score_counter, 100)
                        exam_payload = {"Subject": selected_subject, "Topic": selected_topic_target, "Date": str(datetime.date.today()), "Grade": f"{final_grade}%", "Status": "Graded Instantly via Sheet Key"}
                        st.success(f"🎯 Graded Instantly! Score: {final_grade}/100 Marks.")
                    else:
                        exam_payload = {"Subject": selected_subject, "Topic": selected_topic_target, "Date": str(datetime.date.today()), "Grade": "Pending Review", "Status": "Forwarded to Reviewer Panels"}
                        st.info("📋 Proof Answer Captured: Script forwarded to reviewer panels.")
                        
                    st.session_state["exam_vault"][session_uid].append(exam_payload)
                    save_cache_to_disk("db_exams.json", st.session_state["exam_vault"])

        # =========================================================================
        # CORE OPERATIONAL LOGIC FEATURES
        # =========================================================================
        elif client_tab_choice == "🤝 Partner Connection Hub":
            st.title("🤝 Academic Partners Registry")
            st.markdown(f"Linked Partner Profile Name: **{session_partner if session_partner else 'None Linked'}**")
            new_p_assign = st.text_input("Enter target student username link:")
            if st.button("Bind Accountability Matrix"):
                if new_p_assign.strip():
                    st.session_state["users_registry"][session_uid]["partner"] = new_p_assign.strip()
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success(f"Sync complete for: {new_p_assign}")
                    st.rerun()

        elif client_tab_choice == "🌐 General Lounge Chat":
            st.title("🌐 General Chatroom Terminal")
            for msg in st.session_state["general_chat"]:
                align_cls = "chat-right" if msg["sender"] == session_user else "chat-left"
                st.markdown(f"<div class='chat-bubble {align_cls}'><strong>{msg['sender']}</strong> <span style='font-size:10px; color:#aaa;'>[{msg['time']}]</span>: {msg['text']}</div>", unsafe_allow_html=True)
            in_gen_msg = st.text_input("Type message:", key="in_gen_msg_str")
            if st.button("Send to Lounge"):
                if in_gen_msg.strip():
                    st.session_state["general_chat"].append({"sender": session_user, "text": in_gen_msg, "time": datetime.datetime.now().strftime("%I:%M:%S %p")})
                    save_cache_to_disk("db_genchat.json", st.session_state["general_chat"])
                    st.rerun()

        elif client_tab_choice == "📖 Revision Notes Portal":
            st.title(f"📖 Notes Portal - {selected_subject}")
            notes_array = st.session_state["revision_notes"].get("S4_General" if session_class == "Senior Four" else lookup_key, [])
            for item in notes_array:
                with st.expander(f"📁 Note: {item['title']}"): st.write(item["content"])

        elif client_tab_choice == "🔒 Private Peer Chatroom":
            st.title("🔒 Inbuilt Private Chat Matrix")
            target_p = st.text_input("Enter recipient username link:")
            for msg in st.session_state["private_chats"]:
                st.markdown(f"<div class='chat-bubble chat-left'><strong>{msg['sender']}</strong> <span style='font-size:10px; color:#aaa;'>[{msg['time']}]</span>: {msg['text']}</div>", unsafe_allow_html=True)
            in_priv_msg = st.text_input("Type private text:", key="in_priv_msg_str")
            if st.button("Send Private Message"):
                if in_priv_msg.strip():
                    st.session_state["private_chats"].append({"sender": session_user, "text": in_priv_msg, "to": target_p, "time": datetime.datetime.now().strftime("%I:%M:%S %p")})
                    save_cache_to_disk("db_p2pchat.json", st.session_state["private_chats"])
                    st.rerun()

        elif client_tab_choice == "📊 Progress Tracker Logs":
            st.title("📊 Progress Log Sheets")
            st.table(pd.DataFrame(st.session_state["exam_vault"].get(session_uid, [])))

        elif client_tab_choice == "📁 Finished Exam Vault":
            st.title("📁 Historic Exam Vault")
            st.write(st.session_state["exam_vault"].get(session_uid, []))

        elif client_tab_choice == "📩 Submit App Suggestions":
            st.title("📩 Public Feedback Portal")
            for sug in st.session_state["suggestions"]:
                st.markdown(f"<div style='background-color:#111; padding:10px; margin-bottom:5px; border-radius:4px;'><strong>{sug['user']}</strong> <span style='font-size:10px; color:grey;'>[{sug['time']}]</span>: {sug['text']}<br><span style='color:#ff3333; font-size:12px;'>Outcome: {sug['reply']}</span></div>", unsafe_allow_html=True)
            in_sug_text = st.text_area("Propose adjustments:")
            if st.button("Submit Suggestion Log"):
                if in_sug_text.strip():
                    st.session_state["suggestions"].append({"user": session_user, "text": in_sug_text, "reply": "Awaiting Review.", "time": datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")})
                    save_cache_to_disk("db_suggestions.json", st.session_state["suggestions"])
                    st.success("Suggestion logged successfully!")
                    st.rerun()

# =========================================================================
# MODULE C: CENTRAL SYSTEM ADMINISTRATIVE DASHBOARD (ROOT HUB)
# =========================================================================
elif app_mode == "System Administrator Hub":
    st.subheader("🛡️ Administrative Dashboard Terminal")
    admin_token = st.text_input("Enter Admin Verification Password:", type="password")
    
    if admin_token == "SudaisiAdmin2026":
        st.success("✔ Root Privileges Enabled.")
        adm_t1, adm_t2, adm_t3, adm_t4, adm_t5 = st.tabs(["👥 Registrations Pipeline", "👤 Directory Control & Codes", "📖 Notes Uploads", "📢 Mass Alerts", "📩 Suggestions Responses"])
        
        with adm_t1:
            st.subheader(f"🔔 Queue Counter: {len(st.session_state['pending_registrations'])} Registrations Awaiting Verification")
            for index, item_node in enumerate(st.session_state["pending_registrations"]):
                st.markdown(f"📌 **Request Profile {index+1}:** User: `{item_node['username']}` ({item_node.get('class','S5')}) | Sent: {item_node['timestamp']}")
                if st.button(f"🟢 Approve Profile & Grant Entry ID for {item_node['username']}", key=f"p_app_{index}"):
                    allocated_uid_id = str(6601 + len(st.session_state["users_registry"]))
                    st.session_state["users_registry"][allocated_uid_id] = {
                        "username": item_node["username"], "pwd": item_node["pwd"], "name": item_node["name"],
                        "class": item_node["class"], "school": item_node["school"], "phone": item_node["phone"],
                        "email": item_node["email"], "gender": item_node["gender"], "location": item_node["location"],
                        "subjects": item_node["subjects"], "status": "Approved", "avatar": item_node.get("avatar", AVATAR_OPTIONS[0]),
                        "partner": "", "expiry": str(datetime.date.today() + datetime.timedelta(days=14))
                    }
                    st.session_state["pending_registrations"].pop(index)
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    save_cache_to_disk("db_pending.json", st.session_state["pending_registrations"])
                    st.success(f"Activated! User ID Assigned: `{allocated_uid_id}`")
                    st.rerun()

        with adm_t2:
            st.subheader("🔑 Registration Codes Token Generator")
            new_generated_code = st.text_input("Create structural verification code string:")
            if st.button("Generate Code Token"):
                if new_generated_code.strip():
                    st.session_state["generated_registration_codes"].append(new_generated_code.strip())
                    save_cache_to_disk("db_regcodes.json", st.session_state["generated_registration_codes"])
                    st.success("Code token active!")

        with adm_t3:
            st.subheader("📖 Upload Subject Notes")
            note_subj = st.selectbox("Choose Target Destination:", ["Mathematics", "Physics", "Chemistry", "Biology", "S4_General"])
            note_head = st.text_input("Enter Notes Title Header:")
            note_body = st.text_area("Paste resource content strings:")
            if st.button("📦 Sync Notes Resource"):
                if note_head and note_body:
                    st.session_state["revision_notes"][note_subj].append({"title": note_head, "content": note_body, "date": str(datetime.date.today())})
                    save_cache_to_disk("db_notes.json", st.session_state["revision_notes"])
                    st.success("Notes compiled!")

        with adm_t4:
            st.subheader("📢 Broadcast Mass Notifications")
            alert_msg = st.text_input("Type urgent messaging updates:")
            if st.button("Broadcast Priority Alert Notification Everywhere"):
                if alert_msg.strip():
                    st.session_state["global_alerts"].append(alert_msg)
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.success("Alert broadcast injected successfully.")

        with adm_t5:
            st.subheader("📩 Process Suggestion Response Loop")
            for idx, log in enumerate(st.session_state["suggestions"]):
                st.markdown(f"**From Student:** {log['user']} | **Content:** {log['text']}")
                reply_text = st.text_input("Formulate resolution outcome:", key=f"adm_rep_{idx}")
                if st.button("Publish Response", key=f"adm_btn_{idx}"):
                    st.session_state["suggestions"][idx]["reply"] = reply_text
                    save_cache_to_disk("db_suggestions.json", st.session_state["suggestions"])
                    st.success("Response resolution updated.")
                    st.rerun()
