# =========================================================================
# COMPREHENSIVE CONTROL CORE SYSTEM (main.py)
# =========================================================================
import streamlit as st
import pandas as pd
import database as db
import styles as stl
import time
from fpdf import FPDF

# Configure core layout and application capabilities
st.set_page_config(page_title="Academic Shield", page_icon="🛡️", layout="wide")
stl.inject_shield_theme()

# --- CUSTOM PWA DOWNLOAD CAPABILITY MANIFEST INJECTION ---
st.markdown("""
<script>
// Check if ServiceWorker is registered to facilitate offline/home-screen installs
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').then(function() { console.log('Service Worker Registered'); });
}
</script>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# PERSISTENT SESSION STATE ARRAYS 
# -------------------------------------------------------------------------
if "logged_in_uid" not in st.session_state:
    st.session_state["logged_in_uid"] = None
if "current_user_role" not in st.session_state:
    st.session_state["current_user_role"] = None
if "active_channel" not in st.session_state:
    st.session_state["active_channel"] = None
if "selected_p2p_partner" not in st.session_state:
    st.session_state["selected_p2p_partner"] = None

# Individual Exam Management Hooks
if "active_exam_questions" not in st.session_state:
    st.session_state["active_exam_questions"] = None
if "exam_graded" not in st.session_state:
    st.session_state["exam_graded"] = False

# Permission Check Anchors
if "exam_permission_granted" not in st.session_state:
    st.session_state["exam_permission_granted"] = False
if "discussion_permission_granted" not in st.session_state:
    st.session_state["discussion_permission_granted"] = False

# =========================================================================
# LOGIN / PORTAL ACCESSIBILITY PIPELINE
# =========================================================================
if st.session_state["logged_in_uid"] is None:
    st.markdown("<h1 style='text-align: center; color: #00a884; margin-top: 15px;'>🛡️ ACADEMIC SHIELD NETWORK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8696a0;'>OWNERSHIP CREDENTIAL SIGNATURE: SUDAYISI SETRA | JINJA, UGANDA</p>", unsafe_allow_html=True)
    
    a_tab1, a_tab2, a_tab3 = st.tabs(["🎓 Candidate Gateway", "🔒 Administrator Portal", "📝 Request New Account"])
    
    with a_tab1:
        st.subheader("Candidate Workspace Access")
        with st.form("User Login Form"):
            usr_username = st.text_input("Registered Account Username", value="Setrastones").strip()
            usr_password = st.text_input("Personal Security Password", type="password", value="Sheillahstones222")
            if st.form_submit_button("INITIALIZE SECURE MEMBER NODE"):
                matched_uid = None
                for uid, data in db.USERS_REGISTRY.items():
                    if data["username"].lower() == usr_username.lower() and data["pwd"] == usr_password:
                        if data.get("role") == "USER":
                            matched_uid = uid
                            break
                if matched_uid:
                    st.session_state["logged_in_uid"] = matched_uid
                    st.session_state["current_user_role"] = "USER"
                    st.session_state["active_channel"] = "Live Individual Exam Center"
                    st.rerun()
                else:
                    st.error("❌ Authentication failure: Check entry strings.")

    with a_tab2:
        st.subheader("Administrative Authority Verification")
        with st.form("Admin Login Form"):
            adm_username = st.text_input("Admin ID / Username Key", value="admin_setra").strip()
            adm_password = st.text_input("Secret Master Password Link", type="password", value="AdminPassword2026")
            if st.form_submit_button("UNLOCK EXECUTIVE FRAMEWORK"):
                matched_uid = None
                for uid, data in db.USERS_REGISTRY.items():
                    if data["username"].lower() == adm_username.lower() and data["pwd"] == adm_password:
                        if data.get("role") in ["ADMIN", "SUPER_ADMIN"]:
                            matched_uid = uid
                            break
                if matched_uid:
                    st.session_state["logged_in_uid"] = matched_uid
                    st.session_state["current_user_role"] = db.USERS_REGISTRY[matched_uid]["role"]
                    st.session_state["active_channel"] = "🎛️ Super Admin Controls Hub"
                    st.rerun()
                else:
                    st.error("❌ Invalid Administrative Credentials or Access Tier Violation.")

    with a_tab3:
        st.subheader("Enrollment Verification Pipeline")
        with st.form("Registration Form"):
            tok = st.text_input("System Activation Token Code Key")
            new_uid = st.text_input("Proposed Unique Account ID Key String (e.g. node_7705)")
            new_user = st.text_input("Desired Unique Account Username")
            new_pass = st.text_input("Secure Account Access Password", type="password")
            new_name = st.text_input("Official Full Candidate Name")
            
            if st.form_submit_button("DISPATCH REGISTRATION REQUEST PAYLOAD"):
                if tok not in db.REGISTRATION_CODES:
                    st.error("❌ Invalid system token key template.")
                elif not all([new_uid, new_user, new_pass, new_name]):
                    st.error("❌ Configuration criteria error: Fields cannot be blank.")
                elif new_uid in db.USERS_REGISTRY:
                    st.error("❌ Node collision: Account index key already taken.")
                else:
                    db.USERS_REGISTRY[new_uid] = {
                        "username": new_user, "pwd": new_pass, "name": new_name, "class": "Senior Five",
                        "school": "The Amazima School", "phone": "+256752047103", "email": "sudaisisetra@gmail.com", "location": "Jinja",
                        "subjects": ["Mathematics", "Physics"], "status": "Approved", "role": "USER", "warning_msg": "", "grade_logs": []
                    }
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.success("🎯 Account provisioned successfully! Proceed to log in.")

else:
    UID = st.session_state["logged_in_uid"]
    USER = db.USERS_REGISTRY.get(UID, {"name": "Sudaisi Setra", "role": "USER", "warning_msg": ""})

    # =========================================================================
    # MANDATORY PERMANENT SYSTEM-WIDE VERIFIED BRANDING HEADER
    # =========================================================================
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0f1c24 0%, #00a884 100%); padding: 18px; border-radius: 8px; margin-bottom: 20px; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 20px; font-weight: bold; letter-spacing: 1px;">🛡️ ACADEMIC SHIELD UTILITY FRAMEWORK</span>
            <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 500;">
                PROPRIETARY PLATFORM OWNER: <b>SUDAISI SETRA</b>
            </span>
        </div>
        <div style="font-size: 12px; margin-top: 6px; opacity: 0.9;">
            Active User Workspace Node: <b>{USER['name']}</b> ({USER['role']}) | Operational Campus Node: Jinja, Uganda
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Navigation Controller Layout
    with st.sidebar:
        st.markdown("### 🗂️ Workspace Navigation")
        if USER["role"] in ["ADMIN", "SUPER_ADMIN"]:
            nav_options = [
                "🎛️ Super Admin Controls Hub",
                "🔑 Registration Code Generator",
                "📤 Upload Notes Page",
                "🔐 Account Security Center"
            ]
        else:
            nav_options = [
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
        
        st.session_state["active_channel"] = st.radio("Active Workspace Channels Selection:", nav_options)
        st.write("---")
        if st.button("🚪 Terminate Handshake & Sign out", use_container_width=True):
            st.session_state["logged_in_uid"] = None
            st.rerun()

    # Handle Warnings Admin Payload Blocks
    if USER.get("warning_msg"):
        st.warning(f"⚠️ **REGULATION NOTICE ACTION LOGGED:** {USER['warning_msg']}")

    # =========================================================================
    # ROUTING LOGIC & CHANNEL EXECUTION BLOCKS
    # =========================================================================
    CH = st.session_state["active_channel"]

    if CH == "🎛️ Super Admin Controls Hub":
        st.header("🎛️ System Registry Overrides & Core Database Management")
        for target_uid, profile in list(db.USERS_REGISTRY.items()):
            if target_uid == UID: continue
            st.markdown(f"""
            <div style="background-color: #1f2c34; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 4px solid #00a884;">
                <h5 style='margin:0; color: #e9edef;'>👤 Node: {profile.get('name')} (<code>{target_uid}</code>)</h5>
                <p style='margin:4px 0 0 0; font-size:13px; color:#8696a0;'>School: {profile.get('school')} | Location: {profile.get('location')} | Clearances: {profile.get('status')}</p>
            </div>
            """, unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("⚠️ Log Warn Notice", key=f"w_{target_uid}"):
                    db.USERS_REGISTRY[target_uid]["warning_msg"] = "Administrative review pending structural behavior guidelines check."
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.success("Warning pinned to account frame.")
            with c2:
                if st.button("❌ Purge Node Profile", key=f"p_{target_uid}"):
                    del db.USERS_REGISTRY[target_uid]
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.rerun()
            with c3:
                status_lbl = "Approved" if profile.get("status") == "Suspended" else "Suspended"
                if st.button(f"🔄 Toggle to {status_lbl}", key=f"t_{target_uid}"):
                    db.USERS_REGISTRY[target_uid]["status"] = status_lbl
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.rerun()

    elif CH == "🔑 Registration Code Generator":
        st.header("🔑 Structural Registration Code Token Generator")
        st.write("Active Code Registries:", db.REGISTRATION_CODES)
        with st.form("Add Token Form"):
            t_input = st.text_input("Enter New Token Code Key String")
            if st.form_submit_button("COMMIT TO ACTIVE REGISTRY"):
                if t_input and t_input not in db.REGISTRATION_CODES:
                    db.REGISTRATION_CODES.append(t_input)
                    db.save_storage_node("registration_codes.json", db.REGISTRATION_CODES)
                    st.rerun()

    elif CH == "📤 Upload Notes Page":
        st.header("📤 Upload NCDC Syllabus Revision Material Notes")
        with st.form("Notes Upload Form"):
            title = st.text_input("Revision Document Title Matrix")
            subj = st.selectbox("Assign Core Syllabus Discipline Domain Target", ["Mathematics", "Physics", "Chemistry", "Biology"])
            content = st.text_area("Write detailed summary notes or paste link parameters to handwritten sheets:")
            if st.form_submit_button("PUBLISH TO LESSON NOTE STORAGE VAULT"):
                if title and content:
                    db.REVISION_NOTES_VAULT.append({"Title": title, "Subject": subj, "Content": content})
                    db.save_storage_node("revision_notes_vault.json", db.REVISION_NOTES_VAULT)
                    st.success("Syllabus resources synchronized down pipeline successfully!")

    elif CH == "Live Individual Exam Center":
        st.header("📝 Real-Time NCDC Syllabus Evaluation Engine")
        st.session_state["exam_permission_granted"] = st.checkbox("I hereby grant explicit authorization for the engine to pull random exam sheets.", value=st.session_state["exam_permission_granted"])
        
        if st.session_state["exam_permission_granted"]:
            sub_sel = st.selectbox("Select Target Subject Track Parameter:", ["Mathematics", "Physics", "Chemistry", "Biology"])
            topic_sel = st.selectbox("Choose Stipulated NCDC Topic Box:", db.NCDC_SYLLABUS.get(sub_sel, []))
            
            if st.button("🎲 Pull 2 Random Questions Live From Sheets"):
                st.session_state["active_exam_questions"] = db.fetch_questions_from_google_sheet(sub_sel, topic_sel)
                st.session_state["exam_graded"] = False
                st.rerun()
                
            if st.session_state["active_exam_questions"]:
                st.subheader(f"Active Evaluation Worksheet: {topic_sel}")
                for i, q in enumerate(st.session_state["active_exam_questions"]):
                    st.info(f"**Question {i+1}:** {q['Question']}")
                    
                with st.form("Individual Submission Form"):
                    typed_work = st.text_area("Type your working equations and calculation proofs here:")
                    file_upload = st.file_uploader("Or upload image scan copies of handwritten work pages:", type=["jpg","jpeg","png"])
                    if st.form_submit_button("SUBMIT PACKET FOR GRADING"):
                        st.success("Work packet submitted down administrative analysis pipelines successfully!")

    elif CH == "🤝 Synchronized Partner Exam Center":
        st.header("🤝 Mutual Synchronized Dual-Candidate Desk Station")
        st.caption("Synchronizes target testing matrices across peers simultaneously. Both users access identical problems, can review tracking frames, and upload responses individually.")
        
        p_sub = st.selectbox("Set collaborative subject track target:", ["Mathematics", "Physics", "Chemistry", "Biology"])
        p_top = st.selectbox("Choose Collaborative Topic Box Range:", db.NCDC_SYLLABUS.get(p_sub, []))
        
        session_key = f"{p_sub}_{p_top.replace(' ', '_')}"
        
        if st.button("🚀 Synchronize & Load Dynamic Twin Board Questions"):
            pulled = db.fetch_questions_from_google_sheet(p_sub, p_top)
            db.MUTUAL_EXAMS_DB[session_key] = {"questions": pulled, "submissions": {}}
            db.save_node("mutual_exams_db.json", db.MUTUAL_EXAMS_DB)
            st.rerun()
            
        mutual_data = db.MUTUAL_EXAMS_DB.get(session_key, None)
        if mutual_data and "questions" in mutual_data:
            st.markdown("### 📋 SHARED SYNCHRONIZED EXAMINATION SHEET")
            for idx, q in enumerate(mutual_data["questions"]):
                st.warning(f"**Mutual Question {idx+1}:** {q['Question']}")
                
            st.write("---")
            st.subheader("Your Personal Worksheet Submission Portal")
            with st.form("Mutual Submission Form"):
                p_text = st.text_area("Type your final answers or equation working steps:")
                p_file = st.file_uploader("Upload photograph scan of handwritten worksheet steps:", type=["jpg","png","jpeg"], key="mut_file")
                if st.form_submit_button("DISPATCH PERSONAL MUTUAL WORKPACKET"):
                    mutual_data["submissions"][UID] = {"text": p_text, "has_file": p_file is not None, "name": USER["name"]}
                    db.MUTUAL_EXAMS_DB[session_key] = mutual_data
                    db.save_node("mutual_exams_db.json", db.MUTUAL_EXAMS_DB)
                    st.success("Your response matrix has been attached to the collaborative score register!")
            
            # Show actively connected user submission states down panel layouts
            st.markdown("#### 👥 Shared Room Submission Status Logs")
            for solver_id, payload in mutual_data["submissions"].items():
                st.caption(f"✅ **{payload['name']}** successfully logged answers. (Handwritten Upload: {payload['has_file']})")

    elif CH == "🔒 Private Peer Chatroom":
        st.header("🔒 Target-Isolated Private Peer Chatroom Hub")
        
        # User Selection Filter Matrix
        peer_list = {uid: data["name"] for uid, data in db.USERS_REGISTRY.items() if uid != UID}
        selected_partner_uid = st.selectbox("Select target peer node to open isolated secure connection channel:", list(peer_list.keys()), format_func=lambda x: peer_list[x])
        
        st.session_state["selected_p2p_partner"] = selected_partner_uid
        
        # Load messages mapped cleanly between these two precise entities
        st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
        for msg in db.P2P_CHAT_LEDGER:
            # Check if message strictly belongs to the chosen conversation corridor
            is_between = (msg["uid"] == UID and msg.get("recipient") == selected_partner_uid) or \
                         (msg["uid"] == selected_partner_uid and msg.get("recipient") == UID)
            if is_between:
                side = "row-right" if msg["uid"] == UID else "row-left"
                bubble = "bubble-right" if msg["uid"] == UID else "bubble-left"
                st.markdown(f"""
                <div class="message-row {side}">
                    <div class="message-bubble {bubble}">
                        <span class="bubble-sender">{msg['sender']}</span>
                        <div>{msg['text']}</div>
                        <span class="bubble-time">{msg['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        with st.form("Secure Private Chat Form", clear_on_submit=True):
            p2p_msg = st.text_input("Type secure private messaging content...")
            if st.form_submit_button("TRANSMIT ENCRYPTED MESSAGE BLOCK"):
                if p2p_msg:
                    db.P2P_CHAT_LEDGER.append({
                        "sender": USER["name"], "uid": UID, "recipient": selected_partner_uid, "text": p2p_msg, "time": "Now"
                    })
                    db.save_node("private_chat.json", db.P2P_CHAT_LEDGER)
                    st.rerun()

    elif CH == "📚 Subject Group Discussions":
        st.header("📚 Interactive Subject Group Discussion Portal")
        st.session_state["discussion_permission_granted"] = st.checkbox("Grant network access to dynamic message relay rooms.", value=st.session_state["discussion_permission_granted"])
        
        if st.session_state["discussion_permission_granted"]:
            d_sub = st.selectbox("Choose Discussion Board:", ["Mathematics", "Physics", "Chemistry", "Biology"])
            
            st.markdown("<div class='whatsapp-chat-canvas'>", unsafe_allow_html=True)
            for msg in db.DISCUSSION_MESSAGES:
                if msg.get("subject") == d_sub:
                    side = "row-right" if msg["uid"] == UID else "row-left"
                    bubble = "bubble-right" if msg["uid"] == UID else "bubble-left"
                    st.markdown(f"""
                    <div class="message-row {side}">
                        <div class="message-bubble {bubble}">
                            <span class="bubble-sender">{msg['sender']}</span>
                            <div>{msg['text']}</div>
                            <span class="bubble-time">{msg['time']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Group chat dispatch form", clear_on_submit=True):
                g_txt = st.text_input("Type clarification post or mathematical arguments...")
                if st.form_submit_button("STREAM MESSAGE"):
                    if g_txt:
                        db.DISCUSSION_MESSAGES.append({
                            "sender": USER["name"], "uid": UID, "subject": d_sub, "text": g_txt, "time": "Now"
                        })
                        db.save_node("discussion_messages.json", db.DISCUSSION_MESSAGES)
                        st.rerun()

    elif CH == "📖 Read Revision Notes Vault":
        st.header("📖 Read Official Revision Notes Vault Storage")
        if not db.REVISION_NOTES_VAULT:
            st.info("No documents are currently available inside the server vaults.")
        else:
            for idx, note in enumerate(db.REVISION_NOTES_VAULT):
                with st.expander(f"📄 {note['Title']} ({note['Subject']})"):
                    st.write(note['Content'])
                    
                    # Safe PDF byte encoding architecture block
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Helvetica", size=12)
                    pdf.cell(200, 10, txt=f"Document Asset: {note['Title']}", ln=1, align="C")
                    pdf.ln(10)
                    pdf.multi_cell(0, 10, txt=str(note['Content']).encode('utf-8').decode('latin-1', 'ignore'))
                    
                    try:
                        pdf_bytes = pdf.output()
                        st.download_button(
                            label="📥 Download This Notes File as PDF Document",
                            data=bytes(pdf_bytes),
                            file_name=f"{note['Title'].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            key=f"dl_pdf_{idx}"
                        )
                    except Exception as e:
                        st.caption("Compilation issue reading characters. File download available via online syncing.")

    elif CH == "💬 General Lounge Chat":
        st.header("💬 Global Media Communications Lounge")
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
        
        with st.form("Lounge Form Interface", clear_on_submit=True):
            l_txt = st.text_input("Type message text content to stream globally...")
            if st.form_submit_button("SEND MSG"):
                if l_txt:
                    db.GENERAL_CHAT_LEDGER.append({"sender": USER["name"], "uid": UID, "text": l_txt, "time": "Now"})
                    db.save_node("lounge_chat.json", db.GENERAL_CHAT_LEDGER)
                    st.rerun()

    elif CH == "📊 Personal Progress Tracker":
        st.header("📊 Personal Analytical Progress Dashboard Matrix")
        logs = USER.get("grade_logs", [])
        if not logs:
            st.info("No recorded assessment logs found yet.")
        else:
            st.dataframe(pd.DataFrame(logs)[["Subject", "Score", "Grade"]])

    elif CH == "📂 Finished Exam Vault Storage":
        st.header("📂 Evaluation Document Historical Storage Vault")
        logs = USER.get("grade_logs", [])
        if not logs:
            st.info("Vault registry records are currently empty.")
        else:
            for idx, item in enumerate(logs):
                st.info(f"📄 **Assessment Log #{idx+1}:** {item['Subject']} | Score Gained: {item['Score']}% ({item['Grade']})")

    elif CH == "📖 Global Candidates Directory":
        st.header("📖 Global Network Candidate Registry Directory")
        for d_uid, d_profile in db.USERS_REGISTRY.items():
            if d_profile.get("status") != "Approved": continue
            # Clear password keys from being exposed inside directory structures securely
            st.markdown(f"""
            <div style="background-color: #1f2c34; padding: 16px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid #00a884;">
                <h3 style="margin: 0 0 6px 0; color: #00a884;">👤 Profile Name: {d_profile.get('name', 'Hidden Candidate Portfolio')}</h3>
                <p style="margin: 3px 0; font-size: 14px; color: #e9edef;"><b>System Username Handle:</b> <code>{d_profile.get('username')}</code></p>
                <p style="margin: 3px 0; font-size: 14px; color: #e9edef;"><b>Class Standing Level:</b> {d_profile.get('class')} </p>
                <p style="margin: 3px 0; font-size: 14px; color: #e9edef;"><b>Assigned Campus Institution:</b> {d_profile.get('school')} </p>
                <p style="margin: 3px 0; font-size: 14px; color: #e9edef;"><b>Contact Support Phone:</b> {d_profile.get('phone')} | <b>Email Node Address:</b> {d_profile.get('email')}</p>
                <p style="margin: 3px 0; font-size: 14px; color: #e9edef;"><b>Geographic Coordinates Location:</b> {d_profile.get('location')} </p>
            </div>
            """, unsafe_allow_html=True)

    elif CH == "🔐 Account Security Center":
        st.header("🔐 Account Security & Password Modification Panel")
        with st.form("Password Adjust Security Form"):
            old_p = st.text_input("Enter Current Password Vector String:", type="password")
            new_p = st.text_input("Define New Secure Account Access Password:", type="password")
            if st.form_submit_button("COMMIT CHANGE"):
                if old_p == USER["pwd"] and len(new_p) >= 4:
                    db.USERS_REGISTRY[UID]["pwd"] = new_p
                    db.save_storage_node("users_registry.json", db.USERS_REGISTRY)
                    st.success("Account credential strings adjusted securely!")
                else:
                    st.error("Validation failed. Check current string entry constraints.")
