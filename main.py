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

st.logo("https://cdn-icons-png.flaticon.com/512/3135/3135715.png")

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
    .system-warn-box { background-color: #3b1111; border: 2px solid #ff3333; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #ff9999; }
    .fallback-alert-box { background-color: #1a1510; border: 1px dashed #ffa500; padding: 12px; border-radius: 6px; margin: 10px 0; }
    .top-profile-pic { border-radius: 50%; border: 2px solid #ff3333; object-fit: cover; width: 60px; height: 60px; }
    .notification-badge { background-color: #ff3333; color: white; padding: 2px 8px; border-radius: 10px; font-weight: bold; font-size: 11px; margin-left: 5px; }
    .admin-broadcast-banner { background-color: #ff3333; color: white; padding: 10px; border-radius: 6px; font-weight: bold; text-align: center; margin-bottom: 15px; }
    
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
    "Mathematics": ["Numerical Concepts", "Equations and Inequalities", "Coordinate Geometry 1", "Partial Fractions", "Trigonometry", "Descriptive Statistics", "Vectors", "Differentiation 1", "Integration 1", "Complex Numbers", "Differential Equations"],
    "Physics": ["Measurement and Dimensions", "Statics", "Linear Motion", "Fluid Mechanics", "Mechanical Properties of Matter", "Thermometry", "Heat Quantities", "Electrostatics", "Capacitors"],
    "Chemistry": ["Moles and Equations", "Atomic and Electronic Structure", "Bonding and Structure", "Periodicity I", "Thermochemistry", "Organic Chemistry I", "Equilibria I", "Electrochemistry"],
    "Biology": ["Cell Biology", "Nutrition", "Transport", "Respiration", "Homeostasis", "Coordination", "Ecology"],
    "S4_Mathematics": ["Three-Dimensional Geometry", "Loci and Modern Geometry", "Advanced Statistics", "Probability"],
    "S4_Physics": ["Electronics", "Radioactivity and Nuclear Physics", "Electromagnetism"],
    "S4_Chemistry": ["Rates of Chemical Reactions", "Organic Chemistry", "Electrolysis and Redox"],
    "S4_Biology": ["Growth and Development", "Genetics", "Evolution"]
}

# =========================================================================
# 3. FILE SYSTEM & GOOGLE SHEETS LIVE EXTRACTOR ENGINE
# =========================================================================
SUDAISI_IMAGE_STREAM = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAFA3PEY8OF5GXFpmZ2hkb6b/2wBDNWZpboaFl6b/"
AVATAR_OPTIONS = [
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    "https://cdn-icons-png.flaticon.com/512/4140/4140037.png",
    "https://cdn-icons-png.flaticon.com/512/4140/4140048.png",
    "https://cdn-icons-png.flaticon.com/512/4139/4139981.png"
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

# Database Engine Restorations
if "users_registry" not in st.session_state:
    st.session_state["users_registry"] = load_cache_from_disk("db_users.json", {
        "0000": {"username": "Admin", "pwd": "SudaisiAdmin2026", "name": "Sudaisi Setra", "class": "Senior Five", "school": "St Marys", "phone": "0752047103", "email": "admin@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry", "Biology"], "expiry": "2030-01-01", "status": "Approved", "warning_msg": "", "avatar": "SUDAISI_BAKED", "partner": "Gideon Cheps"},
        "6601": {"username": "Setra stones", "pwd": "Amazima2026", "name": "Setra Stones", "class": "Senior Five", "school": "St Marys", "phone": "0752047103", "email": "setra@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry"], "expiry": "2030-01-01", "status": "Approved", "warning_msg": "", "avatar": AVATAR_OPTIONS[0], "partner": ""},
        "6602": {"username": "Gideon Cheps", "pwd": "Gideon2026", "name": "Gideon Cheps", "class": "Senior Five", "school": "St Marys", "phone": "0700000000", "email": "gideon@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry"], "expiry": "2030-01-01", "status": "Approved", "warning_msg": "", "avatar": AVATAR_OPTIONS[1], "partner": "Admin"}
    })

if "pending_registrations" not in st.session_state: st.session_state["pending_registrations"] = load_cache_from_disk("db_pending.json", [])
if "general_chat" not in st.session_state: st.session_state["general_chat"] = load_cache_from_disk("db_genchat.json", [])
if "private_chats" not in st.session_state: st.session_state["private_chats"] = load_cache_from_disk("db_p2pchat.json", [])
if "suggestions" not in st.session_state: st.session_state["suggestions"] = load_cache_from_disk("db_suggestions.json", [])
if "global_alerts" not in st.session_state: st.session_state["global_alerts"] = load_cache_from_disk("db_alerts.json", ["🚀 Platform Online. Hardened Dual Mirror Protection Active."])
if "revision_notes" not in st.session_state: st.session_state["revision_notes"] = load_cache_from_disk("db_notes.json", {"Mathematics": [], "Physics": [], "Chemistry": [], "Biology": [], "S4_General": []})
if "exam_vault" not in st.session_state: st.session_state["exam_vault"] = load_cache_from_disk("db_exams.json", {})
if "last_read_tracker" not in st.session_state: st.session_state["last_read_tracker"] = load_cache_from_disk("db_readtrack.json", {})
if "generated_registration_codes" not in st.session_state: st.session_state["generated_registration_codes"] = load_cache_from_disk("db_regcodes.json", ["SHIELD2026", "ASP2026"])
if "online_users" not in st.session_state: st.session_state["online_users"] = {}
if "live_exam_invites" not in st.session_state: st.session_state["live_exam_invites"] = load_cache_from_disk("db_invites.json", {})

# Auto-Sync Background Pull from Google Sheets for Note Materials
sheet_notes_df = read_public_sheet("Notes")
if sheet_notes_df is not None and not sheet_notes_df.empty:
    try:
        for idx, row in sheet_notes_df.iterrows():
            s_subj = str(row.iloc[0]).strip()
            s_class = str(row.iloc[1]).strip()
            s_title = str(row.iloc[2]).strip()
            s_content = str(row.iloc[3]).strip()
            
            l_key = f"S4_{s_subj}" if s_class == "Senior Four" else s_subj
            if l_key in st.session_state["revision_notes"]:
                if not any(n['title'] == s_title for n in st.session_state["revision_notes"][l_key]):
                    st.session_state["revision_notes"][l_key].append({
                        "title": s_title, "content": s_content, "target_class": s_class, "date": "Sheet Sync"
                    })
    except Exception:
        pass

# =========================================================================
# 4. INITIALIZE AUTHENTICATION SCOPE TO PREVENT NAMEERRORS
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

# =========================================================================
# 5. PORTAL INTERFACE MATRIX ROUTING
# =========================================================================
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
        session_partner = st.session_state["users_registry"]["0000"].get("partner", "")
        allowed_subjects = ["Mathematics", "Physics", "Chemistry", "Biology"]
        current_avatar_url = "SUDAISI_BAKED"
        user_account_status = "Approved"
    elif login_uid in st.session_state["users_registry"]:
        node = st.session_state["users_registry"][login_uid]
        if node["username"] == login_user and node["pwd"] == login_pwd:
            user_account_status = node.get("status", "Approved")
            account_warning_text = node.get("warning_msg", "")
            
            if user_account_status == "Banned" or user_account_status == "Locked":
                st.sidebar.error("❌ Access Terminated! This profile account has been suspended by Admin.")
            else:
                is_authenticated = True
                session_user = login_user
                session_uid = login_uid
                session_class = node.get("class", "Senior Five")
                session_partner = node.get("partner", "")
                allowed_subjects = node["subjects"]
                current_avatar_url = node.get("avatar", AVATAR_OPTIONS[0])

# =========================================================================
# INTERFACE TOP BANNER RENDER
# =========================================================================
col_head_title, col_head_pic = st.columns([11, 1])
with col_head_title:
    st.markdown("<h2 style='color:#ff3333; margin:0;'>🛡️ Academic Shield Pro</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#aaaaaa; font-style:italic; margin:0;'>“Conceptual Mastery and Real Testing Engine”</h5>", unsafe_allow_html=True)

with col_head_pic:
    if current_avatar_url == "SUDAISI_BAKED" or session_user == "Admin":
        st.markdown(f'<img src="{SUDAISI_IMAGE_STREAM}" class="top-profile-pic"/>', unsafe_allow_html=True)
    else:
        st.markdown(f'<img src="{current_avatar_url}" class="top-profile-pic"/>', unsafe_allow_html=True)

# =========================================================================
# MODULE A: REGISTRATION TERMINAL
# =========================================================================
if app_mode == "Registration Terminal":
    st.subheader("📋 Student Account Registration Desk")
    st.info("💰 Notice: Send confirmation fee of 2000 UGX to mobile money line 0752047103 to finalize loops.")
    
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
# MODULE B: LOGIN PAGE PANEL & CLIENT WORKSPACE
# =========================================================================
elif app_mode == "Login Page Panel":
    if not is_authenticated:
        st.markdown("<div style='text-align:center; margin-top:12%;'><h3>🛡️ ASP PORTAL SECURITY SCREEN</h3><p>Provide your configurations inside the left side interface panel to populate your dashboard matrix.</p></div>", unsafe_allow_html=True)
    else:
        if account_warning_text:
            st.markdown(f'<div class="system-warn-box">⚠️ <strong>SYSTEM ADMIN WARNING FLAG:</strong> {account_warning_text}</div>', unsafe_allow_html=True)
            
        if st.session_state["global_alerts"]:
            st.markdown(f'<div class="admin-broadcast-banner">📢 BROADCAST: {st.session_state["global_alerts"][-1]}</div>', unsafe_allow_html=True)

        st.session_state["online_users"][session_user] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        u_last = st.session_state["last_read_tracker"].get(session_user, "1970-01-01 00:00:00")
        unread_p2p_cnt = sum(1 for m in st.session_state["private_chats"] if m.get("to") == session_user and m.get("timestamp", "") > u_last)
        unread_gen_cnt = sum(1 for m in st.session_state["general_chat"] if m.get("sender") != session_user and m.get("timestamp", "") > u_last)
        total_badge_weight = unread_p2p_cnt + unread_gen_cnt
        
        badge_indicator = f" ({total_badge_weight} Unread)" if total_badge_weight > 0 else ""
        selected_subject = st.sidebar.selectbox("📚 Select Academic Subject Field", allowed_subjects)
        
        client_tab_choice = st.sidebar.radio(f"Workspace Channels {badge_indicator}", [
            "📝 Access Exam Center", "🤝 Partner Connection Hub", "📖 Revision Notes Portal", 
            "🌐 General Lounge Chat", "🔒 Private Peer Chatroom", "📊 Progress Tracker Logs", 
            "📁 Finished Exam Vault", "🔑 Change Account Password", "📩 Submit App Suggestions"
        ])

        if client_tab_choice == "📝 Access Exam Center":
            st.title("📝 Precision Topic Exam Center")
            lookup_key = f"S4_{selected_subject}" if session_class == "Senior Four" else selected_subject
            official_topics = NCDC_CURRICULUM_MAP.get(lookup_key, ["General Concepts"])
            selected_topic_target = st.selectbox("🎯 Target Challenge Topic Filter:", ["All Topics"] + official_topics)
            
            sheet_data = read_public_sheet(lookup_key)
            filtered_pool = []
            if sheet_data is not None and not sheet_data.empty:
                filtered_pool = [str(r.iloc[0]).strip() for idx, r in sheet_data.iterrows()]
            
            if not filtered_pool:
                filtered_pool = [f"Synthesized Core evaluation task context on {selected_topic_target} for evaluation."]
                
            st.markdown("### ✍️ Pull Evaluation Tasks")
            if st.button("🚀 Load Targeted Matrix Exam Paper"):
                st.session_state[f"seed_{lookup_key}"] = random.randint(1, 10000)
                st.rerun()
                
            random.seed(st.session_state.get(f"seed_{lookup_key}", 42))
            selected_questions = random.sample(filtered_pool, min(len(filtered_pool), 2))
            
            for i, q in enumerate(selected_questions, 1):
                st.markdown(f"<div style='background-color:#1e1e1e; padding:15px; border-radius:6px; margin-top:10px; border-left:4px solid #ff3333;'><strong>Item {i}:</strong> {q}</div>", unsafe_allow_html=True)

            typed_work = st.text_area("Type your explanation or proof strings:")
            if st.button("🚀 Transmit Answers Script"):
                if typed_work.strip():
                    if session_uid not in st.session_state["exam_vault"]: st.session_state["exam_vault"][session_uid] = []
                    st.session_state["exam_vault"][session_uid].append({"Subject": selected_subject, "Topic": selected_topic_target, "Date": str(datetime.date.today()), "Grade": "Pending Review", "Status": "Forwarded"})
                    save_cache_to_disk("db_exams.json", st.session_state["exam_vault"])
                    st.success("✔ Exam script secured!")

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

        elif client_tab_choice == "📖 Revision Notes Portal":
            st.title(f"📖 Protected Notes Portal - {selected_subject}")
            lookup_key = f"S4_{selected_subject}" if session_class == "Senior Four" else selected_subject
            
            notes_array = st.session_state["revision_notes"].get(lookup_key, [])
            filtered_notes = [n for n in notes_array if n.get("target_class", session_class) == session_class]
            
            if not filtered_notes:
                st.info(f"📅 No specific verified material published for {session_class} {selected_subject} yet.")
            for note in filtered_notes:
                with st.expander(f"📘 Material: {note['title']} ({note.get('date','Direct Sync')})"):
                    st.write(note["content"])
                    st.markdown("<span style='color:grey; font-size:11px;'>Authorized Level: Clear Access</span>", unsafe_allow_html=True)

        elif client_tab_choice == "🌐 General Lounge Chat":
            st.title("🌐 General Chatroom Channel")
            st.session_state["last_read_tracker"][session_user] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
            
            for msg in st.session_state["general_chat"]:
                align_cls = "chat-right" if msg["sender"] == session_user else "chat-left"
                st.markdown(f"<div class='chat-bubble {align_cls}'><strong>{msg['sender']}</strong> <span style='font-size:10px; color:#aaa;'>[{msg['time']}]</span>:<br>{msg['text']}</div>", unsafe_allow_html=True)
                
            in_gen_msg = st.text_input("Type general chat string message:", key="in_gen_chat_box")
            if st.button("Send to Lounge Channel"):
                if in_gen_msg.strip():
                    st.session_state["general_chat"].append({
                        "sender": session_user, "text": in_gen_msg.strip(), 
                        "time": datetime.datetime.now().strftime("%I:%M %p"),
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_cache_to_disk("db_genchat.json", st.session_state["general_chat"])
                    st.rerun()

        elif client_tab_choice == "🔒 Private Peer Chatroom":
            st.title("🔒 Isolated Private Chat Room Matrix")
            st.session_state["last_read_tracker"][session_user] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
            
            all_usernames = [u["username"] for k, u in st.session_state["users_registry"].items() if u["username"] != session_user]
            target_p = st.selectbox("Select Target Recipient Buddy to Message:", all_usernames)
            
            isolated_thread = [
                m for m in st.session_state["private_chats"]
                if (m["sender"] == session_user and m["to"] == target_p) or (m["sender"] == target_p and m["to"] == session_user)
            ]
            
            for msg in isolated_thread:
                align_cls = "chat-right" if msg["sender"] == session_user else "chat-left"
                st.markdown(f"<div class='chat-bubble {align_cls}'><strong>{msg['sender']}</strong> <span style='font-size:10px; color:#aaa;'>[{msg['time']}]</span>:<br>{msg['text']}</div>", unsafe_allow_html=True)
                
            in_priv_msg = st.text_input("Type secure message string:", key="in_p2p_box")
            if st.button("Send Secure Private Message"):
                if in_priv_msg.strip() and target_p:
                    st.session_state["private_chats"].append({
                        "sender": session_user, "to": target_p, "text": in_priv_msg.strip(),
                        "time": datetime.datetime.now().strftime("%I:%M %p"),
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_cache_to_disk("db_p2pchat.json", st.session_state["private_chats"])
                    st.rerun()

        elif client_tab_choice == "📊 Progress Tracker Logs":
            st.title("📊 Progress Log Sheets")
            st.table(pd.DataFrame(st.session_state["exam_vault"].get(session_uid, [])))

        elif client_tab_choice == "📁 Finished Exam Vault":
            st.title("📁 Historic Exam Vault")
            st.write(st.session_state["exam_vault"].get(session_uid, []))

        # =========================================================================
        # NEW INTEGRATED FEATURE: RE-ENGINEERED CHANGE PASSWORD CHANNEL
        # =========================================================================
        elif client_tab_choice == "🔑 Change Account Password":
            st.title("🔑 Change Account Access Password")
            st.markdown("Update your account authentication token keys below. Changes take sync effect instantly.")
            
            p_old = st.text_input("Enter Current Password:", type="password", key="pwd_chg_old")
            p_new1 = st.text_input("Enter Brand New Password:", type="password", key="pwd_chg_n1")
            p_new2 = st.text_input("Confirm Brand New Password:", type="password", key="pwd_chg_n2")
            
            if st.button("🔄 Commit Password Sync Payload"):
                current_matching_pwd = st.session_state["users_registry"][session_uid]["pwd"]
                
                if p_old != current_matching_pwd:
                    st.error("❌ Authentication Error: The 'Current Password' you typed does not match our records.")
                elif not p_new1 or not p_new2:
                    st.error("❌ Field Validation Error: New password inputs cannot be blank.")
                elif p_new1 != p_new2:
                    st.error("❌ Discrepancy Error: The two new passwords do not match each other.")
                elif p_new1 == current_matching_pwd:
                    st.warning("⚠️ Optimization Check: The new password cannot be identical to your old password.")
                else:
                    st.session_state["users_registry"][session_uid]["pwd"] = p_new1.strip()
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success("✔ Secure Sync Complete! Your password has been updated across all mirrors successfully.")

        elif client_tab_choice == "📩 Submit App Suggestions":
            st.title("📩 Public Feedback Portal")
            in_sug_text = st.text_area("Propose adjustments:")
            if st.button("Submit Suggestion"):
                if in_sug_text.strip():
                    st.session_state["suggestions"].append({"user": session_user, "text": in_sug_text.strip(), "reply": "Awaiting Review.", "time": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")})
                    save_cache_to_disk("db_suggestions.json", st.session_state["suggestions"])
                    st.success("Logged successfully!")

# =========================================================================
# MODULE C: CENTRAL SYSTEM ADMINISTRATIVE DASHBOARD (ROOT CONTROL HUD)
# =========================================================================
elif app_mode == "System Administrator Hub":
    st.subheader("🛡️ Administrative Dashboard Terminal")
    admin_token = st.text_input("Enter Admin Verification Password:", type="password")
    
    if admin_token == "SudaisiAdmin2026":
        st.success("✔ Root Privileges Enabled.")
        adm_t0, adm_t1, adm_t2, adm_t3, adm_t4 = st.tabs(["🛑 GOD-MODE USER ACCOUNT ACCOUNTABILITY CONTROL", "👥 Registrations Pipeline", "📖 Notes Uploads Desk", "📢 Mass Broadcasts", "📩 Suggestions Responses"])
        
        with adm_t0:
            st.subheader("🛑 Master User Account Management Center")
            st.markdown("Modify permissions or terminate abusive account access strings down down instantly.")
            
            for uid_key, user_node in list(st.session_state["users_registry"].items()):
                if uid_key == "0000": continue 
                
                col_u1, col_u2, col_u3, col_u4, col_u5 = st.columns([3, 2, 2, 2, 2])
                with col_u1:
                    st.markdown(f"👤 **{user_node['username']}** ({user_node['class']})<br>`ID: {uid_key}` | Status: **{user_node.get('status','Approved')}**", unsafe_allow_html=True)
                with col_u2:
                    warn_input = st.text_input("Warning Text String Message:", key=f"warn_txt_{uid_key}", placeholder="Type warning flag...")
                    if st.button("⚠️ Warn User", key=f"btn_warn_{uid_key}"):
                        st.session_state["users_registry"][uid_key]["warning_msg"] = warn_input
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.warning(f"Issued Warning alert flag directly to {user_node['username']}")
                with col_u3:
                    if st.button("🔒 Ban/Lock Account", key=f"btn_lock_{uid_key}"):
                        st.session_state["users_registry"][uid_key]["status"] = "Banned"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.error(f"Terminated profile access token authorization for {user_node['username']}")
                        st.rerun()
                with col_u4:
                    if st.button("🔓 Restore/Approve Account", key=f"btn_res_{uid_key}"):
                        st.session_state["users_registry"][uid_key]["status"] = "Approved"
                        st.session_state["users_registry"][uid_key]["warning_msg"] = ""
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.success(f"Restored clean status clear loops for {user_node['username']}")
                        st.rerun()
                with col_u5:
                    if st.button("❌ Completely Delete Account", key=f"btn_del_{uid_key}"):
                        st.session_state["users_registry"].pop(uid_key)
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.info("Purged profile entirely from system mirrors.")
                        st.rerun()
                st.markdown("---")

        with adm_t1:
            st.subheader(f"🔔 Verification Queue Counter: {len(st.session_state['pending_registrations'])}")
            for index, item_node in enumerate(st.session_state["pending_registrations"]):
                st.markdown(f"📌 **Request Profile {index+1}:** User: `{item_node['username']}` | Sent: {item_node['timestamp']}")
                if st.button(f"🟢 Approve Profile & Grant Entry ID for {item_node['username']}", key=f"p_app_{index}"):
                    allocated_uid_id = str(6601 + len(st.session_state["users_registry"]))
                    st.session_state["users_registry"][allocated_uid_id] = {
                        "username": item_node["username"], "pwd": item_node["pwd"], "name": item_node["name"],
                        "class": item_node["class"], "school": item_node["school"], "phone": item_node["phone"],
                        "email": item_node["email"], "gender": item_node["gender"], "location": item_node["location"],
                        "subjects": item_node["subjects"], "status": "Approved", "warning_msg": "", "avatar": AVATAR_OPTIONS[0],
                        "partner": "", "expiry": "2030-01-01"
                    }
                    st.session_state["pending_registrations"].pop(index)
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    save_cache_to_disk("db_pending.json", st.session_state["pending_registrations"])
                    st.success(f"Activated ID Token: `{allocated_uid_id}`")
                    st.rerun()

        with adm_t2:
            st.subheader("📖 Upload Protected Subject Revision Notes Material")
            note_subj = st.selectbox("Choose Target Subject Fields Material:", ["Mathematics", "Physics", "Chemistry", "Biology"])
            note_class = st.selectbox("Target Class Grade Level Restrictions Rules:", ["Senior Four", "Senior Five", "Senior Six"])
            note_head = st.text_input("Enter Revision Notes Title Header Text:")
            note_body = st.text_area("Paste structural resource contents strings:")
            
            if st.button("📦 Sync Notes Content Resource to Mirrors"):
                if note_head and note_body:
                    lookup_key = f"S4_{note_subj}" if note_class == "Senior Four" else note_subj
                    st.session_state["revision_notes"][lookup_key].append({
                        "title": note_head.strip(), "content": note_body.strip(), "target_class": note_class, "date": str(datetime.date.today())
                    })
                    save_cache_to_disk("db_notes.json", st.session_state["revision_notes"])
                    st.success(f"✔ Live deployed inside app portal framework channel for {note_class} {note_subj}!")

        with adm_t3:
            st.subheader("📢 High Priority Admin Announcement Global Engine Broadcast")
            alert_msg = st.text_input("Type critical system update to flash on all channels:")
            if st.button("Broadcast Priority System Update Alert Everywhere"):
                if alert_msg.strip():
                    st.session_state["global_alerts"].append(alert_msg.strip())
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.success("✔ Notification broadcast injected into global system array frames.")

        with adm_t4:
            st.subheader("📢 Process Suggestion Logs")
            for idx, log in enumerate(st.session_state["suggestions"]):
                st.markdown(f"**From Student:** {log['user']} | **Content:** {log['text']}")
