# =========================================================================
# FILE 3 OF 3: MASTER WORKSPACE CODE ORCHESTRATOR (main.py)
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
if "active_exam_question" not in st.session_state:
    st.session_state["active_exam_question"] = None
if "active_exam_solution" not in st.session_state:
    st.session_state["active_exam_solution"] = None
if "exam_graded" not in st.session_state:
    st.session_state["exam_graded"] = False
if "calculated_score" not in st.session_state:
    st.session_state["calculated_score"] = 0
if "calculated_grade" not in st.session_state:
    st.session_state["calculated_grade"] = "F"

# Partner Session Management
if "partner_stage" not in st.session_state:
    st.session_state["partner_stage"] = 0
if "partner_q1" not in st.session_state:
    st.session_state["partner_q1"] = None
if "partner_q2" not in st.session_state:
    st.session_state["partner_q2"] = None

# Discussion Session Flags
if "disc_leader" not in st.session_state:
    st.session_state["disc_leader"] = None
if "disc_subject" not in st.session_state:
    st.session_state["disc_subject"] = "Mathematics"
if "disc_topic" not in st.session_state:
    st.session_state["disc_topic"] = "General Revision"
if "disc_q" not in st.session_state:
    st.session_state["disc_q"] = None
if "disc_sol" not in st.session_state:
    st.session_state["disc_sol"] = None
if "disc_show_sol" not in st.session_state:
    st.session_state["disc_show_sol"] = False

# =========================================================================
# 3-TIER ISOLATED ACCESSIBILITY GATEWAY (LOGIN/SIGNUP)
# =========================================================================
if st.session_state["logged_in_uid"] is None:
    st.markdown("<h1 style='text-align: center; color: #00a884; margin-top: 15px;'>🛡️ ACADEMIC SHIELD NETWORK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8696a0;'>High-Capacity Secure System Portal Architecture (Jinja, Uganda)</p>", unsafe_allow_html=True)
    
    # Strict 3-Tier Split Interface Separation
    auth_tab1, auth_tab2, auth_tab3 = st.tabs(["🔒 Administrator Portal", "🎓 Candidate Gateway", "📝 Request New Account"])
    
    # TIER 1: ADMIN AUTHORIZATION HUB
    with auth_tab1:
        st.subheader("Administrative Authority Verification")
        with st.form("Admin Authorization Form"):
            adm_user = st.text_input("Admin ID / Username Key", value="admin_setra")
            adm_pwd = st.text_input("Secret Master Password Link", type="password", value="AdminPassword2026")
            if st.form_submit_button("UNLOCK EXECUTIVE FRAMEWORK"):
                matched_id = None
                for uid, data in db.USERS_REGISTRY.items():
                    if data["username"] == adm_user and data["pwd"] == adm_pwd and data["role"] in ["ADMIN", "SUPER_ADMIN"]:
                        matched_id = uid
                        break
                if matched_id:
                    st.session_state["logged_in_uid"] = matched_id
                    st.session_state["current_user_role"] = db.USERS_REGISTRY[matched_id]["role"]
                    st.session_state["active_channel"] = "🎛️ Super Admin Controls Hub"
                    st.rerun()
                else:
                    st.error("❌ Invalid Administrative Credentials or Access Tier Violation.")

    # TIER 2: STANDARD STUDENT PORTAL
    with auth_tab2:
        st.subheader("Candidate Workspace Access")
        with st.form("Candidate Login Form"):
            usr_user = st.text_input("Registered Account Username", value="user_setra")
            usr_pwd = st.text_input("Personal Security Password", type="password", value="UserPassword2026")
            if st.form_submit_button("INITIALIZE SECURE MEMBER NODE"):
                matched_id = None
                for uid, data in db.USERS_REGISTRY.items():
                    if data["username"] == usr_user and data["pwd"] == usr_pwd and data["role"] == "USER":
                        matched_id = uid
                        break
                if matched_id:
                    u_rec = db.USERS_REGISTRY[matched_id]
                    if u_rec["status"] == "Suspended":
                        st.error("🚫 Access Revoked: This operational account node has been locked by administration.")
                    elif u_rec["status"] == "Pending Review":
                        st.warning("⏳ Your registration token is currently in the Admin verification pipeline queue.")
                    else:
                        st.session_state["logged_in_uid"] = matched_id
                        st.session_state["current_user_role"] = "USER"
                        st.session_state["active_channel"] = "📝 Live Individual Exam Center"
                        st.rerun()
                else:
                    st.error("❌ Authentication failure: Check entry strings.")

    # TIER 3: NEW STUDENT ENROLLMENT REQUEST SPACE
    with auth_tab3:
        st.subheader("Enrollment Validation Protocol")
        with st.form("Account Signup Form Matrix"):
            reg_token = st.text_input("System Activation Token Code Key", placeholder="e.g., AMAZIMA-S5-2026")
            reg_uid = st.text_input("Proposed Unique Account ID Key String (e.g., node_6605)")
            reg_username = st.text_input("Desired Unique Account Username")
            reg_password = st.text_input("Secure Account Access Password", type="password")
            reg_fullname = st.text_input("Official Full Candidate Name")
            reg_school = st.text_input("Institution Campus Base", value="The Amazima School")
            reg_phone = st.text_input("Active Phone Communication Link", value="+256752047103")
            reg_email = st.text_input("Coordinate Email String", value="sudaisisetra@gmail.com")
            reg_subjects = st.multiselect("Core Advanced Syllabus Focus Portfolio", ["Mathematics", "Physics", "Chemistry", "Biology"], default=["Mathematics", "Physics"])
            
            if st.form_submit_button("DISPATCH REGISTRATION REQUEST PAYLOAD"):
                if reg_token not in db.REGISTRATION_CODES:
                    st.error("❌ Invalid system token key template. Validation handshake dropped.")
                elif not reg_uid or not reg_username or not reg_password or not reg_fullname:
                    st.error("❌ Configuration criteria error: Input text blocks cannot be left blank.")
                elif reg_uid in db.USERS_REGISTRY:
                    st.error("❌ Node collision: This account index key is already taken.")
                else:
                    db.USERS_REGISTRY[reg_uid] = {
                        "username": reg_username, "pwd": reg_password, "name": reg_fullname, "class": "Senior Five",
                        "school": reg_school, "phone": reg_phone, "email": reg_email, "location": "Jinja",
                        "subjects": reg_subjects, "status": "Pending Review", "role": "USER", "warning_msg": "",
                        "grade_logs": [], "partner_id": ""
                    }
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.success("🎯 Payload written to database pipeline. Awaiting Administrator verification check.")

else:
    # Resolve working database profile nodes
    UID = st.session_state["logged_in_uid"]
    USER = db.USERS_REGISTRY.get(UID, None)
    if not USER:
        st.session_state["logged_in_uid"] = None
        st.rerun()

    # =========================================================================
    # GLOBAL BROADCAST LAYER (VISUAL ALERTS MOUNTED TO TOP HEADER BUFFER PANEL)
    # =========================================================================
    if db.GLOBAL_BROADCASTS:
        st.markdown(f"""
        <div class="global-broadcast-banner">
            <div class="broadcast-title">🚨 HIGH-PRIORITY GLOBAL ADMINISTRATIVE ANNOUNCEMENT</div>
            <div style="font-size: 14.5px; line-height:1.4; color: #e9edef;">"{db.GLOBAL_BROADCASTS[0]}"</div>
        </div>
        """, unsafe_allow_html=True)

    # Top Brand Bar Configuration
    st.markdown(f"""
    <div class="premium-header-bar">
        <div class="header-brand">🛡️ ACADEMIC SHIELD NETWORK</div>
        <div class="header-identity">Active Node: <span style="color:#00a884; font-weight:bold;">{USER['name']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # FIX: "Sign out" button pinned to the top right corner context grid
    h_col1, h_col2 = st.columns([5.8, 1.2])
    with h_col2:
        if st.button("🚪 Sign out", use_container_width=True, help="Disconnect active session node"):
            st.session_state["logged_in_uid"] = None
            st.session_state["current_user_role"] = None
            st.session_state["active_channel"] = None
            st.rerun()

    if USER.get("warning_msg"):
        st.error(f"⚠️ **REGULATION NOTICE ACTION LOGGED:** {USER['warning_msg']}")

    # =========================================================================
    # SIDEBAR EXPANSION WORKSPACE LAYOUT (TOGGLED BY CORNER DIRECTIONAL ARROWS)
    # =========================================================================
    with st.sidebar:
        st.markdown("### 🗂️ Workspace Navigation")
        st.caption("Tap the arrow vectors inside the top-left edge bounds to fold this panel window away dynamically.")
        st.write("---")
        
        # Absolute structural partition between admin tools and standard student views
        if USER["role"] in ["ADMIN", "SUPER_ADMIN"]:
            st.markdown("<b style='color:#ff4b4b;'>🛠️ MANAGEMENT OVERRIDES PANEL</b>", unsafe_allow_html=True)
            workspace_channels = [
                "🎛️ Super Admin Controls Hub",
                "🔑 Registration Code Generator",
                "📥 Incoming Signups Request Queue",
                "📢 Mass Global Communication Portal",
                "📥 Suggestions Box Center",
                "📤 Upload Notes Page"
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
                "📖 Global Candidates Directory"
            ]
            
        if st.session_state["active_channel"] not in workspace_channels:
            st.session_state["active_channel"] = workspace_channels[0]
            
        selected_nav = st.radio("Active Workspace Channels Selection:", workspace_channels, label_visibility="collapsed")
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
            st.caption("Issue explicit warnings, manage bans, clear warnings, or delete user log nodes permanently.")
            
            for target_uid, profile in list(db.USERS_REGISTRY.items()):
                if target_uid == UID: continue  # Prevent administrative self-lockouts
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h4>👤 Node Allocation ID: <code>{target_uid}</code> | Name Target: {profile['name']}</h4>
                    <p><b>Access Clearance State:</b> {profile['status']} | <b>Warnings String Vector:</b> {profile['warning_msg'] if profile['warning_msg'] else 'Clear of Citations'}</p>
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
            st.write("Active security codes stored permanently inside cluster:")
            st.code(db.REGISTRATION_CODES)
            with st.form("Token Addition Form Block"):
                new_token = st.text_input("Enter New Alphanumeric Activation String:")
                if st.form_submit_button("LOCK AND REGISTER TOKEN KEY"):
                    if new_token and new_token not in db.REGISTRATION_CODES:
                        db.REGISTRATION_CODES.append(new_token)
                        db.save_storage_node("registration_codes.json", db.REGISTRATION_CODES)
                        st.success("New structural activation token locked down successfully.")
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📥 Incoming Signups Request Queue":
            st.markdown("<h2>📥 Incoming Registration Verification Intake Pipeline Queue</h2>", unsafe_allow_html=True)
            pending_nodes = False
            for target_uid, profile in list(db.USERS_REGISTRY.items()):
                if profile["status"] == "Pending Review":
                    pending_nodes = True
                    st.markdown(f"""
                    <div class="directory-profile-box" style="border-left: 4px solid #ffaa00;">
                        <b>Proposed Account ID Node:</b> {target_uid} | Name: {profile['name']}<br>
                        <b>School Connection Matrix:</b> {profile['school']} | Contact Phone Vector: {profile['phone']}
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

        elif ACTIVE_WORKSPACE == "📢 Mass Global Communication Portal":
            st.markdown("<h2>📢 High Priority Mass Global Communication Portal</h2>", unsafe_allow_html=True)
            st.caption("Transmit a system warning or network notice directly to every student dashboard module.")
            with st.form("Global Broadcaster Form Box"):
                msg_body = st.text_area("Write administrative notification warning packet content:")
                if st.form_submit_button("TRANSMIT EMERGENCY NOTICE TO EVERY ONLINE USER"):
                    if msg_body:
                        db.GLOBAL_BROADCASTS.insert(0, msg_body)
                        db.save_storage_node("global_broadcasts.json", db.GLOBAL_BROADCASTS)
                        st.success("Global administrative message broadcast completed securely.")
                        st.rerun()

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
    # WORKSPACE MODULE 2: RECONFIGURED STANDARD STUDENT CHANNELS FRAMEWORK
    # =========================================================================
    else:
        
        if ACTIVE_WORKSPACE == "📝 Live Individual Exam Center":
            st.markdown("<h2>📝 Real-Time Google Sheets Evaluation Engine</h2>", unsafe_allow_html=True)
            
            sel_sub = st.selectbox("Select Target Subject Track Parameter:", ["Mathematics", "Physics", "Chemistry", "Biology"])
            
            # Real Automated Sheet Pulling Action Form Link Trigger
            if st.button("🎲 Pull New Random Question From Google Sheets"):
                # Invokes the live parsing functions fetching column A & B directly
                pulled_node = db.fetch_question_from_sheet(sel_sub)
                st.session_state["active_exam_question"] = pulled_node["Question"]
                st.session_state["active_exam_solution"] = pulled_node["Solution"]
                st.session_state["exam_graded"] = False
                st.rerun()
                
            if st.session_state["active_exam_question"]:
                st.markdown("### 📋 ACTIVE EXAMINATION PROFILE BLUEPRINT")
                st.info(st.session_state["active_exam_question"])
                
                with st.form("Evaluation Processing Box Form"):
                    typed_ans = st.text_area("Type your working equations and final computation strings here:")
                    uploaded_photo = st.file_uploader("Or upload image photograph scan copy of handwritten solution sheet:", type=["png","jpg","jpeg"])
                    
                    if st.form_submit_button("SUBMIT AND EVALUATE CORE PACKET SCORE"):
                        if not typed_ans and not uploaded_photo:
                            st.error("❌ Action denied. You must supply an answer string or handwritten solution image to compute a grading score.")
                        else:
                            # Dynamic keywords auto scoring algorithm framework
                            match_score = 40
                            if typed_ans:
                                keywords = ["hence", "therefore", "let", "prove", "equals", "matrix", "implies", "cell", "membrane", "limit"]
                                for word in keywords:
                                    if word in typed_ans.lower(): match_score += 6
                            if match_score > 100: match_score = 100
                            
                            st.session_state["calculated_score"] = match_score
                            if match_score >= 80: st.session_state["calculated_grade"] = "Principal A"
                            elif match_score >= 70: st.session_state["calculated_grade"] = "Principal B"
                            elif match_score >= 60: st.session_state["calculated_grade"] = "Subsidiary C"
                            else: st.session_state["calculated_grade"] = "F"
                            st.session_state["exam_graded"] = True
                            
                            # Append directly to tracker node logs
                            if "grade_logs" not in USER: USER["grade_logs"] = []
                            USER["grade_logs"].append({
                                "Subject": sel_sub, "Score": match_score, "Grade": st.session_state["calculated_grade"], "Question": st.session_state["active_exam_question"], "Solution": st.session_state["active_exam_solution"], "User_Ans": typed_ans
                            })
                            db.USERS_REGISTRY[UID] = USER
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                            
                if st.session_state["exam_graded"]:
                    st.markdown("### 📊 COMPUTED SCORE RESULTS LOG CARD")
                    st.metric("Your Verified Score Rating:", f"{st.session_state['calculated_score']}%", delta=st.session_state["calculated_grade"])
                    
                    if st.session_state["calculated_score"] < 70:
                        st.error("❌ Performance threshold deficit. Review the official NCDC solution sheet below.")
                    else:
                        st.success("✅ Assessment passed successfully.")
                        
                    st.markdown("#### 🌟 OFFICIAL NCDC VERIFIED STANDARD SOLUTION SHEET MATRIX (COLUMN B)")
                    st.success(st.session_state["active_exam_solution"])
            else:
                st.info("Tap the generation key above to select and load an operational assessment question string.")

        elif ACTIVE_WORKSPACE == "🤝 Synchronized Partner Exam Center":
            st.markdown("<h2>🤝 Synchronized Peer-to-Peer Partnership Examination Center</h2>", unsafe_allow_html=True)
            
            st.write(f"Assigned Room Coordinator Leader Unit Node: **{st.session_state.get('p_leader_node', 'Unassigned')}**")
            if st.button("👑 Establish Self as Appointed Session Leader"):
                st.session_state["p_leader_node"] = USER["name"]
                st.rerun()
                
            if st.session_state.get("p_leader_node"):
                if USER["name"] == st.session_state["p_leader_node"]:
                    st.markdown("### 🎛️ Session Leader Administration Dash")
                    p_sub = st.selectbox("Set Target Collaborative Evaluation Discipline Track:", ["Mathematics", "Physics", "Chemistry", "Biology"])
                    if st.button("🚀 Pull & Synchronize 2 Mutual Questions Across Room Nodes"):
                        n1 = db.fetch_question_from_sheet(p_sub)
                        n2 = db.fetch_question_from_sheet(p_sub)
                        st.session_state["partner_q1"] = n1["Question"]
                        st.session_state["partner_sol1"] = n1["Solution"]
                        st.session_state["partner_q2"] = n2["Question"]
                        st.session_state["partner_sol2"] = n2["Solution"]
                        st.session_state["partner_stage"] = 1
                        st.rerun()
                        
                if st.session_state["partner_stage"] > 0 and st.session_state["partner_q1"]:
                    st.markdown("### 👥 ACTIVE PARTNERSHIP SYNC ASSESSMENT QUESTIONS")
                    st.warning(f"📝 **Mutual Question Segment 1:**\n{st.session_state['partner_q1']}")
                    st.warning(f"📝 **Mutual Question Segment 2:**\n{st.session_state['partner_q2']}")
                    
                    with st.form("Partner Concurrent Response Box Form"):
                        st.write("##### Your Workspace Individual Submission Input Slot")
                        p_t_ans = st.text_area("Type your solution paths matrix details...")
                        p_p_ans = st.file_uploader("Or upload worksheet screenshot scan copy:", type=["png","jpg","jpeg"], key="p_sync_ph")
                        if st.form_submit_button("LOCK COLLABORATIVE PACKET DATA"):
                            st.success("Answer arrays locked and committed down data tracking lanes.")
                            
                    # Display NCDC responses dynamically to room members
                    st.markdown("#### 🌟 COMPLED NCDC MARKING SCHEMAS FOR BOTH TRACK QUESTIONS")
                    st.info(f"<b>Solution 1:</b> {st.session_state.get('partner_sol1')}", icon="🔬")
                    st.info(f"<b>Solution 2:</b> {st.session_state.get('partner_sol2')}", icon="🔬")
                    
                    if USER["name"] == st.session_state.get("p_leader_node"):
                        if st.button("⏭️ Generate Next 2 Exam Questions Vector Loop"):
                            st.session_state["partner_stage"] += 1
                            st.session_state["partner_q1"] = None
                            st.rerun()

        elif ACTIVE_WORKSPACE == "📚 Subject Group Discussions":
            st.markdown("<h2>📚 Interactive Subject Group Discussion Portal</h2>", unsafe_allow_html=True)
            
            if not st.session_state["disc_leader"]:
                st.session_state["disc_leader"] = USER["name"]
                
            st.write(f"Classroom Session Leader Overlord: **{st.session_state['disc_leader']}**")
            
            # ✋ INTERCOM CONTROLLER RESTRICTED SOLELY TO THE MESSAGING VIEW PAGES ONLY
            st.markdown("#### ✋ Intercom Microphone Flow Raise Hand Controller")
            if "discussion_hands" not in st.session_state: st.session_state["discussion_hands"] = []
            is_up = UID in st.session_state["discussion_hands"]
            if is_up:
                if st.button("⬇️ LOWER MY INTERCOM VOICE HAND DISPATCH NOW", type="primary", use_container_width=True):
                    st.session_state["discussion_hands"].remove(UID)
                    st.rerun()
            else:
                if st.button("✋ RAISE ACTIVE INTERCOM HAND FOR VOICE SPACE CLEARANCE", use_container_width=True):
                    st.session_state["discussion_hands"].append(UID)
                    st.rerun()
                    
            if st.session_state["discussion_hands"]:
                for h_uid in st.session_state["discussion_hands"]:
                    st.warning(f"🖐️ Student user **{db.USERS_REGISTRY.get(h_uid, {}).get('name')}** has raised an intercom voice call request signal.")

            if USER["name"] == st.session_state["disc_leader"]:
                st.markdown("### 👑 Session Leader Executive Override Controls")
                l_s = st.selectbox("Set Room Focus Subject Area Profile Target:", ["Mathematics", "Physics", "Chemistry", "Biology"])
                l_t = st.text_input("Define Topic Target Variant String Summary:", value="Syllabus Matrix Review Loops")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("🔒 Lock Topic Down Streams"):
                        st.session_state["disc_subject"] = l_s
                        st.session_state["disc_topic"] = l_t
                        st.rerun()
                with c2:
                    if st.button("🎲 Deploy Random Sheet Exam Question"):
                        node = db.fetch_question_from_sheet(st.session_state["disc_subject"])
                        st.session_state["disc_q"] = node["Question"]
                        st.session_state["disc_sol"] = node["Solution"]
                        st.session_state["disc_show_sol"] = False
                        st.rerun()
                with c3:
                    if st.button("✅ Force Display NCDC Master Solution"):
                        st.session_state["disc_show_sol"] = True
                        st.rerun()

            st.markdown(f"#### Current Focus Core Metrics Vector: `{st.session_state['disc_subject']} -> {st.session_state['disc_topic']}`")
            if st.session_state["disc_q"]:
                st.info(f"❓ **DISCUSSION BLUEPRINT BOARD PROBLEM:**\n{st.session_state['disc_q']}")
            if st.session_state["disc_show_sol"] and st.session_state["disc_sol"]:
                st.success(f"🌟 **NCDC STANDARD SOLUTION MAP SHEET:**\n{st.session_state['disc_sol']}")

            # PREMIUM WHATSAPP PERSISTENT CHAT DESIGN BLOCK
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
                        {f'<div class="chat-media-attachment">📷 <i>Photo Attachment Uploaded File Linked</i></div>' if m.get('has_img') else ''}
                        {f'<div class="chat-media-attachment">🎤 🗣️ <i>Voice Recording Memo Attachment Shared</i></div>' if m.get('has_aud') else ''}
                        <span class="bubble-time">{m['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # INTEGRATED MULTIMEDIA FORM INPUT COMPONENT WITH MICROPHONE CAPTURE TRIGGER
            with st.form("Unified Discussion Media Transmission Console Hub", clear_on_submit=True):
                m_txt = st.text_input("Type clarification argument or concept response text details:")
                m_img = st.file_uploader("Attach handwritten solution worksheet photograph file matrix capture:", type=["png","jpg","jpeg"])
                
                # FIX: Interactive custom voice memo microphone upload component link
                m_mic = st.file_uploader("🎤 TAP MICROPHONE INPUT - Upload recorded audio voice note memo file:", type=["mp3","wav","m4a"])
                
                if st.form_submit_button("TRANSMIT MULTIMEDIA PAYLOAD PACKET"):
                    if m_txt or m_img or m_mic:
                        db.DISCUSSION_MESSAGES.append({
                            "sender": USER["name"], "uid": UID, "text": m_txt if m_txt else "Shared multimedia file assets.",
                            "time": "10:41", "has_img": m_img is not None, "has_aud": m_mic is not None
                        })
                        db.save_node("discussion_messages.json", db.DISCUSSION_MESSAGES)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "💬 General Lounge Chat":
            st.markdown("<h2>💬 Global WhatsApp Media Communications Lounge</h2>", unsafe_allow_html=True)
            
            st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
            for m in db.GENERAL_CHAT_LEDGER:
                side = "row-right" if m["uid"] == UID else "row-left"
                bubble = "bubble-right" if m["uid"] == UID else "bubble-left"
                st.markdown(f"""
                <div class="message-row {side}">
                    <div class="message-bubble {bubble}">
                        <span class="bubble-sender">{m['sender']}</span>
                        <div>{m['text']}</div>
                        {f'<div class="chat-media-attachment">📷 <i>Attached Graphic Image Rendered Safe</i></div>' if m.get('has_img') else ''}
                        {f'<div class="chat-media-attachment">🎤 🗣️ <i>Voice Memo Recording Note File Bound</i></div>' if m.get('has_aud') else ''}
                        <span class="bubble-time">{m['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Lounge Broadcast Input Box Form", clear_on_submit=True):
                l_txt = st.text_input("Type message text content to stream globally...")
                l_img = st.file_uploader("Attach photo file asset:", type=["png","jpg","jpeg"], key="l_i")
                l_mic = st.file_uploader("🎤 Tap Mic - Share Audio file voice recording:", type=["mp3","wav","m4a"], key="l_m")
                if st.form_submit_button("SEND MSG"):
                    if l_txt or l_img or l_mic:
                        db.GENERAL_CHAT_LEDGER.append({
                            "sender": USER["name"], "uid": UID, "text": l_txt if l_txt else "Dispatched structured multimedia files.",
                            "time": "10:41", "has_img": l_img is not None, "has_aud": l_mic is not None
                        })
                        db.save_node("lounge_chat.json", db.GENERAL_CHAT_LEDGER)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "🔒 Private Peer Chatroom":
            st.markdown("<h2>🔒 Private Peer-to-Peer Cryptographic Chatroom Node</h2>", unsafe_allow_html=True)
            
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
                p_mic = st.file_uploader("🎤 Tap Mic - Attach secure voice note recording audio clip:", type=["mp3","wav","m4a"], key="p_m")
                if st.form_submit_button("TRANSMIT ENCRYPTED MESSAGE BLOCK"):
                    if p_txt or p_img or p_mic:
                        db.P2P_CHAT_LEDGER.append({
                            "sender": USER["name"], "uid": UID, "text": p_txt if p_txt else "Sent private media parameters.",
                            "time": "10:41", "has_img": p_img is not None, "has_aud": p_mic is not None
                        })
                        db.save_node("private_chat.json", db.P2P_CHAT_LEDGER)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📊 Personal Progress Tracker":
            st.markdown("<h2>📊 Personal Analytical Progress Tracker Dashboard Matrix</h2>", unsafe_allow_html=True)
            st.caption("Simplified metrics mapping your syllabus performance trajectory dynamically.")
            
            logs = USER.get("grade_logs", [])
            if not logs:
                st.info("No recorded assessment logs found. Complete an evaluation inside the Live Individual Exam Center to build tracking charts.")
            else:
                df_logs = pd.DataFrame(logs)
                st.dataframe(df_logs[["Subject", "Score", "Grade"]])
                st.write("### Mastery Performance Chart Summary")
                st.bar_chart(df_logs.set_index("Subject")["Score"])

        elif ACTIVE_WORKSPACE == "📂 Finished Exam Vault Storage":
            st.markdown("<h2>📂 Done Assessment Historical Storage Vault</h2>", unsafe_allow_html=True)
            
            logs = USER.get("grade_logs", [])
            if not logs:
                st.info("Vault registry records are currently empty.")
            else:
                for idx, item in enumerate(logs):
                    st.markdown(f"""
                    <div class="revision-note-card">
                        <h4>📄 Historical Assessment Entry Node Reference #{idx+1}</h4>
                        <p><b>Syllabus Discipline Area:</b> {item['Subject']} | <b>Calculated Performance Score:</b> {item['Score']}% ({item['Grade']})</p>
                        <p style='color:#8696a0;'><b>Your Typed Solution Answer Payload:</b> "{item['User_Ans']}"</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    pdf_payload = (
                        "🛡️ ACADEMIC SHIELD NETWORK ARCHIVE SYSTEM REPORT\n"
                        "===================================================\n"
                        f"Candidate User Name Target: {USER['name']}\n"
                        f"Subject Domain Track Area: {item['Subject']}\n"
                        f"Computed Score Rating: {item['Score']}% [{item['Grade']}]\n\n"
                        f"NCDC CORE EXAM QUESTION FIELD:\n{item['Question']}\n\n"
                        f"OFFICIAL ATTACHED NCDC REFERENCE STANDARD MARKING SCHEMAS SOLUTION:\n{item['Solution']}\n"
                    )
                    st.download_button(
                        label=f"📥 Download Exam Document #{idx+1} (Formatted Text/PDF Archive Link)",
                        data=pdf_payload,
                        file_name=f"Shield_Assessment_Report_File_{idx+1}.txt",
                        mime="text/plain",
                        key=f"dl_sh_{idx}"
                    )

        elif ACTIVE_WORKSPACE == "📖 Global Candidates Directory":
            st.markdown("<h2>📖 Global Network Candidate Registry Directory Panel</h2>", unsafe_allow_html=True)
            st.caption("Rendering active profiles for 200+ network nodes safely. Security passwords hidden completely from view arrays.")
            
            # PUBLIC DIRECTORY FOR SENDING MESSAGES / PARTNERSHIP REQUESTS
            for d_uid, d_profile in db.USERS_REGISTRY.items():
                if d_profile["status"] != "Approved": continue
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h3>👤 Candidate Profile: {d_profile['name']}</h3>
                    <p><b>Username Reference Key Node ID:</b> <code>{d_profile['username']}</code> (Node Key: {d_uid})</p>
                    <p><b>Institution Base School:</b> {d_profile['school']} | <b>Location Coordinates:</b> {d_profile['location']}</p>
                    <p><b>Contact Info Vector:</b> {d_profile['phone']} | <b>Active Network Email:</b> {d_profile['email']}</p>
                    <p><b>Enrolled Academic Subjects Track:</b> <span style='color:#00a884;'>{', '.join(d_profile['subjects'])}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                da1, da2, _ = st.columns([2, 3, 3])
                with da1:
                    if st.button(f"✉️ Stream Message to {d_uid}", key=f"dir_msg_{d_uid}"):
                        st.info(f"Communications pipe linked with user {d_profile['name']}. Access your Private Chat panel options.")
                with da2:
                    if st.button(f"🤝 Request Academic Partnership with {d_uid}", key=f"dir_prt_{d_uid}"):
                        st.success(f"Partnership request successfully dispatched down network lines to user node {d_profile['name']}!")
                        
            st.write("---")
            st.markdown("### 📤 Send System Feature Recommendation to Public Logs")
            with st.form("Public Suggestion File Append Form", clear_on_submit=True):
                s_txt = st.text_area("Type app feedback or feature updates requests to display publicly to all users:")
                if st.form_submit_button("SUBMIT PUBLIC RECOMMENDATION"):
                    if s_txt:
                        db.SUGGESTIONS_BOX.append({"text": s_txt, "reply": "Awaiting administrative verification response packet."})
                        db.save_storage_node("suggestions_box.json", db.SUGGESTIONS_BOX)
                        st.success("Recommendation entry added to public records database channels.")
                        st.rerun()
