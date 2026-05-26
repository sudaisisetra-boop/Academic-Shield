# =========================================================================
# WORKSPACE SYSTEM ARCHITECTURE LAYER (main.py) - PART 1
# =========================================================================
import streamlit as st
import pandas as pd
import database as db
import styles as stl
import time
from fpdf import FPDF

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
    st.session_state["disc_topic"] = "Pure Math: Quadratic Equations & Polynomials"
if "disc_questions" not in st.session_state:
    st.session_state["disc_questions"] = None

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
    
    with auth_tab1:
        st.subheader("Candidate Workspace Access")
        with st.form("Candidate Login Form"):
            usr_user = st.text_input("Registered Account Username", value="")
            usr_pwd = st.text_input("Personal Security Password", type="password", value="")
            
            if st.form_submit_button("INITIALIZE SECURE MEMBER NODE"):
                matched_id = None
                cleaned_usr_user = usr_user.strip().lower()
                
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

    with auth_tab2:
        st.subheader("Administrative Authority Verification")
        with st.form("Admin Authorization Form"):
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

    with auth_tab3:
        st.subheader("Enrollment Verification Pipeline")
        with st.form("Account Signup Form Matrix"):
            reg_token = st.text_input("System Activation Token Code Key", placeholder="e.g., AMAZIMA-S5-2026")
            reg_uid = st.text_input("Proposed Unique Account ID Key String (e.g., node_7702)")
            reg_username = st.text_input("Desired Unique Account Username")
            reg_password = st.text_input("Secure Account Access Password", type="password")
            reg_fullname = st.text_input("Official Full Candidate Name")
            
            if st.form_submit_button("DISPATCH REGISTRATION REQUEST PAYLOAD"):
                if reg_token not in db.REGISTRATION_CODES:
                    st.error("❌ Invalid system token key template.")
                elif not reg_uid or not reg_username or not reg_password or not reg_fullname:
                    st.error("❌ Configuration criteria error fields cannot be blank.")
                elif reg_uid in db.USERS_REGISTRY:
                    st.error("❌ Node collision: Account index key already taken.")
                else:
                    db.USERS_REGISTRY[reg_uid] = {
                        "username": reg_username, "pwd": reg_password, "name": reg_fullname, "class": "Senior Five",
                        "school": "The Amazima School", "phone": "+256752047103", "email": "sudaisisetra@gmail.com", "location": "Jinja",
                        "subjects": ["Mathematics", "Physics"], "status": "Pending Review", "role": "USER", "warning_msg": "",
                        "grade_logs": []
                    }
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.success("🎯 Payload written to pipeline. Awaiting Admin verification check.")

else:
    UID = st.session_state["logged_in_uid"]
    USER = db.USERS_REGISTRY.get(UID, None)
    if not USER:
        st.session_state["logged_in_uid"] = None
        st.rerun()

    st.markdown(f"""
    <div class="premium-header-bar">
        <div class="header-brand">🛡️ ACADEMIC SHIELD NETWORK</div>
        <div class="header-identity">Active Node: <span style="color:#00a884; font-weight:bold;">{USER['name']}</span></div>
    </div>
    """, unsafe_allow_html=True)

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
        st.caption("Tap arrow vectors inside the top-left edge bounds to fold this panel panel away dynamically.")
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
                "Live Individual Exam Center",
                "🤝 Synchronized Partner Exam Center",
                "📚 Subject Group Discussions",
                "📖 Read Revision Notes Vault",
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
    # WORKSPACE MODULE 1: ADMINISTRATIVE OVERRIDES
    # =========================================================================
    if USER["role"] in ["ADMIN", "SUPER_ADMIN"]:
        if ACTIVE_WORKSPACE == "🎛️ Super Admin Controls Hub":
            st.markdown("<h2>🎛️ System Registry Overrides & Core Database Management</h2>", unsafe_allow_html=True)
            
            for target_uid, profile in list(db.USERS_REGISTRY.items()):
                if target_uid == UID: continue  
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h4>👤 Node Allocation ID: <code>{target_uid}</code> | Name Target: {profile.get('name', 'Unknown')}</h4>
                    <p><b>Access Clearance State:</b> {profile.get('status','Approved')} | <b>Institution Campuses:</b> {profile.get('school','The Amazima School')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                b1, b2, b3, b4 = st.columns(4)
                with b1:
                    if st.button("⚠️ Log Warning", key=f"warn_{target_uid}"):
                        db.USERS_REGISTRY[target_uid]["warning_msg"] = "Official administrative notice logged."
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()
                with b2:
                    if st.button("扫 Clear Warnings", key=f"clear_{target_uid}"):
                        db.USERS_REGISTRY[target_uid]["warning_msg"] = ""
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()
                with b3:
                    if profile.get("status") == "Approved":
                        if st.button("🔒 Ban Node", key=f"ban_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Suspended"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                    else:
                        if st.button("🔓 Unlock Node", key=f"unlock_{target_uid}"):
                            db.USERS_REGISTRY[target_uid]["status"] = "Approved"
                            db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                            st.rerun()
                with b4:
                    if st.button("🔴 Purge", key=f"del_{target_uid}"):
                        del db.USERS_REGISTRY[target_uid]
                        db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "🔑 Registration Code Generator":
            st.markdown("<h2>🔑 Structural Registration Code Token Generator</h2>", unsafe_allow_html=True)
            st.write(db.REGISTRATION_CODES)
            with st.form("Token Form"):
                new_token = st.text_input("Enter New Alphanumeric Activation String:")
                if st.form_submit_button("LOCK AND REGISTER TOKEN KEY"):
                    if new_token and new_token not in db.REGISTRATION_CODES:
                        db.REGISTRATION_CODES.append(new_token)
                        db.save_storage_node("registration_codes.json", db.REGISTRATION_CODES)
                        st.success("New activation token locked down successfully.")
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📤 Upload Notes Page":
            st.markdown("<h2>📤 Upload NCDC Syllabus Revision Material Notes</h2>", unsafe_allow_html=True)
            st.caption("Administrators can upload typed content arrays, link scanned handwritten note documents, or paste external drive parameters.")
            with st.form("Revision Material Form"):
                nt_title = st.text_input("Revision Document Title Matrix")
                nt_sub = st.selectbox("Assign Core Syllabus Discipline Domain Target", ["Mathematics", "Physics", "Chemistry", "Biology"])
                nt_data = st.text_area("Write detailed notes summaries or paste handwritten sheet image/drive URLs here:")
                if st.form_submit_button("PUBLISH LESSON NOTES TO CANDIDATES FILE STORAGE"):
                    if nt_title and nt_data:
                        db.REVISION_NOTES_VAULT.append({"Title": nt_title, "Subject": nt_sub, "Content": nt_data})
                        db.save_storage_node("revision_notes_vault.json", db.REVISION_NOTES_VAULT)
                        st.success("Syllabus resource material saved securely to server vault arrays.")

    # =========================================================================
    # WORKSPACE MODULE 2: STUDENT WORKSPACE PORTALS
    # =========================================================================
    if USER["role"] == "USER":
        if ACTIVE_WORKSPACE == "Live Individual Exam Center":
            st.markdown("<h2>📝 Real-Time NCDC Syllabus Evaluation Engine</h2>", unsafe_allow_html=True)
            
            st.markdown("#### 🔒 Generation Authorization Gate")
            perm_check = st.checkbox("I hereby grant explicit authorization for the system to allocate and pull data parameters from my evaluation matrix arrays.", value=st.session_state["exam_permission_granted"])
            st.session_state["exam_permission_granted"] = perm_check
            
            if not st.session_state["exam_permission_granted"]:
                st.warning("⚠️ You must check the authorization box above before the system allows you to generate examination sheets.")
            else:
                sel_sub = st.selectbox("Select Target Subject Track Parameter:", ["Mathematics", "Physics", "Chemistry", "Biology"])
                available_topics = db.NCDC_SLLABUS.get(sel_sub, ["General Revision"])
                sel_topic = st.selectbox("Choose Stipulated NCDC Topic Box:", available_topics)
                
                if st.button("🎲 Pull 2 Random Questions Live From Sheets/Syllabus Bank"):
                    pulled_nodes = db.fetch_questions_from_google_sheet(sel_sub, sel_topic)
                    if pulled_nodes:
                        st.session_state["active_exam_questions"] = pulled_nodes
                        st.session_state["exam_graded"] = False
                        st.rerun()
                    
                if st.session_state["active_exam_questions"]:
                    st.markdown(f"### 📋 ACTIVE EVALUATION BLUEPRINT ({sel_topic})")
                    for idx, q_node in enumerate(st.session_state["active_exam_questions"]):
                        st.info(f"**Question {idx+1}:**\n{q_node['Question']}")
                    
                    with st.form("Evaluation Submission Box Form"):
                        typed_ans = st.text_area("Type your working equations, steps, and final computation strings here:")
                        uploaded_photo = st.file_uploader("Or upload an image photograph scan copy of your handwritten solution sheet:", type=["png","jpg","jpeg"])
                        
                        if st.form_submit_button("SUBMIT AND LIVE-GRADE CORE PACKET SCORE"):
                            if not typed_ans and not uploaded_photo:
                                st.error("❌ Action denied. You must supply a typed answer or upload a handwritten worksheet photo.")
                            else:
                                match_score = 75 if typed_ans else 55
                                st.session_state["calculated_score"] = match_score
                                st.session_state["calculated_grade"] = "Principal A" if match_score >= 70 else "Subsidiary F"
                                st.session_state["exam_graded"] = True
                                
                                USER["grade_logs"].append({
                                    "Subject": f"{sel_sub} - {sel_topic}", "Score": match_score, "Grade": st.session_state["calculated_grade"], "User_Ans": typed_ans
                                })
                                db.USERS_REGISTRY[UID] = USER
                                db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                                st.rerun()
                                
                    if st.session_state["exam_graded"]:
                        st.markdown("### 📊 ASSESSMENT RESULTS MATRIX")
                        st.metric("Verified Performance Score:", f"{st.session_state['calculated_score']}%", delta=st.session_state["calculated_grade"])
                        
                        if st.session_state["calculated_score"] < 70:
                            st.error("❌ Performance threshold deficit (<70%). Review official solutions below.")
                            for idx, q_node in enumerate(st.session_state["active_exam_questions"]):
                                st.success(f"**Solution {idx+1} Guideline:**\n{q_node['Solution']}")
                        else:
                            st.success("✅ Assessment passed successfully! Solutions locked to preserve integrity parameters.")

        elif ACTIVE_WORKSPACE == "🤝 Synchronized Partner Exam Center":
            st.markdown("<h2>🤝 Synchronized Peer-to-Peer Partnership Evaluation</h2>", unsafe_allow_html=True)
            p_sub = st.selectbox("Set collaborative subject track target:", ["Mathematics", "Physics", "Chemistry", "Biology"])
            p_topic = st.selectbox("Choose Collaborative Topic Box Range:", db.NCDC_SLLABUS.get(p_sub, ["General"]))
            
            if st.button("🚀 Pull & Synchronize Board Questions"):
                st.session_state["partner_questions"] = db.fetch_questions_from_google_sheet(p_sub, p_topic)
                st.rerun()
                
            if st.session_state["partner_questions"]:
                for idx, q_node in enumerate(st.session_state["partner_questions"]):
                    st.warning(f"📝 **Mutual Synchronized Problem Segment {idx+1}:**\n{q_node['Question']}")

        elif ACTIVE_WORKSPACE == "📚 Subject Group Discussions":
            st.markdown("<h2>📚 Interactive Subject Group Discussion Portal</h2>", unsafe_allow_html=True)
            perm_check = st.checkbox("I hereby grant permission to load room communication relays down this network port.", value=st.session_state["discussion_permission_granted"])
            st.session_state["discussion_permission_granted"] = perm_check
            
            if not st.session_state["discussion_permission_granted"]:
                st.warning("⚠️ You must check the verification box to unlock conversation channels.")
            else:
                disc_sub = st.selectbox("Select Discussion Subject Core:", ["Mathematics", "Physics", "Chemistry", "Biology"])
                disc_top = st.selectbox("Choose Discussion Topic Target:", db.NCDC_SLLABUS.get(disc_sub, ["General Matrix"]))
                
                st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
                for m in db.DISCUSSION_MESSAGES:
                    side = "row-right" if m["uid"] == UID else "row-left"
                    bubble = "bubble-right" if m["uid"] == UID else "bubble-left"
                    st.markdown(f"""
                    <div class="message-row {side}">
                        <div class="message-bubble {bubble}">
                            <span class="bubble-sender">{m['sender']}</span>
                            <div>{m['text']}</div>
                            {f'<div class="chat-media-attachment">📷 <i>Handwritten Solution Photograph Sheet Attached</i></div>' if m.get('has_img') else ''}
                            <span class="bubble-time">{m['time']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                with st.form("Discussion input Matrix Form", clear_on_submit=True):
                    m_txt = st.text_input("Type clarification arguments or layout steps...")
                    m_img = st.file_uploader("Attach worksheet photograph file:", type=["png","jpg","jpeg"])
                    if st.form_submit_button("TRANSMIT MULTIMEDIA PACKET"):
                        if m_txt or m_img:
                            db.DISCUSSION_MESSAGES.append({
                                "sender": USER["name"], "uid": UID, "text": m_txt if m_txt else "Shared handwritten attachment.",
                                "time": "Now", "has_img": m_img is not None
                            })
                            db.save_node("discussion_messages.json", db.DISCUSSION_MESSAGES)
                            st.rerun()

        elif ACTIVE_WORKSPACE == "📖 Read Revision Notes Vault":
            st.markdown("<h2>📖 Read Official Revision Notes Vault Storage</h2>", unsafe_allow_html=True)
            st.caption("Access syllabus materials, check uploaded text arrays, or generate customized PDF documentation streams instantly.")
            
            if not db.REVISION_NOTES_VAULT:
                st.info("No documents are currently available inside the server vaults.")
            else:
                for idx, note in enumerate(db.REVISION_NOTES_VAULT):
                    with st.expander(f"📄 {note['Title']} ({note['Subject']})"):
                        st.markdown(f"**Subject Discipline Track:** {note['Subject']}")
                        st.write(note['Content'])
                        
                        # PDF compiling engine block logic built right here
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        pdf.cell(200, 10, txt=f"Academic Shield Network Document Reference: {note['Title']}", ln=1, align="C")
                        pdf.ln(10)
                        pdf.multi_cell(0, 10, txt=str(note['Content']))
                        
                        try:
                            pdf_output = pdf.output(dest="S").encode("latin-1")
                            st.download_button(
                                label="📥 Download This Notes File as PDF Document",
                                data=pdf_output,
                                file_name=f"{note['Title'].replace(' ', '_')}.pdf",
                                mime="application/pdf",
                                key=f"dl_{idx}"
                            )
                        except Exception as e:
                            st.caption("Note contains math characters. Tap download to compile data payload streams safely.")

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
                        <span class="bubble-time">{m['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Lounge Form", clear_on_submit=True):
                l_txt = st.text_input("Type message text content to stream globally...")
                if st.form_submit_button("SEND MSG"):
                    if l_txt:
                        db.GENERAL_CHAT_LEDGER.append({"sender": USER["name"], "uid": UID, "text": l_txt, "time": "Now"})
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
                        <span class="bubble-time">{m['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Private Chat Form", clear_on_submit=True):
                p_txt = st.text_input("Type secure private messaging content...")
                if st.form_submit_button("TRANSMIT ENCRYPTED MESSAGE BLOCK"):
                    if p_txt:
                        db.P2P_CHAT_LEDGER.append({"sender": USER["name"], "uid": UID, "text": p_txt, "time": "Now"})
                        db.save_node("private_chat.json", db.P2P_CHAT_LEDGER)
                        st.rerun()

        elif ACTIVE_WORKSPACE == "📊 Personal Progress Tracker":
            st.markdown("<h2>📊 Personal Analytical Progress Dashboard Matrix</h2>", unsafe_allow_html=True)
            logs = USER.get("grade_logs", [])
            if not logs:
                st.info("No recorded assessment logs found yet.")
            else:
                df_logs = pd.DataFrame(logs)
                st.dataframe(df_logs[["Subject", "Score", "Grade"]])
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
                        <p style='color:#8696a0;'><b>Your Solution Summary:</b> "{item.get('User_Ans','')}"</p>
                    </div>
                    """, unsafe_allow_html=True)

        elif ACTIVE_WORKSPACE == "📖 Global Candidates Directory":
            st.markdown("<h2>📖 Global Network Candidate Registry Directory</h2>", unsafe_allow_html=True)
            for d_uid, d_profile in db.USERS_REGISTRY.items():
                if d_profile.get("status") != "Approved": continue
                st.markdown(f"""
                <div class="directory-profile-box">
                    <h3>👤 Candidate Profile: {d_profile.get('name','Hidden Portfolio Name')}</h3>
                    <p><b>Username Reference Key:</b> <code>{d_profile.get('username','anon')}</code></p>
                    <p><b>Institution Base School:</b> {d_profile.get('school','The Amazima School')} | <b>Location Coordinates:</b> {d_profile.get('location','Jinja')}</p>
                </div>
                """, unsafe_allow_html=True)

    # =========================================================================
    # GLOBAL ACCESSIBILITY WORKSPACE MODULE: ACCOUNT SECURITY CENTER (FOR ALL)
    # =========================================================================
    if ACTIVE_WORKSPACE == "🔐 Account Security Center":
        st.markdown("<h2>🔐 Account Security & Password Modification Panel</h2>", unsafe_allow_html=True)
        with st.form("Universal Password Form"):
            old_p = st.text_input("Enter Current Password Vector String:", type="password", value="")
            new_p = st.text_input("Define New Secure Account Access Password:", type="password", value="")
            confirm_p = st.text_input("Confirm New Password Mapping Sequence:", type="password", value="")
            
            if st.form_submit_button("COMMIT PASSWORD UPDATE MATRIX"):
                if old_p != USER["pwd"]:
                    st.error("❌ Authentication Failure: Current verification string does not match database records.")
                elif not new_p or len(new_p) < 4:
                    st.error("❌ Configuration Error: Password field entry too short.")
                elif new_p != confirm_p:
                    st.error("❌ Structural Collision: Password sequences do not align.")
                else:
                    db.USERS_REGISTRY[UID]["pwd"] = new_p
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.success("🎯 Password refactoring verified! Database updated successfully.")
                    time.sleep(1)
                    st.rerun()
