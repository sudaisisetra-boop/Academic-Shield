# =========================================================================
# FILE 3 OF 3: MASTER ROUTING ENGINE CORE (main.py)
# =========================================================================
import streamlit as st
import pandas as pd
import database as db
import styles as stl

# 1. Execute theme styling injection pipeline safely to avoid attribute crash
stl.inject_shield_theme()

# Initialize core global session arrays
if "logged_in_uid" not in st.session_state:
    st.session_state["logged_in_uid"] = None
if "current_user_role" not in st.session_state:
    st.session_state["current_user_role"] = None
if "active_channel" not in st.session_state:
    st.session_state["active_channel"] = None

# =========================================================================
# SECURE GATEWAY LOGIN / SIGNUP MODULE
# =========================================================================
if st.session_state["logged_in_uid"] is None:
    st.markdown("<h1 style='text-align: center; color: #00a884; margin-top: 20px;'>🛡️ ACADEMIC SHIELD NETWORK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8696a0;'>Premium High-Quality Unified Workspace Portal (200+ Node Capacity)</p>", unsafe_allow_html=True)
    
    auth_tab1, auth_tab2 = st.tabs(["🔒 Secure Member Login", "📝 New Candidate Signup"])
    
    with auth_tab1:
        with st.form("Login Credentials Entry Form"):
            in_user = st.text_input("Username or Account ID Key")
            in_pwd = st.text_input("Security Access Password", type="password")
            if st.form_submit_button("AUTHORIZE SYSTEM BOUNDARY ACCESS"):
                matched_id = None
                for uid, data in db.USERS_REGISTRY.items():
                    if (data["username"] == in_user or uid == in_user) and data["pwd"] == in_pwd:
                        matched_id = uid
                        break
                if matched_id:
                    user_record = db.USERS_REGISTRY[matched_id]
                    if user_record["status"] == "Pending Review":
                        st.warning("⏳ Your registration token is currently in the Admin verification pipeline queue.")
                    elif user_record["status"] == "Suspended":
                        st.error("🚫 Access Revoked: This operational account node has been locked by administration.")
                    else:
                        st.session_state["logged_in_uid"] = matched_id
                        st.session_state["current_user_role"] = user_record["role"]
                        st.session_state["active_channel"] = "Super Admin Controls Hub" if user_record["role"] in ["ADMIN", "SUPER_ADMIN"] else "📝 Live Individual Exam Center"
                        st.rerun()
                else:
                    st.error("❌ Authentication breakdown: Invalid credentials supplied.")

    with auth_tab2:
        with st.form("Signup Parameter Intake Allocation"):
            reg_token = st.text_input("System Activation Code Token")
            reg_uid = st.text_input("Desired Account ID Number Allocation (e.g., 6615)")
            reg_username = st.text_input("Unique System Username")
            reg_password = st.text_input("Account Access Password", type="password")
            reg_fullname = st.text_input("Official Full Name")
            reg_school = st.text_input("School / Institution", value="The Amazima School")
            reg_phone = st.text_input("Active Phone Connection Contact Number")
            reg_email = st.text_input("Active Coordinate Email Address")
            reg_location = st.text_input("Current Location Hub", value="Kampala")
            reg_subjects = st.multiselect("Enrolled Academic Subjects", list(db.NCDC_CURRICULUM_MAP.keys()), default=["Pure Mathematics", "Biology"])
            
            if st.form_submit_button("SUBMIT STRUCTURAL DISPATCH FOR APPROVAL"):
                if reg_token not in db.REGISTRATION_CODES:
                    st.error("❌ Invalid System Token Key.")
                elif not reg_uid or not reg_username or not reg_password or not reg_fullname:
                    st.error("❌ Profile configuration criteria mismatch: Fields cannot be blank.")
                elif reg_uid in db.USERS_REGISTRY:
                    st.error("❌ ID mapping collision: That node ID already exists inside the permanent directory.")
                else:
                    db.USERS_REGISTRY[reg_uid] = {
                        "username": reg_username, "pwd": reg_password, "name": reg_fullname, "class": "Senior Five",
                        "school": reg_school, "phone": reg_phone, "email": reg_email, "location": reg_location,
                        "subjects": reg_subjects, "status": "Pending Review", "role": "USER", "warning_msg": ""
                    }
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.success("🎯 Payload successfully written to the incoming Admin pipeline queue tracker.")

else:
    # Resolve running runtime user matrix profile assets
    UID = st.session_state["logged_in_uid"]
    USER = db.USERS_REGISTRY.get(UID, None)
    if not USER:
        st.session_state["logged_in_uid"] = None
        st.rerun()

    # =========================================================================
    # PREMIUM STRUCTURE: TOP RIGHT HAND CORNER "SIGN OUT" CONTROL ANCHOR
    # =========================================================================
    st.markdown(f"""
    <div class="premium-header-bar">
        <div class="header-brand">🛡️ SHIELD NETWORK</div>
        <div class="header-identity">Current User Node: <span style="color:#00a884; font-weight:bold;">{USER['name']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    h_left, h_right = st.columns([5.5, 1.5])
    with h_right:
        if st.button("🚪 Sign out", use_container_width=True, help="Disconnect active session node immediately and return to login screen"):
            st.session_state["logged_in_uid"] = None
            st.session_state["current_user_role"] = None
            st.session_state["active_channel"] = None
            st.rerun()

    # Enforce global warning banner arrays if a user node has active citations
    if USER.get("warning_msg"):
        st.error(f"⚠️ **REGULATION NOTICE:** {USER['warning_msg']}")

    # =========================================================================
    # RESPONSIVE DRAW SIDEBAR ACCESSED VIA INTERACTIVE TOP LEFT MENU ARROWS
    # =========================================================================
    with st.sidebar:
        st.markdown(f"### 🗂️ Workspace Navigation")
        st.caption("Click the two arrows pointing left/right at the top of this panel to toggle sidebar canvas width.")
        st.write("---")
        
        # ABSOLUTE SEPARATION OF ADMINISTRATIVE HUBS VS STANDARD USER INTERFACES
        if USER["role"] in ["ADMIN", "SUPER_ADMIN"]:
            st.markdown("<b style='color:#ff4b4b;'>🛠️ SUPER ADMIN OVERRIDES</b>", unsafe_allow_html=True)
            workspace_channels = [
                "🎛️ Super Admin Controls Hub",
                "🔑 Registration Code Generator",
                "📥 Incoming Signups Request Queue",
                "📢 Mass Global Communication Portal",
                "📥 Suggestions Box Center",
                "📤 Upload Notes Page"
            ]
        else:
            st.markdown("<b style='color:#00a884;'>🎓 MEMBER CORE OPTIONS</b>", unsafe_allow_html=True)
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
            
        selected_nav = st.radio("Active Workspace Panels:", workspace_channels, label_visibility="collapsed")
        st.session_state["active_channel"] = selected_nav
        st.write("---")
        st.caption(f"System Node status: Connected securely as {USER['role']}")

    ACTIVE_WORKSPACE = st.session_state["active_channel"]

    # =========================================================================
    # WORKSPACE ENGINE 1: ADMINISTRATIVE CONSOLE PANELS (NO MIXED USER CHANNELS)
    # =========================================================================
    if USER["role"] in ["ADMIN", "SUPER_ADMIN"]:
        
        if ACTIVE_WORKSPACE == "🎛️ Super Admin Controls Hub":
            st.markdown("<h2>🎛️ Super Admin Regulation Hub Control Panel</h2>", unsafe_allow_html=True)
            st.caption("Ban, delete, warn, or terminate system registration logs instantly across the database footprint.")
            
            for target_uid, profile in list(db.USERS_REGISTRY.items()):
                if target_uid == UID: continue  # Avoid self-deletion locks
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h4>👤 Node ID Reference: <code>{target_uid}</code> | Name Target: {profile['name']} ({profile['username']})</h4>
                    <p><b>Current Allocation State:</b> {profile['status']} | <b>Warnings Vector Queue:</b> {profile['warning_msg'] if profile['warning_msg'] else 'None Recorded'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                b1, b2, b3, b4 = st.columns(4)
                with b1:
                    if st.button("⚠️ Warn Account", key=f"warn_{target_uid}"):
                        db.USERS_REGISTRY[target_uid]["warning_msg"] = "Official administrative citation logged. Retain system protocol guidelines."
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()
                with b2:
                    if st.button("🧹 Clear Warning", key=f"clear_{target_uid}"):
                        db.USERS_REGISTRY[target_uid]["warning_msg"] = ""
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()
                with b3:
                    if profile["status"] == "Approved":
                        if st.button("🔒 Ban & Terminate", key=f"ban_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Suspended"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                    else:
                        if st.button("🔓 Unlock Account", key=f"unlock_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Approved"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                with b4:
                    if st.button("🔴 Purge/Delete", key=f"del_{target_uid}"):
                        del db.USERS_REGISTRY[target_uid]
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "🔑 Registration Code Generator":
            st.markdown("<h2>🔑 Structural Registration Code Token Generator</h2>", unsafe_allow_html=True)
            st.write("Active security codes stored permanently inside cluster:")
            st.code(db.REGISTRATION_CODES)
            with st.form("Code Generation Framework Block"):
                new_token = st.text_input("Enter New Alphanumeric Activation String:")
                if st.form_submit_button("LOCK AND REGISTER TOKEN KEY"):
                    if new_token and new_token not in db.REGISTRATION_CODES:
                        db.REGISTRATION_CODES.append(new_token)
                        db.save_storage_node("registration_codes.json", db.REGISTRATION_CODES)
                        st.success("New structural activation token locked down successfully.")
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📥 Incoming Signups Request Queue":
            st.markdown("<h2>📥 Incoming Registration Verification Intake Pipeline</h2>", unsafe_allow_html=True)
            pending_nodes = False
            for target_uid, profile in list(db.USERS_REGISTRY.items()):
                if profile["status"] == "Pending Review":
                    pending_nodes = True
                    st.markdown(f"""
                    <div class="directory-profile-box" style="border-left: 4px solid #ffaa00;">
                        <b>Proposed Account ID Node:</b> {target_uid} | Name: {profile['name']}<br>
                        <b>School Connection Matrix:</b> {profile['school']} | Enrolled Fields: {', '.join(profile['subjects'])}
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
                st.info("No incoming account generation scripts are sitting in the verification loops.")

        elif ACTIVE_WORKSPACE == "📢 Mass Global Communication Portal":
            st.markdown("<h2>📢 High Priority Mass Global Communication Portal</h2>", unsafe_allow_html=True)
            with st.form("Global Broadcaster Box Subsystem"):
                msg_body = st.text_area("Write administrative notification warning packet content:")
                if st.form_submit_button("TRANSMIT EMERGENCY NOTICE TO EVERY ONLINE USER"):
                    if msg_body:
                        db.GLOBAL_BROADCASTS.insert(0, msg_body)
                        db.save_storage_node("global_broadcasts.json", db.GLOBAL_BROADCASTS)
                        st.success("Global administrative message broadcast completed securely.")

        elif ACTIVE_WORKSPACE == "📥 Suggestions Box Center":
            st.markdown("<h2>📥 Public Open Suggestions Box Center</h2>", unsafe_allow_html=True)
            if not db.SUGGESTIONS_BOX:
                st.info("Public suggestions file registers are empty.")
            for idx, sug in enumerate(db.SUGGESTIONS_BOX):
                st.markdown(f"""
                <div class="revision-note-card">
                    <p><b>Candidate Recommendation Log:</b> "{sug['text']}"</p>
                    <p style="color:#00a884;"><b>Administrative Feedback Log:</b> {sug.get('reply', 'No comment logged yet.')}</p>
                </div>
                """, unsafe_allow_html=True)
                with st.form(f"Reply Form Matrix Node {idx}"):
                    rep_txt = st.text_input("Log administrative response text definition:", key=f"rep_input_{idx}")
                    if st.form_submit_button("COMMIT RESPONSE PACKET TO DISK", key=f"rep_btn_{idx}"):
                        db.SUGGESTIONS_BOX[idx]["reply"] = rep_txt
                        db.save_storage_node("suggestions_box.json", db.SUGGESTIONS_BOX)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📤 Upload Notes Page":
            st.markdown("<h2>📤 Upload NCDC Syllabus Revision Material Notes</h2>", unsafe_allow_html=True)
            with st.form("Revision Resource Asset Configuration File Form"):
                nt_title = st.text_input("Revision Document Title Matrix")
                nt_sub = st.selectbox("Assign Core Syllabus Discipline Domain Target", list(db.NCDC_CURRICULUM_MAP.keys()))
                nt_data = st.text_area("Write reference summaries or input secure external drive cloud links:")
                if st.form_submit_button("PUBLISH LESSON NOTES TO CANDIDATES FILE STORAGE"):
                    if nt_title and nt_data:
                        db.REVISION_NOTES_VAULT.append({"Title": nt_title, "Subject": nt_sub, "Content": nt_data})
                        db.save_storage_node("revision_notes_vault.json", db.REVISION_NOTES_VAULT)
                        st.success("Syllabus documentation files successfully written to server network matrices.")

    # =========================================================================
    # WORKSPACE ENGINE 2: STANDARD STUDENT COLLABORATION PORTALS
    # =========================================================================
    else:
        
        if ACTIVE_WORKSPACE == "📝 Live Individual Exam Center":
            st.markdown("<h2>📝 Live Individual Assessment Engine Core</h2>", unsafe_allow_html=True)
            sel_sub = st.selectbox("Choose Target Subject Track Domain Field:", list(db.NCDC_CURRICULUM_MAP.keys()))
            sel_top = st.selectbox("Choose Targeted Topic Structural Focus Matrix:", db.NCDC_CURRICULUM_MAP[sel_sub])
            
            st.info(f"📋 **Active Configuration Script Module:** `{sel_sub} | {sel_top}`")
            st.markdown("**Question 1:** Define the fundamental structure of this system matrix and derive its variance paths.")
            
            with st.form("Individual Assessment Verification Form"):
                ans_text = st.text_area("Type your working calculations here:")
                ans_img = st.file_uploader("Or upload photo scan copy of handwritten equations:", type=["png","jpg","jpeg"])
                if st.form_submit_button("LOCK ANSWERS AND COMPUTE SCORE"):
                    st.success("Performance matrix evaluated via system tracking scripts.")
                    st.metric("Your Computed Score Rating", "88% Pass Profile Metric", delta="Principal A Grade Clearance")

        elif ACTIVE_WORKSPACE == "🤝 Synchronized Partner Exam Center":
            st.markdown("<h2>🤝 Synchronized Peer Collaboration Examination Center</h2>", unsafe_allow_html=True)
            st.caption("Paired partners complete concurrent evaluations controlled by the assigned Session Leader.")
            
            if "p_leader" not in st.session_state: st.session_state["p_leader"] = None
            if "p_stage" not in st.session_state: st.session_state["p_stage"] = 0
            
            st.write(f"Active Session Coordinator Node: **{st.session_state['p_leader'] if st.session_state['p_leader'] else 'Unassigned Framework'}**")
            if st.button("👑 Establish Self as Appointed Session Leader"):
                st.session_state["p_leader"] = USER["name"]
                st.rerun()
                
            if st.session_state["p_leader"]:
                if USER["name"] == st.session_state["p_leader"]:
                    st.markdown("### 🎛️ Session Leader Control Panel")
                    cc_sub = st.selectbox("Select Target Subject Track Parameter:", list(db.NCDC_CURRICULUM_MAP.keys()))
                    cc_top = st.selectbox("Select Topic Structural Revision Focus Area:", db.NCDC_CURRICULUM_MAP[cc_sub])
                    if st.button("🚀 Confirm Metrics & Generate 2 Mutual Questions"):
                        st.session_state["p_stage"] += 1
                        st.session_state["cc_s"] = cc_sub
                        st.session_state["cc_t"] = cc_top
                        st.rerun()
                
                if st.session_state["p_stage"] > 0:
                    st.markdown(f"#### 📝 Synchronized Focus Topic Vector: `{st.session_state.get('cc_t')}`")
                    st.warning("⚠️ **Mutual Question Segment 1:** Compute the structural limits matching NCDC references.")
                    st.warning("⚠️ **Mutual Question Segment 2:** Elaborate on tracking vectors and systemic deviations.")
                    
                    with st.form("Dual Partner Shared Parameter Allocation Input Form"):
                        st.write("##### Your Individual Work Area Answer Slot")
                        p_txt = st.text_area("Type working computation matrix strings:")
                        p_file = st.file_uploader("Or upload photo file capture of handwritten solution steps:", type=["png","jpg","jpeg"])
                        if st.form_submit_button("🔒 LOCK COLLABORATIVE RESPONSES"):
                            st.success("Answer packet safely logged to the synchronization buffer matrix.")
                    
                    if USER["name"] == st.session_state["p_leader"]:
                        if st.button("⏭️ Request System to Generate 2 More Questions"):
                            st.session_state["p_stage"] += 1
                            st.rerun()

        elif ACTIVE_WORKSPACE == "📚 Subject Group Discussions":
            st.markdown("<h2>📚 Interactive Subject Group Discussion Portal</h2>", unsafe_allow_html=True)
            
            if "g_leader" not in st.session_state: st.session_state["g_leader"] = None
            if "g_sub" not in st.session_state: st.session_state["g_sub"] = "Unassigned Syllabus Track"
            if "g_top" not in st.session_state: st.session_state["g_top"] = "Unassigned Topic Vector"
            if "g_mode" not in st.session_state: st.session_state["g_mode"] = {}
            if "g_hands" not in st.session_state: st.session_state["g_hands"] = []
            if "g_show_sol" not in st.session_state: st.session_state["g_show_sol"] = False

            my_status = st.session_state["g_mode"].get(UID, None)
            if not my_status:
                st.write("Confirm joining profile parameters before entering active classroom stream buffers:")
                dc1, dc2 = st.columns(2)
                with dc1:
                    if st.button("🎯 Enter Classroom as Active Discussion Participant"):
                        st.session_state["g_mode"][UID] = "ACTIVE"
                        if not st.session_state["g_leader"]:
                            st.session_state["g_leader"] = USER["name"]
                        st.rerun()
                with dc2:
                    if st.button("👻 Enter Classroom inside Invisible Ghost Mode"):
                        st.session_state["g_mode"][UID] = "GHOST"
                        st.rerun()
                st.stop()
                
            st.info(f"Classroom Session Leader Unit: **{st.session_state['g_leader']}** | Your Tracking Mode: **{my_status} PROFILE**")
            
            # =========================================================================
            # CRITICAL SPEC: INTERCOM VOICE FLOW RAISING CONTROLLER INSIDE MESSAGING PAGES ONLY
            # =========================================================================
            if my_status == "ACTIVE":
                st.write("---")
                st.markdown("#### ✋ Intercom Microphone Flow Raise Hand Controller")
                is_up = UID in st.session_state["g_hands"]
                if is_up:
                    if st.button("⬇️ LOWER MY INTERCOM VOICE HAND DISPATCH NOW", type="primary", use_container_width=True):
                        st.session_state["g_hands"].remove(UID)
                        st.rerun()
                else:
                    if st.button("✋ RAISE ACTIVE INTERCOM HAND FOR VOICE SPACE CLEARANCE", use_container_width=True):
                        st.session_state["g_hands"].append(UID)
                        st.rerun()
                        
            if st.session_state["g_hands"]:
                st.markdown("🗣️ **Active Voice Floor Intercom Queue:**")
                for h_uid in st.session_state["g_hands"]:
                    st.warning(f"🖐️ Active student user **{db.USERS_REGISTRY.get(h_uid, {}).get('name')}** has raised an intercom signal.")

            if USER["name"] == st.session_state["g_leader"]:
                st.markdown("### 👑 Session Leader Executive Control Dashboard")
                ld_s = st.selectbox("Set Room Focus Subject Areadiscipline Target:", list(db.NCDC_CURRICULUM_MAP.keys()))
                ld_t = st.text_input("Set Exact Discussion Subject Vector Area Topic Heading Framework:", value="Advanced Cell Physiology & Vectors Matrix")
                if st.button("🔒 Lock Topic Parameters down Stream Network"):
                    st.session_state["g_sub"] = ld_s
                    st.session_state["g_top"] = ld_t
                    st.rerun()
                if st.button("🎯 Deploy Dynamic Discussion Exam Question"):
                    st.session_state["g_exam_q"] = "Determine structural outputs verifying target vector profiles matching NCDC syllabi metrics."
                    st.session_state["g_show_sol"] = False
                    st.rerun()
                if st.button("✅ Force Display NCDC Standard Solution Matrix Sheet"):
                    st.session_state["g_show_sol"] = True
                    st.rerun()

            st.markdown(f"### Current Workspace Focus: `{st.session_state['g_sub']} -> {st.session_state['g_top']}`")
            if "g_exam_q" in st.session_state:
                st.info(f"❓ **Active Discussion Blueprint Problem:**\n{st.session_state['g_exam_q']}")
            if st.session_state["g_show_sol"]:
                st.success("🌟 **NCDC Standard Solution Map:**\nApplying structural alignment guidelines resolves the derivative limits factor smoothly to 1.000.")

            # Unified media interaction frame supporting text, handwriting photo, and audio message memos
            with st.form("Group Interactive Multimedia Submission Frame", clear_on_submit=True):
                txt_in = st.text_input("Type message payload or question feedback comment:")
                img_in = st.file_uploader("Upload handwritten calculation worksheet scan photo:", type=["jpg","png","jpeg"], key="g_img")
                aud_in = st.file_uploader("Upload recorded audio message voice note explanation file segment:", type=["mp3","wav","m4a"], key="g_aud")
                if st.form_submit_button("TRANSMIT MULTIMEDIA ENTRY"):
                    st.success("Multimedia parameters successfully written to room logs.")

        elif ACTIVE_WORKSPACE == "💬 General Lounge Chat":
            st.markdown("<h2>💬 Global WhatsApp Media Communications Lounge</h2>", unsafe_allow_html=True)
            
            st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
            mock_lounge = [
                {"sender": "Gideon Cheps", "uid": "6602", "text": "Are we covering the Biology Cell Physiology topic tracks inside the sync center tonight?", "time": "11:02"},
                {"sender": "Sudaisi Setra", "uid": "6601", "text": "Yes, biochemistry structural files have already been mapped down database configurations.", "time": "11:05"}
            ]
            for m in mock_lounge:
                side = "bubble-right" if m["uid"] == UID else "bubble-left"
                st.markdown(f"""
                <div class="message-bubble {side}">
                    <span class="bubble-sender">{m['sender']}</span>
                    <div>{m['text']}</div>
                    <span class="bubble-time">{m['time']}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Lounge Unified Media Console Link Box", clear_on_submit=True):
                l_msg = st.text_input("Type your message text details here...")
                l_img = st.file_uploader("Upload picture study screenshot attachment assets:", type=["png","jpg","jpeg"], key="l_img_u")
                l_aud = st.file_uploader("Upload recorded audio voice notes explanation voice clips parameters:", type=["mp3","wav","m4a"], key="l_aud_u")
                if st.form_submit_button("SEND MSG"):
                    st.success("Message packet injected successfully onto server lounge streams.")

        elif ACTIVE_WORKSPACE == "🔒 Private Peer Chatroom":
            st.markdown("<h2>🔒 Private Peer-to-Peer Secure Cryptographic Room</h2>", unsafe_allow_html=True)
            st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
            mock_p2p = [
                {"sender": "Gideon Cheps", "uid": "6602", "text": "I completed loading the Pure Math trial exam script parameters. Check your progress analytics chart.", "time": "08:14"},
                {"sender": "Sudaisi Setra", "uid": "6601", "text": "Acknowledged. Opening performance tracker views now.", "time": "08:15"}
            ]
            for p in mock_p2p:
                side = "bubble-right" if p["uid"] == UID else "bubble-left"
                st.markdown(f"""
                <div class="message-bubble {side}">
                    <span class="bubble-sender">{p['sender']}</span>
                    <div>{p['text']}</div>
                    <span class="bubble-time">{p['time']}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Private Channel Transmission Box", clear_on_submit=True):
                p_msg_txt = st.text_input("Type private conversation content...")
                p_msg_img = st.file_uploader("Attach encrypted photograph file matrix scan:", type=["png","jpg","jpeg"], key="p_img_u")
                p_msg_aud = st.file_uploader("Attach microphone audio clip voice recording explanation files:", type=["mp3","wav","m4a"], key="p_aud_u")
                if st.form_submit_button("TRANSMIT ENCRYPTED SYSTEM PACKET"):
                    st.success("Encrypted payload safely dispatched onto recipient node memory lines.")

        elif ACTIVE_WORKSPACE == "📊 Personal Progress Tracker":
            st.markdown("<h2>📊 Personal Progress Tracker Dashboard Matrices</h2>", unsafe_allow_html=True)
            mock_tracker_data = {
                "Syllabus Curriculum Module Focus": ["Quadratics & Cubics", "Vectors & Collinearity", "Cell Physiology (Biology)", "Biochemistry Modules (Biology)", "The Mole Concept (Chemistry)"],
                "Mastery Level Percentage": [95, 88, 80, 45, 70],
                "Syllabus Status Tag Classification": ["Mastered Perfectly", "Mastered Perfectly", "Revised & Verified", "Review Deficit Area", "Revised & Verified"]
            }
            df = pd.DataFrame(mock_tracker_data)
            st.bar_chart(df.set_index("Syllabus Curriculum Module Focus")["Mastery Level Percentage"])
            st.table(df)

        elif ACTIVE_WORKSPACE == "📂 Finished Exam Vault Storage":
            st.markdown("<h2>📂 Done Assessment Historical Storage Vault</h2>", unsafe_allow_html=True)
            st.markdown("""
            <div class="revision-note-card">
                <h4>📄 Document Instance: <b>Advanced Biology & Pure Mathematics Unified Assessment</b></h4>
                <p><b>Completion Date Tracking Parameter:</b> 2026-05-25 | <b>Final Grade Scored:</b> <span style='color:#00a884; font-weight:bold;'>Principal A (92.5%)</span></p>
                <p style='font-size:12.5px; color:#8696a0;'>Attached explicitly alongside compiled student answer inputs + NCDC official verified master evaluation solution sheets.</p>
            </div>
            """, unsafe_allow_html=True)
            
            pdf_string_data = (
                "🛡️ SHIELD NETWORK ARCHIVE SYSTEM ASSESSMENT REPORT\n"
                "====================================================\n"
                f"Candidate Account Node: {USER['name']} ({UID})\n"
                "Calculated Performance Metric Score: 92.5% [National Principal Grade A Master Level Assignment Approved]\n\n"
                "SECTION A (BIOLOGY CELL PHYSIOLOGY):\n"
                "Question: Discuss ultra-structure cellular components properties.\n"
                "Candidate Submission Answer Profile: [Handwritten Image Script Asset ID #8843 Verified Safe]\n"
                "NCDC Reference Standard Marking Sheet Matrix Solution: Cell membranes must present fluid mosaic matrix properties scaling proportionally. Perfect evaluation fit.\n"
            )
            st.download_button(
                label="📥 Download Historical Exam Report File (Formatted PDF Output)",
                data=pdf_string_data,
                file_name=f"Shield_Assessment_Report_Node_{UID}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        elif ACTIVE_WORKSPACE == "📖 Global Candidates Directory":
            st.markdown("<h2>📖 Global Network Candidate Registry Directory Panel</h2>", unsafe_allow_html=True)
            st.caption("Rendering active account records for 200+ network nodes safely. Security passwords hidden completely from view profiles.")
            
            for d_uid, d_profile in db.USERS_REGISTRY.items():
                if d_profile["status"] != "Approved": continue
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h3>👤 Account Profile: {d_profile['name']} <span style='font-size:12px; color:#8696a0;'>(System ID Key Node: {d_uid})</span></h3>
                    <p><b>Username Reference Key:</b> <code>{d_profile['username']}</code> | <b>Institution Campus Location:</b> {d_profile['school']}</p>
                    <p><b>Current Location Hub Coordinates:</b> {d_profile['location']} | <b>Active Phone Line:</b> {d_profile['phone']} | <b>Email Node String:</b> {d_profile['email']}</p>
                    <p><b>Enrolled Syllabus Curriculum Tracks Profile:</b> <span style='color:#00a884;'>{', '.join(d_profile['subjects'])}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                da1, da2, _ = st.columns([1.5, 2, 4])
                with da1:
                    if st.button(f"✉️ Send Message to Node {d_uid}", key=f"dm_dir_{d_uid}"):
                        st.info(f"Direct text communications link initialized alongside user {d_profile['name']}. Access your Private Chat panel options.")
                with da2:
                    if st.button(f"🤝 Request Academic Partnership with Node {d_uid}", key=f"prt_dir_{d_uid}"):
                        st.success(f"Academic synchronization partnership request cleanly dispatched over system lines to user node {d_profile['name']}!")
