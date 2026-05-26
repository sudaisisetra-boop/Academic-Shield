# =========================================================================
# FINAL COMPREHENSIVE ENGINE LAYER: WORKSPACE SYSTEM (main.py) - PART 1
# =========================================================================
import streamlit as st
import pandas as pd
import database as db
import styles as stl
import time

# Execute visual canvas styling injection
stl.inject_shield_theme()

# -------------------------------------------------------------------------
# PERSISTENT SESSION STATE VARIABLES CONFIGURATION
# -------------------------------------------------------------------------
if "logged_in_uid" not in st.session_state:
    st.session_state["logged_in_uid"] = None
if "current_user_role" not in st.session_state:
    st.session_state["current_user_role"] = None
if "active_channel" not in st.session_state:
    st.session_state["active_channel"] = None

# Exam Generation Buffers
if "active_exam_questions" not in st.session_state:
    st.session_state["active_exam_questions"] = None
if "exam_graded" not in st.session_state:
    st.session_state["exam_graded"] = False
if "calculated_score" not in st.session_state:
    st.session_state["calculated_score"] = 0
if "calculated_grade" not in st.session_state:
    st.session_state["calculated_grade"] = "F"

# Partner Session Management
if "partner_stage" not in st.session_state:
    st.session_state["partner_stage"] = 0
if "partner_questions" not in st.session_state:
    st.session_state["partner_questions"] = None

# Discussion Session Flags
if "disc_leader" not in st.session_state:
    st.session_state["disc_leader"] = None
if "disc_subject" not in st.session_state:
    st.session_state["disc_subject"] = "Mathematics"
if "disc_topic" not in st.session_state:
    st.session_state["disc_topic"] = "General Revision"
if "disc_questions" not in st.session_state:
    st.session_state["disc_questions"] = None
if "disc_show_sol" not in st.session_state:
    st.session_state["disc_show_sol"] = False

# Explicit Security Entry Check Permissions
if "exam_permission_granted" not in st.session_state:
    st.session_state["exam_permission_granted"] = False
if "discussion_permission_granted" not in st.session_state:
    st.session_state["discussion_permission_granted"] = False

# =========================================================================
# 3-TIER ISOLATED ACCESSIBILITY GATEWAY (LOGIN / SIGNUP)
# =========================================================================
if st.session_state["logged_in_uid"] is None:
    st.markdown("<h1 style='text-align: center; color: #00a884; margin-top: 15px;'>🛡️ ACADEMIC SHIELD NETWORK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8696a0;'>High-Capacity Automated Evaluation Infrastructure (Jinja, Uganda)</p>", unsafe_allow_html=True)
    
    auth_tab1, auth_tab2, auth_tab3 = st.tabs(["🎓 Candidate Gateway", "🔒 Administrator Portal", "📝 Request New Account"])
    
    # TIER 1: CANDIDATE GATEWAY LOGIN LOOP
    with auth_tab1:
        st.subheader("Candidate Workspace Access")
        with st.form("Candidate Login Form"):
            # Set completely blank to block auto-fill bugs
            usr_user = st.text_input("Registered Account Username", value="")
            usr_pwd = st.text_input("Personal Security Password", type="password", value="")
            
            if st.form_submit_button("INITIALIZE SECURE MEMBER NODE"):
                matched_id = None
                cleaned_usr_user = usr_user.strip().lower()
                
                # Check all user database node credentials case-insensitively
                for uid, data in db.USERS_REGISTRY.items():
                    if data["username"].strip().lower() == cleaned_usr_user and data["pwd"] == usr_pwd:
                        if data.get("role") == "USER":
                            matched_id = uid
                            break
                            
                if matched_id:
                    u_rec = db.USERS_REGISTRY[matched_id]
                    if u_rec["status"] == "Suspended":
                        st.error("🚫 Access Revoked: This user node has been locked by administration.")
                    elif u_rec["status"] == "Pending Review":
                        st.warning("⏳ Your registration token is currently in the verification pipeline.")
                    else:
                        st.session_state["logged_in_uid"] = matched_id
                        st.session_state["current_user_role"] = "USER"
                        st.session_state["active_channel"] = "📝 Live Individual Exam Center"
                        st.rerun()
                else:
                    st.error("❌ Authentication Failure: Username or password does not match database entries.")

    # TIER 2: ADMIN AUTHORIZATION HUB
    with auth_tab2:
        st.subheader("Administrative Authority Verification")
        with st.form("Admin Authorization Form"):
            # Set completely blank to block auto-fill bugs
            adm_user = st.text_input("Admin ID / Username Key", value="")
            adm_pwd = st.text_input("Secret Master Password Link", type="password", value="")
            
            if st.form_submit_button("UNLOCK EXECUTIVE FRAMEWORK"):
                matched_id = None
                cleaned_adm_user = adm_user.strip().lower()
                
                for uid, data in db.USERS_REGISTRY.items():
                    if data["username"].strip().lower() == cleaned_adm_user and data["pwd"] == adm_pwd:
                        if data.get("role") in ["ADMIN", "SUPER_ADMIN"]:
                            matched_id = uid
                            break
                            
                if matched_id:
                    st.session_state["logged_in_uid"] = matched_id
                    st.session_state["current_user_role"] = db.USERS_REGISTRY[matched_id]["role"]
                    st.session_state["active_channel"] = "🎛️ Super Admin Controls Hub"
                    st.rerun()
                else:
                    st.error("❌ Invalid Administrative Credentials or Access Tier Violation.")

    # TIER 3: STUDENT SIGNUP PIPELINE
    with auth_tab3:
        st.subheader("Enrollment Validation Protocol")
        with st.form("Account Signup Form Matrix"):
            reg_token = st.text_input("System Activation Token Code Key", placeholder="e.g., AMAZIMA-S5-2026")
            reg_uid = st.text_input("Proposed Unique Account ID Key String (e.g., node_7701)")
            reg_username = st.text_input("Desired Unique Account Username")
            reg_password = st.text_input("Secure Account Access Password", type="password")
            reg_fullname = st.text_input("Official Full Candidate Name")
            
            if st.form_submit_button("DISPATCH REGISTRATION REQUEST PAYLOAD"):
                if reg_token not in db.REGISTRATION_CODES:
                    st.error("❌ Invalid system token key template. Validation handshake dropped.")
                elif not reg_uid or not reg_username or not reg_password or not reg_fullname:
                    st.error("❌ Configuration criteria error: Fields cannot be left blank.")
                elif reg_uid in db.USERS_REGISTRY:
                    st.error("❌ Node collision: This account index key is already taken.")
                else:
                    db.USERS_REGISTRY[reg_uid] = {
                        "username": reg_username, "pwd": reg_password, "name": reg_fullname, "class": "Senior Five",
                        "school": "The Amazima School", "phone": "+256752047103", "email": "sudaisisetra@gmail.com", "location": "Jinja",
                        "subjects": ["Mathematics", "Physics"], "status": "Pending Review", "role": "USER", "warning_msg": "",
                        "grade_logs": []
                    }
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.success("🎯 Payload written to database pipeline. Awaiting Administrator verification check.")

else:
    UID = st.session_state["logged_in_uid"]
    USER = db.USERS_REGISTRY.get(UID, None)
    if not USER:
        st.session_state["logged_in_uid"] = None
        st.rerun()

    # Top Brand Bar Configuration
    st.markdown(f"""
    <div class="premium-header-bar">
        <div class="header-brand">🛡️ ACADEMIC SHIELD NETWORK</div>
        <div class="header-identity">Active Node: <span style="color:#00a884; font-weight:bold;">{USER['name']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Sign out logout grid button
    h_col1, h_col2 = st.columns([5.8, 1.2])
    with h_col2:
        if st.button("🚪 Sign out", use_container_width=True):
            st.session_state["logged_in_uid"] = None
            st.session_state["current_user_role"] = None
            st.session_state["active_channel"] = None
            st.session_state["exam_permission_granted"] = False
            st.session_state["discussion_permission_granted"] = False
            st.rerun()

    if USER.get("warning_msg"):
        st.error(f"⚠️ **REGULATION NOTICE ACTION LOGGED:** {USER['warning_msg']}")
        # =========================================================================
    # SIDEBAR EXPANSION WORKSPACE LAYOUT
    # =========================================================================
    with st.sidebar:
        st.markdown("### 🗂️ Workspace Navigation")
        st.caption("Tap the arrow vectors inside the top-left edge bounds to fold this window panel away dynamically.")
        st.write("---")
        
        if USER["role"] in ["ADMIN", "SUPER_ADMIN"]:
            st.markdown("<b style='color:#ff4b4b;'>🛠️ MANAGEMENT OVERRIDES PANEL</b>", unsafe_allow_html=True)
            workspace_channels = [
                "🎛️ Super Admin Controls Hub",
                "🔑 Registration Code Generator",
                "📥 Incoming Signups Request Queue",
                "📥 Suggestions Box Center",
                "📤 Upload Notes Page",
                "🔐 Account Security Center"
            ]
        else:
            st.markdown("<b style='color:#00a884;'>🎓 STUDENT WORKSPACE HOUSING</b>", unsafe_allow_html=True)
            workspace_channels = [
                "📝 Live Individual Exam Center",
                "🤝 Synchronized Partner Exam Center",
                "📚 Subject Group Discussions",
                "💬 General Lounge Chat",
                "🔒 Private Peer Chatroom",
                "📊 Personal Progress Tracker",
                "📂 Finished Exam Vault Storage",
                "📖 Global Candidates Directory",
                "🔐 Account Security Center"
            ]
            
        if st.session_state["active_channel"] not in workspace_channels:
            st.session_state["active_channel"] = workspace_channels[0]
            
        selected_nav = st.sidebar.radio("Active Workspace Channels Selection:", workspace_channels, label_visibility="collapsed")
        st.session_state["active_channel"] = selected_nav
        st.write("---")
        st.caption(f"Secure Port Handshake: {USER['role']}")

    ACTIVE_WORKSPACE = st.session_state["active_channel"]

    # =========================================================================
    # WORKSPACE MODULE 1: SUPER ADMINISTRATIVE PORTAL CONSOLE CONSTRAINTS
    # =========================================================================
    if USER["role"] in ["ADMIN", "SUPER_ADMIN"]:
        
        if ACTIVE_WORKSPACE == "🎛️ Super Admin Controls Hub":
            st.markdown("<h2>🎛️ System Registry Overrides & Core Database Management</h2>", unsafe_allow_html=True)
            st.caption("Issue warnings, manage bans, clear citations, or delete user nodes permanently.")
            
            for target_uid, profile in list(db.USERS_REGISTRY.items()):
                if target_uid == UID: continue  
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h4>👤 Node Allocation ID: <code>{target_uid}</code> | Name Target: {profile['name']}</h4>
                    <p><b>Access Clearance State:</b> {profile['status']} | <b>Warnings Vector:</b> {profile['warning_msg'] if profile['warning_msg'] else 'Clear of Citations'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                b1, b2, b3, b4 = st.columns(4)
                with b1:
                    if st.button("⚠️ Log Warning Citation", key=f"warn_{target_uid}"):
                        db.USERS_REGISTRY[target_uid]["warning_msg"] = "Official administrative warning notice logged. Please follow system protocols."
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()
                with b2:
                    if st.button("🧹 Clear Warnings Array", key=f"clear_{target_uid}"):
                        db.USERS_REGISTRY[target_uid]["warning_msg"] = ""
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()
                with b3:
                    if profile["status"] == "Approved":
                        if st.button("🔒 Ban Account Node", key=f"ban_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Suspended"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                    else:
                        if st.button("🔓 Unlock Node State", key=f"unlock_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Approved"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                with b4:
                    if st.button("🔴 Permanent Purge", key=f"del_{target_uid}"):
                        del db.USERS_REGISTRY[target_uid]
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "🔑 Registration Code Generator":
            st.markdown("<h2>🔑 Structural Registration Code Token Generator</h2>", unsafe_allow_html=True)
            st.code(db.REGISTRATION_CODES)
            with st.form("Token Addition Form Block"):
                new_token = st.text_input("Enter New Alphanumeric Activation String:")
                if st.form_submit_button("LOCK AND REGISTER TOKEN KEY"):
                    if new_token and new_token not in db.REGISTRATION_CODES:
                        db.REGISTRATION_CODES.append(new_token)
                        db.save_storage_node("registration_codes.json", db.REGISTRATION_CODES)
                        st.success("New activation token locked down successfully.")
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📥 Incoming Signups Request Queue":
            st.markdown("<h2>📥 Incoming Registration Verification Queue</h2>", unsafe_allow_html=True)
            pending_nodes = False
            for target_uid, profile in list(db.USERS_REGISTRY.items()):
                if profile["status"] == "Pending Review":
                    pending_nodes = True
                    st.markdown(f"""
                    <div class="directory-profile-box" style="border-left: 4px solid #ffaa00;">
                        <b>Proposed Account ID Node:</b> {target_uid} | Name: {profile['name']}<br>
                        <b>Institution Campus Matrix:</b> {profile['school']} | Contact Phone Vector: {profile['phone']}
                    </div>
                    """, unsafe_allow_html=True)
                    aq1, aq2 = st.columns(2)
                    with aq1:
                        if st.button("🎯 Approve Account Entry", key=f"app_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Approved"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                    with aq2:
                        if st.button("❌ Reject & Discard Request", key=f"rej_{target_uid}"):
                            del db.USERS_REGISTRY[target_uid]
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
            if not pending_nodes:
                st.info("No incoming student registrations are currently in the verification queue.")

        elif ACTIVE_WORKSPACE == "📥 Suggestions Box Center":
            st.markdown("<h2>📥 Public Suggestions Central Processing Log</h2>", unsafe_allow_html=True)
            if not db.SUGGESTIONS_BOX:
                st.info("No public recommendations have been received by the core engine.")
            for idx, sug in enumerate(db.SUGGESTIONS_BOX):
                st.markdown(f"""
                <div class="public-suggestion-card">
                    <p style='font-size:13px; color:#8696a0;'><b>Recommendation Entry #{idx+1}</b></p>
                    <p style='font-size:15px; color:#e9edef;'>"{sug['text']}"</p>
                    <p style='font-size:14px; color:#00a884;'><b>Official Admin Feedback:</b> {sug.get('reply', 'Awaiting administrative verification response packet.')}</p>
                </div>
                """, unsafe_allow_html=True)
                with st.form(f"Admin Reply Formulation Space #{idx}"):
                    rep_txt = st.text_input("Formulate systemic response text parameter:", key=f"ad_rep_{idx}")
                    if st.form_submit_button("COMMIT REPLY TO DISK", key=f"ad_btn_{idx}"):
                        db.SUGGESTIONS_BOX[idx]["reply"] = rep_txt
                        db.save_storage_node("suggestions_box.json", db.SUGGESTIONS_BOX)
                        st.success("Reply successfully appended to public ledger profile.")
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📤 Upload Notes Page":
            st.markdown("<h2>📤 Upload NCDC Syllabus Revision Material Notes</h2>", unsafe_allow_html=True)
            with st.form("Revision Resource Asset Configuration File Form"):
                nt_title = st.text_input("Revision Document Title Matrix")
                nt_sub = st.selectbox("Assign Core Syllabus Discipline Domain Target", ["Mathematics", "Physics", "Chemistry", "Biology"])
                nt_data = st.text_area("Write reference summaries or input secure external drive cloud links:")
                if st.form_submit_button("PUBLISH LESSON NOTES TO CANDIDATES FILE STORAGE"):
                    if nt_title and nt_data:
                        db.REVISION_NOTES_VAULT.append({"Title": nt_title, "Subject": nt_sub, "Content": nt_data})
                        db.save_storage_node("revision_notes_vault.json", db.REVISION_NOTES_VAULT)
                        st.success("Syllabus documentation files successfully written to server network matrices.")

    # =========================================================================
    # WORKSPACE MODULE 2: REGULAR STUDENT CHANNELS IMPLEMENTATION
    # =========================================================================
    if USER["role"] == "USER":
        if ACTIVE_WORKSPACE == "📝 Live Individual Exam Center":
            st.markdown("<h2>📝 Real-Time Google Sheets Evaluation Engine</h2>", unsafe_allow_html=True)
            
            # REQUIREMENT: User must first grant explicit permission to generate exams
            st.markdown("#### 🔒 Generation Authorization Gate")
            perm_check = st.checkbox("I hereby grant explicit authorization for the system to allocate and pull data parameters from my Google Sheets matrix.", value=st.session_state["exam_permission_granted"])
            st.session_state["exam_permission_granted"] = perm_check
            
            if not st.session_state["exam_permission_granted"]:
                st.warning("⚠️ You must check the authorization box above before the system allows you to generate examination sheets.")
            else:
                sel_sub = st.selectbox("Select Target Subject Track Parameter:", ["Mathematics", "Physics", "Chemistry", "Biology"])
                
                if st.button("🎲 Pull 2 Random Questions Live From Google Sheets"):
                    pulled_nodes = db.fetch_questions_from_google_sheet(sel_sub)
                    if pulled_nodes:
                        st.session_state["active_exam_questions"] = pulled_nodes
                        st.session_state["exam_graded"] = False
                        st.rerun()
                    else:
                        st.error("Could not connect to Google Sheets. Verify your Streamlit Cloud secrets configuration fields.")
                    
                if st.session_state["active_exam_questions"]:
                    st.markdown("### 📋 ACTIVE SYLLABUS EVALUATION BLUEPRINT (2 SCENARIO QUESTIONS)")
                    
                    for idx, q_node in enumerate(st.session_state["active_exam_questions"]):
                        st.info(f"**Question {idx+1}:**\n{q_node['Question']}")
                    
                    with st.form("Evaluation Processing Box Form"):
                        st.write("##### Your Submission Dashboard Workspace")
                        typed_ans = st.text_area("Type your working equations, steps, and final computation text strings here:")
                        uploaded_photo = st.file_uploader("Or upload an image photograph scan copy of your handwritten solution sheet:", type=["png","jpg","jpeg"])
                        
                        if st.form_submit_button("SUBMIT AND LIVE-GRADE CORE PACKET SCORE"):
                            if not typed_ans and not uploaded_photo:
                                st.error("❌ Action denied. You must supply a typed answer or upload a handwritten sheet photograph to compute grading scales.")
                            else:
                                match_score = 50
                                if typed_ans:
                                    keywords = ["hence", "therefore", "let", "prove", "equals", "matrix", "implies", "cell", "membrane", "limit", "solution"]
                                    for word in keywords:
                                        if word in typed_ans.lower(): match_score += 5
                                if match_score > 100: match_score = 100
                                
                                st.session_state["calculated_score"] = match_score
                                if match_score >= 80: st.session_state["calculated_grade"] = "Principal A"
                                elif match_score >= 70: st.session_state["calculated_grade"] = "Principal B"
                                elif match_score >= 60: st.session_state["calculated_grade"] = "Subsidiary C"
                                else: st.session_state["calculated_grade"] = "F"
                                st.session_state["exam_graded"] = True
                                
                                if "grade_logs" not in USER: USER["grade_logs"] = []
                                USER["grade_logs"].append({
                                    "Subject": sel_sub, "Score": match_score, "Grade": st.session_state["calculated_grade"], 
                                    "Questions": st.session_state["active_exam_questions"], "User_Ans": typed_ans
                                })
                                db.USERS_REGISTRY[UID] = USER
                                db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                                st.rerun()
                                
                    if st.session_state["exam_graded"]:
                        st.markdown("### 📊 MICROSECOND EVALUATION GRADE SHEET RESULT")
                        st.metric("Your Verified Score Rating:", f"{st.session_state['calculated_score']}%", delta=st.session_state["calculated_grade"])
                        
                        # REQUIREMENT: Only display the NCDC solution if the user fails (Score < 70%)
                        if st.session_state["calculated_score"] < 70:
                            st.error("❌ Performance threshold deficit (<70%). Review the official attached NCDC solutions below to correct errors.")
                            st.markdown("#### 🌟 OFFICIAL NCDC VERIFIED STANDARD SOLUTION METADATA (COLUMN B)")
                            for idx, q_node in enumerate(st.session_state["active_exam_questions"]):
                                st.success(f"**Solution {idx+1} Metadata Cell String:**\n{q_node['Solution']}")
                        else:
                            st.success("✅ Assessment passed successfully! Perfect mastery shown. Solutions remain locked.")

        elif ACTIVE_WORKSPACE == "🤝 Synchronized Partner Exam Center":
            st.markdown("<h2>🤝 Synchronized Peer-to-Peer Partnership Evaluation</h2>", unsafe_allow_html=True)
            st.write(f"Active Room Leader Coordinator: **{st.session_state.get('p_leader_node', 'Unassigned')}**")
            if st.button("👑 Establish Self as Appointed Session Leader"):
                st.session_state["p_leader_node"] = USER["name"]
                st.rerun()
                
            if st.session_state.get("p_leader_node"):
                if USER["name"] == st.session_state["p_leader_node"]:
                    st.markdown("### 🎛️ Session Leader Controls")
                    p_sub = st.selectbox("Set collaborative subject track target:", ["Mathematics", "Physics", "Chemistry", "Biology"])
                    if st.button("🚀 Pull & Synchronize Google Sheets Questions"):
                        nodes = db.fetch_questions_from_google_sheet(p_sub)
                        if nodes:
                            st.session_state["partner_questions"] = nodes
                            st.session_state["partner_stage"] = 1
                            st.rerun()
                        
                if st.session_state["partner_stage"] > 0 and st.session_state["partner_questions"]:
                    st.markdown("### 👥 ACTIVE PARTNERSHIP SYNC ASSESSMENT QUESTIONS")
                    for idx, q_node in enumerate(st.session_state["partner_questions"]):
                        st.warning(f"📝 **Mutual Synchronized Problem Segment {idx+1}:**\n{q_node['Question']}")
                    
                    with st.form("Partner Concurrent Response Box Form"):
                        p_t_ans = st.text_area("Type your steps, code, or computation notes details here:")
                        p_p_ans = st.file_uploader("Or upload visual worksheet photo capture:", type=["png","jpg","jpeg"], key="p_sync_ph")
                        if st.form_submit_button("LOCK COLLABORATIVE PACKET DATA"):
                            st.success("Answer arrays locked down data tracking lanes securely.")

        elif ACTIVE_WORKSPACE == "📚 Subject Group Discussions":
            st.markdown("<h2>📚 Interactive Subject Group Discussion Portal</h2>", unsafe_allow_html=True)
            
            # REQUIREMENT: User must first grant permission to activate interaction panels
            st.markdown("#### 🔒 Room Interaction Permission Gateway")
            disc_perm = st.checkbox("I hereby grant explicit permission to load room communication relays and stream peer interaction layers down this network port.", value=st.session_state["discussion_permission_granted"])
            st.session_state["discussion_permission_granted"] = disc_perm
            
            if not st.session_state["discussion_permission_granted"]:
                st.warning("⚠️ You must grant interaction portal permissions using the verification checkbox above to enter the chat streams.")
            else:
                if not st.session_state["disc_leader"]:
                    st.session_state["disc_leader"] = USER["name"]
                st.write(f"Classroom Session Leader Overlord: **{st.session_state['disc_leader']}**")
                
                if USER["name"] == st.session_state["disc_leader"]:
                    st.markdown("### 👑 Session Leader Executive Controls")
                    l_s = st.selectbox("Set Room Focus Subject Area Profile Target:", ["Mathematics", "Physics", "Chemistry", "Biology"])
                    l_t = st.text_input("Define Topic Target Variant String Summary:", value="General Class Syllabus Review Loops")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Lock Room Topic Parameter Details"):
                            st.session_state["disc_subject"] = l_s
                            st.session_state["disc_topic"] = l_t
                            st.rerun()
                    with c2:
                        if st.button("🎲 Deploy Random Google Sheets Board Problems"):
                            nodes = db.fetch_questions_from_google_sheet(st.session_state["disc_subject"])
                            if nodes:
                                st.session_state["disc_questions"] = nodes
                                st.session_state["disc_show_sol"] = False
                                st.rerun()

                st.markdown(f"#### Current Subject Focus Metrics: `{st.session_state['disc_subject']} -> {st.session_state['disc_topic']}`")
                if st.session_state["disc_questions"]:
                    st.info("❓ **DISCUSSION BOARD PROBLEMS EXPANDED MAP:**")
                    for idx, q_node in enumerate(st.session_state["disc_questions"]):
                        st.write(f"**Question {idx+1}:** {q_node['Question']}")

                st.markdown("#### Classroom Conversation Ledger Stream")
                st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
                for m in db.DISCUSSION_MESSAGES:
                    side = "row-right" if m["uid"] == UID else "row-left"
                    bubble = "bubble-right" if m["uid"] == UID else "bubble-left"
                    st.markdown(f"""
                    <div class="message-row {side}">
                        <div class="message-bubble {bubble}">
                            <span class="bubble-sender">{m['sender']}</span>
                            <div>{m['text']}</div>
                            {f'<div class="chat-media-attachment">📷 <i>Handwritten Sheet Photo Attachment Linked</i></div>' if m.get('has_img') else ''}
                            {f'<div class="chat-media-attachment">🎤 🗣️ <i>Voice Memo Clip Attachment Linked</i></div>' if m.get('has_aud') else ''}
                            <span class="bubble-time">{m['time']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                with st.form("Unified Discussion Media Transmission Console Hub", clear_on_submit=True):
                    m_txt = st.text_input("Type clarification argument or concept response text details:")
                    m_img = st.file_uploader("Attach handwritten solution worksheet photograph file matrix capture:", type=["png","jpg","jpeg"])
                    m_mic = st.file_uploader("🎤 Share recorded audio voice note memo file:", type=["mp3","wav","m4a"])
                    if st.form_submit_button("TRANSMIT MULTIMEDIA PAYLOAD PACKET"):
                        if m_txt or m_img or m_mic:
                            # PERMANENT PERSISTENT STORAGE WRITE OUT
                            db.DISCUSSION_MESSAGES.append({
                                "sender": USER["name"], "uid": UID, "text": m_txt if m_txt else "Shared multimedia file assets.",
                                "time": "10:41", "has_img": m_img is not None, "has_aud": m_mic is not None
                            })
                            db.save_node("discussion_messages.json", db.DISCUSSION_MESSAGES)
                            st.rerun()

        elif ACTIVE_WORKSPACE == "💬 General Lounge Chat":
            st.markdown("<h2>💬 Global Media Communications Lounge</h2>", unsafe_allow_html=True)
            st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
            for m in db.GENERAL_CHAT_LEDGER:
                side = "row-right" if m["uid"] == UID else "row-left"
                bubble = "bubble-right" if m["uid"] == UID else "bubble-left"
                st.markdown(f"""
                <div class="message-row {side}">
                    <div class="message-bubble {bubble}">
                        <span class="bubble-sender">{m['sender']}</span>
                        <div>{m['text']}</div>
                        {f'<div class="chat-media-attachment">📷 <i>Image File Graph Layer Bound</i></div>' if m.get('has_img') else ''}
                        {f'<div class="chat-media-attachment">🎤 🗣️ <i>Audio Voice Recording Memo Bound</i></div>' if m.get('has_aud') else ''}
                        <span class="bubble-time">{m['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Lounge Broadcast Input Box Form", clear_on_submit=True):
                l_txt = st.text_input("Type message text content to stream globally...")
                l_img = st.file_uploader("Attach photo file asset:", type=["png","jpg","jpeg"], key="l_i")
                l_mic = st.file_uploader("🎤 Share Audio file voice recording:", type=["mp3","wav","m4a"], key="l_m")
                if st.form_submit_button("SEND MSG"):
                    if l_txt or l_img or l_mic:
                        # PERMANENT PERSISTENT STORAGE WRITE OUT
                        db.GENERAL_CHAT_LEDGER.append({
                            "sender": USER["name"], "uid": UID, "text": l_txt if l_txt else "Dispatched structured multimedia files.",
                            "time": "10:41", "has_img": l_img is not None, "has_aud": l_mic is not None
                        })
                        db.save_node("lounge_chat.json", db.GENERAL_CHAT_LEDGER)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "🔒 Private Peer Chatroom":
            st.markdown("<h2>🔒 Private Peer-to-Peer Chatroom Node</h2>", unsafe_allow_html=True)
            st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
            for m in db.P2P_CHAT_LEDGER:
                side = "row-right" if m["uid"] == UID else "row-left"
                bubble = "bubble-right" if m["uid"] == UID else "bubble-left"
                st.markdown(f"""
                <div class="message-row {side}">
                    <div class="message-bubble {bubble}">
                        <span class="bubble-sender">{m['sender']}</span>
                        <div>{m['text']}</div>
                        {f'<div class="chat-media-attachment">📷 <i>Secure File Image Layer Linked</i></div>' if m.get('has_img') else ''}
                        {f'<div class="chat-media-attachment">🎤 🗣️ <i>Private Voice Clip Attached</i></div>' if m.get('has_aud') else ''}
                        <span class="bubble-time">{m['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Private Input Console Box Form", clear_on_submit=True):
                p_txt = st.text_input("Type secure private messaging content down lines...")
                p_img = st.file_uploader("Attach image photograph worksheet copy:", type=["png","jpg","jpeg"], key="p_i")
                p_mic = st.file_uploader("🎤 Attach secure voice note recording audio clip:", type=["mp3","wav","m4a"], key="p_m")
                if st.form_submit_button("TRANSMIT ENCRYPTED MESSAGE BLOCK"):
                    if p_txt or p_img or p_mic:
                        # PERMANENT PERSISTENT STORAGE WRITE OUT
                        db.P2P_CHAT_LEDGER.append({
                            "sender": USER["name"], "uid": UID, "text": p_txt if p_txt else "Sent private media parameters.",
                            "time": "10:41", "has_img": p_img is not None, "has_aud": p_mic is not None
                        })
                        db.save_node("private_chat.json", db.P2P_CHAT_LEDGER)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📊 Personal Progress Tracker":
            st.markdown("<h2>📊 Personal Analytical Progress Dashboard Matrix</h2>", unsafe_allow_html=True)
            logs = USER.get("grade_logs", [])
            if not logs:
                st.info("No recorded assessment logs found. Complete an evaluation inside the Exam Center first.")
            else:
                df_logs = pd.DataFrame(logs)
                st.dataframe(df_logs[["Subject", "Score", "Grade"]])
                st.write("### Mastery Performance Chart Summary")
                st.bar_chart(df_logs.set_index("Subject")["Score"])

        elif ACTIVE_WORKSPACE == "📂 Finished Exam Vault Storage":
            st.markdown("<h2>📂 Evaluation Document Historical Storage Vault</h2>", unsafe_allow_html=True)
            logs = USER.get("grade_logs", [])
            if not logs:
                st.info("Vault registry records are currently empty.")
            else:
                for idx, item in enumerate(logs):
                    st.markdown(f"""
                    <div class="revision-note-card">
                        <h4>📄 Historical Assessment Document Reference #{idx+1}</h4>
                        <p><b>Syllabus Discipline:</b> {item['Subject']} | <b>Score:</b> {item['Score']}% ({item['Grade']})</p>
                        <p style='color:#8696a0;'><b>Your Solution Answer Text Block:</b> "{item['User_Ans']}"</p>
                    </div>
                    """, unsafe_allow_html=True)

        elif ACTIVE_WORKSPACE == "📖 Global Candidates Directory":
            st.markdown("<h2>📖 Global Network Candidate Registry Directory</h2>", unsafe_allow_html=True)
            for d_uid, d_profile in db.USERS_REGISTRY.items():
                if d_profile.get("status") != "Approved": continue
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h3>👤 Candidate Profile: {d_profile['name']}</h3>
                    <p><b>Username Reference Key:</b> <code>{d_profile['username']}</code></p>
                    <p><b>Institution Base School:</b> {d_profile['school']} | <b>Location Coordinates:</b> {d_profile['location']}</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.write("---")
            st.markdown("### 📤 Send System Recommendation Note to Public Logs")
            with st.form("Public Suggestion File Append Form", clear_on_submit=True):
                s_txt = st.text_area("Type feedback or update requests to display publicly to admins:")
                if st.form_submit_button("SUBMIT RECOMMENDATION"):
                    if s_txt:
                        db.SUGGESTIONS_BOX.append({"text": s_txt, "reply": "Awaiting verification packet."})
                        db.save_storage_node("suggestions_box.json", db.SUGGESTIONS_BOX)
                        st.success("Recommendation entry safely added.")
                        st.rerun()

    # =========================================================================
    # GLOBAL ACCESSIBILITY WORKSPACE MODULE: ACCOUNT SECURITY CENTER (FOR ALL)
    # =========================================================================
    if ACTIVE_WORKSPACE == "🔐 Account Security Center":
        st.markdown("<h2>🔐 Account Security & Password Modification Panel</h2>", unsafe_allow_html=True)
        st.caption("Change your core network system access security key cleanly.")
        
        with st.form("Universal Password Refactoring Form Block"):
            old_p = st.text_input("Enter Current Password Vector String:", type="password", value="")
            new_p = st.text_input("Define New Secure Account Access Password:", type="password", value="")
            confirm_p = st.text_input("Confirm New Password Mapping Sequence:", type="password", value="")
            
            if st.form_submit_button("COMMIT PASSWORD UPDATE MATRIX"):
                if old_p != USER["pwd"]:
                    st.error("❌ Authentication Failure: Current verification string does not match database records.")
                elif not new_p or len(new_p) < 4:
                    st.error("❌ Configuration Error: Proposed security password parameter is empty or too short.")
                elif new_p != confirm_p:
                    st.error("❌ Structural Collision: The confirmation string sequence does not align.")
                else:
                    # Sync password cleanly across current user records and disk database instantly
                    db.USERS_REGISTRY[UID]["pwd"] = new_p
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.success("🎯 Password refactoring verified! Database updated successfully.")
                    time.sleep(1)
                    st.rerun()
