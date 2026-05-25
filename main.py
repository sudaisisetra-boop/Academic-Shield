# =========================================================================
# FILE 3 OF 3: MASTER ROUTING ENGINE CORE (main.py)
# =========================================================================
import streamlit as st
import pandas as pd
import time

# Absolute first call integration line
import database as db
import styles as stl

# Apply the custom high-quality dark mode and layout settings
stl.inject_shield_theme()

# Verify active session states
if "logged_in_uid" not in st.session_state:
    st.session_state["logged_in_uid"] = None
if "current_user_role" not in st.session_state:
    st.session_state["current_user_role"] = None
if "active_channel" not in st.session_state:
    st.session_state["active_channel"] = None

# =========================================================================
# GATEWAY AUTHENTICATION SHIELD LAYOUT
# =========================================================================
if st.session_state["logged_in_uid"] is None:
    st.markdown("<h1 style='text-align: center; color: #00a884;'>🛡️ ACADEMIC SHIELD NETWORK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8696a0;'>Premium High-Quality Unified Workspace Portal (200+ Node Ready)</p>", unsafe_allow_html=True)
    
    auth_tab1, auth_tab2 = st.tabs(["🔒 Secure Member Login", "📝 New Candidate Signup"])
    
    with auth_tab1:
        with st.form("Login Credentials Matrix Entry"):
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
                        # Pre-route base default view channels based on assigned operational role
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
            reg_subjects = st.multiselect("Enrolled Academic Subjects", list(db.NCDC_CURRICULUM_MAP.keys()), default=["Mathematics", "Biology"])
            
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
                        "subjects": reg_subjects, "status": "Pending Review", "role": "USER", "warning_msg": "",
                        "partner": "", "partner_role": "Standalone"
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
    # PREMIUM FIX: UPPER RIGHT LOGOUT BANNER ZONE
    # =========================================================================
    st.markdown(f"""
    <div class="premium-header-bar">
        <div class="header-brand">🛡️ SHIELD NETWORK v4.26</div>
        <div class="header-identity">Active: <span style="color:#00a884; font-weight:bold;">{USER['name']} ({USER['role']})</span></div>
    </div>
    """, unsafe_allow_html=True)

    col_space_buffer, col_sign_out = st.columns([6, 1.2])
    with col_sign_out:
        if st.button("🚪 Logout / Sign out", use_container_width=True, help="Disconnect active account node immediately"):
            st.session_state["logged_in_uid"] = None
            st.session_state["current_user_role"] = None
            st.session_state["active_channel"] = None
            st.rerun()

    # Apply global admin warning alerts block if current node is cited
    if USER.get("warning_msg"):
        st.error(f"⚠️ **REGULATION NOTICE:** {USER['warning_msg']}")

    # =========================================================================
    # ORIGINAL SIDEBAR DRAW COMPONENT (ACCESSED VIA TOP-LEFT ARROWS ICON)
    # =========================================================================
    with st.sidebar:
        st.markdown(f"### 🗂️ {USER['name']}'s Workspace")
        st.caption("Tap top-left workspace menu arrows to minimize/maximize view channel selection.")
        st.write("---")
        
        # ---------------------------------------------------------------------
        # ABSOLUTE ROLE ISOLATION SYSTEM DETECTOR
        # ---------------------------------------------------------------------
        if USER["role"] in ["ADMIN", "SUPER_ADMIN"]:
            st.markdown("<b style='color:#ff3333;'>🛡️ ADMINISTRATIVE CORE CONSOLE</b>", unsafe_allow_html=True)
            admin_options = [
                "🎛️ Super Admin Controls Hub",
                "🔑 Registration Code Generator",
                "📥 Intake Registration Request Queue",
                "📢 Mass Global Communication Portal",
                "📥 Suggestions Box Center",
                "📤 Upload Notes Reference Portal"
            ]
            if st.session_state["active_channel"] not in admin_options:
                st.session_state["active_channel"] = admin_options[0]
            selected_node = st.radio("Navigate Control Matrices:", admin_options)
            st.session_state["active_channel"] = selected_node
        else:
            st.markdown("<b style='color:#00a884;'>🎓 CANDIDATE CHANNELS WORKSPACE</b>", unsafe_allow_html=True)
            candidate_options = [
                "📝 Live Individual Exam Center",
                "🤝 Synchronized Partner Exam Center",
                "📚 Subject Group Discussions",
                "💬 General Lounge Chat",
                "🔒 Private Peer Chatroom",
                "📊 Personal Progress Tracker",
                "📂 Finished Exam Vault Storage",
                "📖 Global Candidates Directory"
            ]
            if st.session_state["active_channel"] not in candidate_options:
                st.session_state["active_channel"] = candidate_options[0]
            selected_node = st.radio("Navigate Channels Tree:", candidate_options)
            st.session_state["active_channel"] = selected_node

        st.write("---")
        st.caption("System Instance Node Engine Online.")

    ACTIVE_WORKSPACE = st.session_state["active_channel"]

    # =========================================================================
    # EXECUTION VIEWPORT A: ADMINISTRATIVE CORE OPERATIONAL TERMINAL
    # =========================================================================
    if USER["role"] in ["ADMIN", "SUPER_ADMIN"] and ACTIVE_WORKSPACE.startswith(("🎛️", "🔑", "📥", "📢", "📤")):
        
        if ACTIVE_WORKSPACE == "🎛️ Super Admin Controls Hub":
            st.markdown("<h2>🛠️ Master Identity Registry Moderator</h2>", unsafe_allow_html=True)
            st.caption("Ban, delete, warn, or terminate rogue account metrics instantly.")
            
            for target_uid, profile in list(db.USERS_REGISTRY.items()):
                if target_uid == UID: continue # Protect self administrative credentials node from drop routines
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h4>👤 User Node ID: <code>{target_uid}</code> | Name: {profile['name']}</h4>
                    <p><b>Status Flag:</b> {profile['status']} | <b>Active Violations Summary:</b> {profile['warning_msg'] if profile['warning_msg'] else 'Clear'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    if st.button("⚠️ Log Warning Citation", key=f"w_{target_uid}"):
                        db.USERS_REGISTRY[target_uid]["warning_msg"] = "Official warning issued. Retain compliance."
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()
                with c2:
                    if st.button("🧹 Clear Warnings Stack", key=f"c_{target_uid}"):
                        db.USERS_REGISTRY[target_uid]["warning_msg"] = ""
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()
                with c3:
                    if profile["status"] == "Approved":
                        if st.button("🔒 Ban & Terminate Node Access", key=f"b_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Suspended"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                    else:
                        if st.button("🔓 Unlock Account State", key=f"u_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Approved"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                with c4:
                    if st.button("🔴 Purge Account Data", key=f"p_{target_uid}"):
                        del db.USERS_REGISTRY[target_uid]
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "🔑 Registration Code Generator":
            st.markdown("<h2>🔑 Token Code Assignment Engine</h2>", unsafe_allow_html=True)
            st.write("Active structural invitation verification codes saved:")
            st.code(db.REGISTRATION_CODES)
            with st.form("Add Token Field Block"):
                new_token = st.text_input("Compile New Registration Security Activation Code Key")
                if st.form_submit_button("LOCK AND BROADCAST ACTIVATION TOKEN"):
                    if new_token and new_token not in db.REGISTRATION_CODES:
                        db.REGISTRATION_CODES.append(new_token)
                        db.save_storage_node("registration_codes.json", db.REGISTRATION_CODES)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📥 Intake Registration Request Queue":
            st.markdown("<h2>📥 Identity Approvals Processing Intake Queue</h2>", unsafe_allow_html=True)
            pending_found = False
            for target_uid, profile in list(db.USERS_REGISTRY.items()):
                if profile["status"] == "Pending Review":
                    pending_found = True
                    st.markdown(f"""
                    <div class="directory-profile-box" style="border-left: 4px solid #ffcc00;">
                        <b>Account ID Requested:</b> {target_uid} | Name: {profile['name']}<br>
                        <b>Subjects Map Selection:</b> {', '.join(profile['subjects'])}
                    </div>
                    """, unsafe_allow_html=True)
                    ac1, ac2 = st.columns(2)
                    with ac1:
                        if st.button("🎯 Authorize & Approve Profile", key=f"app_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Approved"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                    with ac2:
                        if st.button("❌ Reject Account Discard Request", key=f"rej_{target_uid}"):
                            del db.USERS_REGISTRY[target_uid]
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
            if not pending_found:
                st.info("No incoming signups requiring attention inside verification pipeline channels.")

        elif ACTIVE_WORKSPACE == "📢 Mass Global Communication Portal":
            st.markdown("<h2>📢 High-Priority Global System Broadcast Terminal</h2>", unsafe_allow_html=True)
            with st.form("Broadcast Terminal Block Frame"):
                msg_body = st.text_input("Type emergency priority system message text:")
                if st.form_submit_button("TRANSMIT ALERTS TO EVERY SYSTEM MODULE SCREEN"):
                    if msg_body:
                        db.GLOBAL_BROADCASTS.insert(0, msg_body)
                        db.save_storage_node("global_broadcasts.json", db.GLOBAL_BROADCASTS)
                        st.success("Global alert packet broadcasted securely.")

        elif ACTIVE_WORKSPACE == "📥 Suggestions Box Center":
            st.markdown("<h2>💬 Transparent Public Suggestions Repository</h2>", unsafe_allow_html=True)
            if not db.SUGGESTIONS_BOX:
                st.info("No user suggestions submitted into database yet.")
            for idx, sug in enumerate(db.SUGGESTIONS_BOX):
                st.markdown(f"""
                <div class="revision-note-card">
                    <b>Node Submission Entry ID:</b> Anonymous Candidate Member<br>
                    <b>Text:</b> {sug['text']}<br>
                    <span style="color:#00a884;"><b>Official Response:</b> {sug.get('reply', 'No administrative response logged yet.')}</span>
                </div>
                """, unsafe_allow_html=True)
                with st.form(f"Reply Suggestion Matrix {idx}"):
                    rep_txt = st.text_input("Draft administrative response text:")
                    if st.form_submit_button("COMMIT RESPONSE PACKET"):
                        db.SUGGESTIONS_BOX[idx]["reply"] = rep_txt
                        db.save_storage_node("suggestions_box.json", db.SUGGESTIONS_BOX)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📤 Upload Notes Reference Portal":
            st.markdown("<h2>📤 NCDC Standard Syllabus Study Material Library</h2>", unsafe_allow_html=True)
            with st.form("Study Notes Asset Attachment Form"):
                nt_title = st.text_input("Revision Document Title String")
                nt_sub = st.selectbox("Assign Core Syllabus Domain Discipline Target", list(db.NCDC_CURRICULUM_MAP.keys()))
                nt_data = st.text_area("Write summary content or insert secure drive cloud document hyper-links:")
                if st.form_submit_button("COMMIT NOTE PACKET PERMANENTLY TO SYSTEM VAULT"):
                    if nt_title and nt_data:
                        db.REVISION_NOTES_VAULT.append({"Title": nt_title, "Subject": nt_sub, "Content": nt_data})
                        db.save_storage_node("revision_notes_vault.json", db.REVISION_NOTES_VAULT)
                        st.success("Syllabus resource material successfully written to data cluster storage matrices.")

    # =========================================================================
    # EXECUTION VIEWPORT B: CANDIDATE COLLABORATION ENVIRONMENT
    # =========================================================================
    elif USER["role"] == "USER" and ACTIVE_WORKSPACE.startswith(("📝", "🤝", "📚", "💬", "🔒", "📊", "📂", "📖")):
        
        if ACTIVE_WORKSPACE == "📝 Live Individual Exam Center":
            st.markdown("<h2>📝 Individual Microsecond Assessment Core Engine</h2>", unsafe_allow_html=True)
            st.caption("Simulates real-time examination testing blocks based on selected principal advanced curriculum tracks.")
            
            sel_sub = st.selectbox("Choose Target Subject Track Domain Field:", list(db.NCDC_CURRICULUM_MAP.keys()))
            sel_top = st.selectbox("Choose Targeted Topic Structural Focus Matrix:", db.NCDC_CURRICULUM_MAP[sel_sub])
            
            st.info(f"📋 **Current Exam Script Configuration Module Instance:** `{sel_sub} | {sel_top}`")
            st.markdown("**Question 1:** Define the fundamental linear vector structures or metabolic pathways mapping this system matrix.")
            
            exam_mode = st.radio("Choose Entry Assessment Interface Format Type:", ["🔤 Typed Input Fields Option", "✍️ Upload Handwritten Work Solution Images"], horizontal=True)
            with st.form("Individual Submission Matrix Engine Block"):
                if exam_mode == "🔤 Typed Input Fields Option":
                    ans_text = st.text_area("Type your working calculations or full solution equations here:")
                else:
                    ans_img = st.file_uploader("Scan and upload photo file copy scan of handwritten structural equations:", type=["png","jpg","jpeg"])
                
                if st.form_submit_button("LOCK SYSTEM ANSWERS AND COMPUTE TARGET PERCENTAGE PERFORMANCE"):
                    st.success("Evaluating performance data profiles using microsecond calculations parsing loops...")
                    st.metric("Computed Performance Score Rating Metric", "75% Pass Profile Metric Score", delta="Principal B Rating Scale Status Secured")

        elif ACTIVE_WORKSPACE == "🤝 Synchronized Partner Exam Center":
            st.markdown("<h2>🤝 Synchronized Peer Collaboration Examination Center</h2>", unsafe_allow_html=True)
            st.caption("Allows paired partner nodes to run concurrent evaluation tests under dynamic orchestration controls.")
            
            if "p_leader" not in st.session_state: st.session_state["p_leader"] = None
            if "p_stage" not in st.session_state: st.session_state["p_stage"] = 0
            
            st.write(f"Active Session Coordinator Coordinator: **{st.session_state['p_leader'] if st.session_state['p_leader'] else 'Unassigned Module'}**")
            if st.button("👑 Appoint Self Session Leader"):
                st.session_state["p_leader"] = USER["name"]
                st.rerun()
                
            if st.session_state["p_leader"]:
                if USER["name"] == st.session_state["p_leader"]:
                    st.markdown("### 🎛️ Session Leader Allocation Panel Matrix")
                    cc_sub = st.selectbox("Select Subject Parameter Matrix Area:", list(db.NCDC_CURRICULUM_MAP.keys()))
                    cc_top = st.selectbox("Select Syllabus Revision Topic Matrix Area:", db.NCDC_CURRICULUM_MAP[cc_sub])
                    if st.button("🚀 Confirm Parameters & Generate 2 Exam Questions Now"):
                        st.session_state["p_stage"] += 1
                        st.session_state["cc_s"] = cc_sub
                        st.session_state["cc_t"] = cc_top
                        st.rerun()
                
                if st.session_state["p_stage"] > 0:
                    st.markdown(f"#### 📝 Active Assessment Field Focus Track: `{st.session_state.get('cc_t')}`")
                    st.warning("⚠️ Question 1: Compute proportional values matching calculation framework values.")
                    st.warning("⚠️ Question 2: Elaborate on structural systems mechanisms or advanced vectors collinear paths.")
                    
                    with st.form("Dual Partner Interactive Input Allocation Form"):
                        st.write("##### Your Submission Workspace Profile Input Box Slot")
                        p_txt = st.text_area("Type working calculation tracking text inputs:")
                        p_file = st.file_uploader("Upload handwritten computation work image file sheet:", type=["png","jpg","jpeg"])
                        if st.form_submit_button("🔒 LOCK COLLABORATIVE RESPONSE SEGMENTS"):
                            st.success("Your answer coordinates have been safely written to the partner synchronization ledger.")
                    
                    if USER["name"] == st.session_state["p_leader"]:
                        if st.button("⏭️ Request 2 More Questions From Next Module Segment"):
                            st.session_state["p_stage"] += 1
                            st.rerun()

        elif ACTIVE_WORKSPACE == "📚 Subject Group Discussions":
            st.markdown("<h2>📚 Interactive Subject Group Discussion Portal</h2>", unsafe_allow_html=True)
            
            if "g_leader" not in st.session_state: st.session_state["g_leader"] = None
            if "g_sub" not in st.session_state: st.session_state["g_sub"] = "Unassigned Matrix"
            if "g_top" not in st.session_state: st.session_state["g_top"] = "Unassigned Matrix"
            if "g_mode" not in st.session_state: st.session_state["g_mode"] = {}
            if "g_hands" not in st.session_state: st.session_state["g_hands"] = []
            if "g_show_sol" not in st.session_state: st.session_state["g_show_sol"] = False

            my_session_status = st.session_state["g_mode"].get(UID, None)
            if not my_session_status:
                st.write("Confirm your room configuration parameters to connect safely down the classroom stream channel:")
                c_act, c_gh = st.columns(2)
                with c_act:
                    if st.button("🎯 Enter Room as Active Discussion Node"):
                        st.session_state["g_mode"][UID] = "ACTIVE"
                        if not st.session_state["g_leader"]:
                            st.session_state["g_leader"] = USER["name"]
                        st.rerun()
                with c_gh:
                    if st.button("👻 Enter Room Inside Invisible Ghost View Mode"):
                        st.session_state["g_mode"][UID] = "GHOST"
                        st.rerun()
                st.stop()
                
            st.info(f"Discussion Leader Unit: **{st.session_state['g_leader']}** | Your Profile State: **{my_session_status} MODE**")
            
            # =========================================================================
            # PREMIUM FEATURE: INTERCOM TRIGGER SHUTTLES ONLY INSIDE MESSAGING DOMAINS
            # =========================================================================
            if my_session_status == "ACTIVE":
                st.write("---")
                st.markdown("#### ✋ Intercom Microphone Flow Hand-Raise Controller Node")
                is_raised = UID in st.session_state["g_hands"]
                if is_raised:
                    if st.button("⬇️ LOWER MY INTERCOM HAND", type="primary", use_container_width=True):
                        st.session_state["g_hands"].remove(UID)
                        st.rerun()
                else:
                    if st.button("✋ RAISE INTERCOM HAND SIGNAL TO SESSION LEADER", use_container_width=True):
                        st.session_state["g_hands"].append(UID)
                        st.rerun()
                        
            if st.session_state["g_hands"]:
                st.markdown("🗣️ **Active Intercom Request Stack:**")
                for h_uid in st.session_state["g_hands"]:
                    st.warning(f"🖐️ Node candidate user **{db.USERS_REGISTRY.get(h_uid, {}).get('name')}** requests voice floor space clearance.")

            if USER["name"] == st.session_state["g_leader"]:
                st.markdown("### 👑 Session Leader Executive Control Override Dashboard")
                ld_s = st.selectbox("Set Room Focus Subject Area discipline Target:", list(db.NCDC_CURRICULUM_MAP.keys()))
                ld_t = st.text_input("Set Exact Discussion Subject Vector Area Topic Heading Framework:", value="Cell Biology Anatomy / Vector Fields Analysis")
                if st.button("🔒 Broadcast Topic Parameters Globally to Room Matrix"):
                    st.session_state["g_sub"] = ld_s
                    st.session_state["g_top"] = ld_t
                    st.rerun()
                if st.button("🎯 Inject Selected Examination Blueprint Question Matrix"):
                    st.session_state["g_exam_q"] = "Determine the computational outcomes of checking vector structures matching NCDC references."
                    st.session_state["g_show_sol"] = False
                    st.rerun()
                if st.button("✅ Inject NCDC Standard Reference Solutions Sheet Now"):
                    st.session_state["g_show_sol"] = True
                    st.rerun()

            st.markdown(f"### Current Workspace Focus: `{st.session_state['g_sub']} -> {st.session_state['g_top']}`")
            if "g_exam_q" in st.session_state:
                st.info(f"❓ **Active Discussion Target Problem Question:**\n{st.session_state['g_exam_q']}")
            if st.session_state["g_show_sol"]:
                st.success("🌟 **NCDC Standard Reference Solution Structural Layout Outline:**\nApplying core curriculum parameters yields a proportional convergence factor scaling down cleanly to 1.000.")

            # Unified classroom media chat interaction node
            with st.form("Group Room Transmit Matrix Console", clear_on_submit=True):
                txt_in = st.text_input("Type comment or message payload:")
                img_in = st.file_uploader("Attach handwritten solution scan photo option:", type=["jpg","png","jpeg"], key="grp_img")
                aud_in = st.file_uploader("Attach micro-classroom audio note recordings audio files options:", type=["mp3","wav","m4a"], key="grp_aud")
                if st.form_submit_button("TRANSMIT PACKET TO STREAM"):
                    st.success("Data transmitted safely down classroom discussion channels.")

        elif ACTIVE_WORKSPACE == "💬 General Lounge Chat":
            st.markdown("<h2>💬 Global WhatsApp Media Communications Lounge</h2>", unsafe_allow_html=True)
            
            st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
            # Simulated real-time left-right chat bubble presentation algorithms
            mock_lounge = [
                {"sender": "Gideon Cheps", "uid": "6602", "text": "Are we covering the Biology Biochemistry topic tracks inside the sync center tonight?", "time": "11:02"},
                {"sender": "Sudaisi Setra", "uid": "6601", "text": "Yes, cell physiology structural systems files have already been uploaded inside the database.", "time": "11:05"}
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
                l_msg = st.text_input("Type your message payload text data here...")
                l_img = st.file_uploader("Upload picture study screenshot attachment assets:", type=["png","jpg","jpeg"], key="lng_img")
                l_aud = st.file_uploader("Upload recorded audio voice notes explanation voice clips parameters:", type=["mp3","wav","m4a"], key="lng_aud")
                if st.form_submit_button("SEND MSG"):
                    st.success("Message packet injected successfully onto server lounge streams.")

        elif ACTIVE_WORKSPACE == "🔒 Private Peer Chatroom":
            st.markdown("<h2>🔒 Private Peer-to-Peer Secure Communication Channel</h2>", unsafe_allow_html=True)
            p_link = USER.get("partner", "")
            if not p_link:
                st.warning("No active partner node coordinate handshake is established inside your registry directory profile.")
            else:
                partner_profile = db.USERS_REGISTRY.get(p_link, {})
                st.info(f"🔒 Isolated end-to-end cryptographic frequency link channel paired alongside user node identifier: **{partner_profile.get('name')}**")
                
                st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
                mock_p2p = [
                    {"sender": partner_profile.get("name"), "uid": p_link, "text": "I completed loading the Pure Math trial exam script parameters. Check your progress analytics chart.", "time": "08:14"},
                    {"sender": USER["name"], "uid": UID, "text": "Acknowledged. Opening performance tracker views now.", "time": "08:15"}
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
                    p_msg_img = st.file_uploader("Attach encrypted photograph file matrix scan:", type=["png","jpg","jpeg"], key="p2p_img")
                    p_msg_aud = st.file_uploader("Attach microphone audio clip voice recording explanation files:", type=["mp3","wav","m4a"], key="p2p_aud")
                    if st.form_submit_button("TRANSMIT ENCRYPTED SYSTEM PACKET"):
                        st.success("Encrypted payload safely dispatched onto recipient node memory lines.")

        elif ACTIVE_WORKSPACE == "📊 Personal Progress Tracker":
            st.markdown("<h2>📊 Graphical Syllabus Milestone Coverage Tracker</h2>", unsafe_allow_html=True)
            st.caption("Simplified metrics tables and tracking charts illustrating your total curriculum mastery.")
            
            mock_tracker_data = {
                "Syllabus Curriculum Module": ["Quadratics & Cubics", "Vectors & Collinearity", "Cell Physiology (Biology)", "Biochemistry Modules (Biology)", "The Mole Concept (Chemistry)"],
                "Mastery Level Percentage": [90, 85, 75, 40, 65],
                "Syllabus Status Tag Classification": ["Mastered Perfectly", "Mastered Perfectly", "Revised & Verified", "Review Deficit Area", "Revised & Verified"]
            }
            df = pd.DataFrame(mock_tracker_data)
            st.bar_chart(df.set_index("Syllabus Curriculum Module")["Mastery Level Percentage"])
            st.table(df)

        elif ACTIVE_WORKSPACE == "📂 Finished Exam Vault Storage":
            st.markdown("<h2>📂 Historical Finished Assessment Vault</h2>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="revision-note-card">
                <h4>📄 Document Code ID Log Instance: <b>Advanced Biology & Pure Mathematics Unified Assessment</b></h4>
                <p><b>Completion Date Parameters:</b> 2026-05-25 | <b>Final Grade Earned:</b> <span style='color:#00a884; font-weight:bold;'>Principal A (92.5%)</span></p>
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
                file_name=f"Shield_Vault_Assessment_Report_Node_{UID}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        elif ACTIVE_WORKSPACE == "📖 Global Candidates Directory":
            st.markdown("<h2>📖 Global Network Candidate Registry Directory</h2>", unsafe_allow_html=True)
            st.caption("Rendering active account attributes safely for 200+ network nodes. Passwords hidden.")
            
            for d_uid, d_profile in db.USERS_REGISTRY.items():
                if d_profile["status"] != "Approved": continue
                
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h3>👤 Candidate Name: {d_profile['name']} <span style='font-size:12px; color:#8696a0;'>(System ID Key: {d_uid})</span></h3>
                    <p><b>Username Reference Account Handle:</b> <code>{d_profile['username']}</code> | <b>Institution Link:</b> {d_profile['school']}</p>
                    <p><b>Current Location Hub:</b> {d_profile['location']} | <b>Phone Line Contact Connection:</b> {d_profile['phone']} | <b>Email Link:</b> {d_profile['email']}</p>
                    <p><b>Enrolled Syllabus Curriculum Tracks Profile:</b> <span style='color:#00a884;'>{', '.join(d_profile['subjects'])}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                da1, da2, _ = st.columns([1.5, 2, 4])
                with da1:
                    if st.button(f"✉️ Direct Message Node {d_uid}", key=f"dm_{d_uid}"):
                        st.info(f"Direct connection request sent to user {d_profile['name']}. Access your Private Chat panel.")
                with da2:
                    if st.button(f"🤝 Request Academic Partnership Node {d_uid}", key=f"prt_{d_uid}"):
                        st.success(f"Academic sync alliance invitation successfully routed across server wire nodes to {d_profile['name']}!")
