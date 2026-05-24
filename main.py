import streamlit as st
import pandas as pd
import random
import time

# Import configuration layers from your modular backend
from styles import inject_whatsapp_styles
from database import (
    NCDC_CURRICULUM_MAP,
    AVATAR_OPTIONS,
    DEFAULT_SUDAISI_IMAGE,
    get_east_timestamp,
    read_public_sheet,
    save_cache_to_disk,
    load_cache_from_disk,
    initialize_global_states,
    create_blank_progress_card,
    push_system_notification
)

# Boot data directories and apply layout style engine
initialize_global_states()
inject_whatsapp_styles()

# Extra stability states for advanced system functions
if "logged_in_uid" not in st.session_state:
    st.session_state["logged_in_uid"] = None
if "discussion_leaders" not in st.session_state:
    st.session_state["discussion_leaders"] = load_cache_from_disk("db_leaders.json", {})

# Calibrated A-Level National Principal Scale Grading Engine
def compute_ugandan_grade(score):
    if score >= 80: return "Principal A (Excellent)"
    elif score >= 70: return "Principal B (Very Good)"
    elif score >= 60: return "Principal C (Good)"
    elif score >= 50: return "Principal D (Satisfactory)"
    elif score >= 40: return "Principal E (Pass)"
    elif score >= 35: return "O (Subsidiary Pass)"
    else: return "F (Fail)"

# =========================================================================
# GATEWAY TERMINAL (ADJUSTED TO YOUR EXACT CHANNELS & VISIBILITY)
# =========================================================================
if st.session_state["logged_in_uid"] is None:
    st.markdown("<h1 style='text-align: center; color: #ff3333;'>🛡️ ACADEMIC SHIELD NETWORK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Ugandan Advanced Curriculum Portal & Core Database</p>", unsafe_allow_html=True)
    
    auth_mode = st.radio(
        "Select Portal Action Gate:", 
        ["🔑 System Security Login", "🛡️ System Administrator Hub", "📝 Create Candidate Account"], 
        horizontal=False
    )
    
    # SECTION 1: STANDARD STUDENT LOGIN
    if auth_mode == "🔑 System Security Login":
        st.markdown("### 🔓 Enter Active Credentials")
        with st.form("Student Login Terminal"):
            input_username = st.text_input("Username / ID Coordinate")
            input_password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("AUTHORIZE SYSTEM ACCESS")
            
            if submit_login:
                found_uid = None
                for uid, data in st.session_state["users_registry"].items():
                    if data.get("username") == input_username and data.get("pwd") == input_password:
                        if data.get("role") in ["ADMIN", "SUPER_ADMIN"]:
                            st.error("🚫 Administrative accounts must use the System Administrator Hub gate.")
                            st.stop()
                        found_uid = uid
                        break
                
                if found_uid:
                    user_node = st.session_state["users_registry"][found_uid]
                    if user_node.get("status", "Approved") == "Suspended":
                        st.error("🚫 Access Revoked. Account suspended.")
                    elif user_node.get("status", "Approved") == "Pending Review":
                        st.warning("⏳ Verification Pending. Please await Admin clearance.")
                    else:
                        st.session_state["logged_in_uid"] = found_uid
                        st.success(f"🔓 Access Granted.")
                        st.rerun()
                else:
                    st.error("❌ Authentication Failed. Double-check your credentials.")
                    
    # SECTION 2: ADMIN LOGIN TERMINAL
    elif auth_mode == "🛡️ System Administrator Hub":
        st.markdown("### 🛡️ Administrative Secure Command Center")
        with st.form("Admin Core Login Terminal"):
            admin_username = st.text_input("Admin Username / ID Code Token")
            admin_password = st.text_input("Master System Password", type="password")
            submit_admin = st.form_submit_button("UNLOCK ADMIN METRICS")
            
            if submit_admin:
                found_uid = None
                for uid, data in st.session_state["users_registry"].items():
                    if data.get("username") == admin_username and data.get("pwd") == admin_password:
                        if data.get("role") in ["ADMIN", "SUPER_ADMIN"]:
                            found_uid = uid
                            break
                
                if found_uid:
                    st.session_state["logged_in_uid"] = found_uid
                    st.success("⚡ Master Clearance Granted.")
                    st.rerun()
                else:
                    st.error("❌ Cryptographic Error: Invalid Admin Credentials.")

    # SECTION 3: CANDIDATE REGISTRATION INTAKE
    elif auth_mode == "📝 Create Candidate Account":
        st.markdown("### 📝 New Registration Intake")
        with st.form("Registration Intake Module"):
            reg_code = st.text_input("Access Validation Code")
            reg_uid = st.text_input("User ID Code Token (4 Digits)")
            reg_user = st.text_input("Username")
            reg_pwd = st.text_input("Password", type="password")
            reg_name = st.text_input("Full Official Name")
            reg_class = st.selectbox("Academic Level Class", ["Senior Five", "Senior Six"])
            reg_school = st.text_input("Institution Name", value="The Amazima School")
            
            selected_subs = st.multiselect("Enrolled Academic Subjects", list(NCDC_CURRICULUM_MAP.keys()), default=["Mathematics"])
            submit_reg = st.form_submit_button("SUBMIT REGISTRATION APPLICATION")
            
            if submit_reg:
                if reg_code not in st.session_state["generated_registration_codes"]:
                    st.error("❌ Invalid Key Code.")
                elif reg_uid in st.session_state["users_registry"]:
                    st.error("❌ ID Collision: Token already registered.")
                else:
                    new_profile = {
                        "username": reg_user, "pwd": reg_pwd, "name": reg_name, "class": reg_class,
                        "school": reg_school, "status": "Pending Review", "warning_msg": "", 
                        "avatar": random.choice(AVATAR_OPTIONS), "partner": "", "partner_role": "Standalone", 
                        "role": "USER", "subjects": selected_subs, "progress": create_blank_progress_card(selected_subs)
                    }
                    st.session_state["users_registry"][reg_uid] = new_profile
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success("🎯 Application sent to Admin review loop.")

else:
    CURRENT_USER_ID = st.session_state["logged_in_uid"]
    USER_DATA = st.session_state["users_registry"].get(CURRENT_USER_ID, {})
    
    if not USER_DATA:
        st.session_state["logged_in_uid"] = None
        st.rerun()

    # =========================================================================
    # DUAL-COLUMN WORKSPACE VIEWPORT (FIXES MOBILE SCREEN HIDDEN SIDEBARS)
    # =========================================================================
    st.markdown(f"### 🛡️ Welcome, {USER_DATA.get('name')} | `{USER_DATA.get('role')}`")
    
    # Render Warning banners globally on top if any exist
    if USER_DATA.get("warning_msg"):
        st.markdown(f"<div style='background-color:#ff3333;color:white;padding:10px;margin-bottom:10px;'>⚠️ ALERT: {USER_DATA.get('warning_msg')}</div>", unsafe_allow_html=True)

    # Force continuous open structure split layout
    menu_col, content_col = st.columns([1, 2])
    
    with menu_col:
        st.markdown("### 🗺️ Workspace Channels")
        
        navigation_nodes = [
            "📝 Access Exam Center",
            "🤝 Synchronized Partner Exam Center",
            "📚 Read Revision Notes",
            "💬 General Lounge Chat",
            "🔒 Private Peer Chatroom",
            "📊 Progress Tracker Logs",
            "📂 Finished Exam Vault",
            "📚 Subject Group Discussions",
            "🤝 Partner Connection Hub"
        ]
        
        if USER_DATA.get("role") in ["ADMIN", "SUPER_ADMIN"]:
            navigation_nodes.append("⚙️ Super Admin Operations")
            
        selected_workspace = st.radio("Navigate Node Channels:", navigation_nodes, label_visibility="collapsed")
        
        # Intercom quick hand raiser feature below menus
        st.write("---")
        my_hand_raised = st.session_state["raised_hands"].get(CURRENT_USER_ID, False)
        if my_hand_raised:
            if st.button("⬇️ LOWER MY HAND", type="primary"):
                st.session_state["raised_hands"][CURRENT_USER_ID] = False
                save_cache_to_disk("db_hands.json", st.session_state["raised_hands"])
                st.rerun()
        else:
            if st.button("✋ RAISE INTERCOM HAND"):
                st.session_state["raised_hands"][CURRENT_USER_ID] = True
                save_cache_to_disk("db_hands.json", st.session_state["raised_hands"])
                st.rerun()
                
        st.write("---")
        if st.button("🔴 DISCONNECT SESSION"):
            st.session_state["logged_in_uid"] = None
            st.rerun()

    with content_col:
        # 📝 ACCESS EXAM CENTER INTERFACE
        if selected_workspace == "📝 Access Exam Center":
            st.markdown("<h2>📝 Live Microsecond Metric Assessment Node</h2>", unsafe_allow_html=True)
            
            fallback_quiz = pd.DataFrame([
                {"Question": "Factorize completely the cubic expression: $x^3 - 6x^2 + 11x - 6 = 0$. Determine correct roots.", "OptionA": "1, 2, 3", "OptionB": "-1, -2, -3", "OptionC": "0, 1, 5", "OptionD": "2, 4, 6", "Answer": "A", "Solution": "By factor theorem, testing x=1 gives 0. Long division results in (x-1)(x-2)(x-3)=0. Therefore, the roots are exactly 1, 2, and 3."},
                {"Question": "A particle progresses along a linear vector with displacement $s = t^3 - 3t^2 + 2$. Evaluate acceleration at $t=3$ seconds.", "OptionA": "6 m/s^2", "OptionB": "12 m/s^2", "OptionC": "18 m/s^2", "OptionD": "24 m/s^2", "Answer": "B", "Solution": "Velocity v = ds/dt = 3t^2 - 6t. Acceleration a = dv/dt = 6t - 6. Substituting t=3 yields a = 6(3) - 6 = 12 m/s^2."}
            ])
            quiz_df = read_public_sheet("QuizBank")
            if quiz_df is None or quiz_df.empty: quiz_df = fallback_quiz

            if "exam_running" not in st.session_state: st.session_state["exam_running"] = False
            if "start_epoch" not in st.session_state: st.session_state["start_epoch"] = 0.0

            if not st.session_state["exam_running"]:
                if st.button("🚀 BOOT HIGH-PRECISION EVALUATION LOOP"):
                    st.session_state["exam_running"] = True
                    st.session_state["start_epoch"] = time.time()
                    st.rerun()
            else:
                elapsed = time.time() - st.session_state["start_epoch"]
                st.write(f"⏱️ Counter: `{elapsed:.4f} seconds elapsed`")
                
                submission_type = st.radio("Submission Execution Mode:", ["🔤 Typed Input Option", "✍️ Handwritten Document Link Reference"], horizontal=True)
                
                with st.form("Exam Questionnaire Blueprint"):
                    user_selections = {}
                    for idx, row in quiz_df.iterrows():
                        st.markdown(f"#### Q{idx+1}: {row['Question']}")
                        if submission_type == "🔤 Typed Input Option":
                            opts = [f"A) {row['OptionA']}", f"B) {row['OptionB']}", f"C) {row['OptionC']}", f"D) {row['OptionD']}"]
                            user_selections[idx] = st.radio(f"Select Choice Q{idx+1}:", opts, key=f"qm_{idx}")
                        else:
                            user_selections[idx] = st.text_input(f"Handwritten Solution Link Q{idx+1}:", placeholder="Paste Cloud Storage URL...", key=f"hw_{idx}")
                    
                    if st.form_submit_button("🔒 LOCK ANSWERS AND CALCULATE"):
                        total_time = time.time() - st.session_state["start_epoch"]
                        st.session_state["exam_running"] = False
                        
                        correct = 0
                        breakdown = []
                        for idx, row in quiz_df.iterrows():
                            if submission_type == "🔤 Typed Input Option":
                                chosen = user_selections[idx].split(")")[0].strip()
                            else:
                                chosen = "A" if user_selections[idx] else "FAIL_NO_SUBMISSION"
                                
                            ans = str(row['Answer']).strip()
                            ok = (chosen == ans)
                            if ok: correct += 1
                            breakdown.append({
                                "Item": f"Question {idx+1}", 
                                "Your Entry": user_selections[idx] if submission_type != "🔤 Typed Input Option" else chosen, 
                                "Correct Key": ans, 
                                "Status": "PASS" if ok else "💥 MISFIRED AREA", 
                                "Traceback Explanation": row['Solution']
                            })
                        
                        st.session_state["last_score"] = (correct / len(quiz_df)) * 100
                        st.session_state["last_breakdown"] = breakdown
                        st.session_state["last_exam_time"] = total_time
                        st.rerun()

            if "last_score" in st.session_state:
                u_grade = compute_ugandan_grade(st.session_state["last_score"])
                st.markdown(f"### Score Summary: **{st.session_state['last_score']:.2f}%** | Grade: **{u_grade}**")
                st.caption(f"Processed in {st.session_state.get('last_exam_time', 0.0):.4f} microseconds/seconds loop.")
                
                st.markdown("#### ⚡ Microsecond Instant Solutions Feedback Matrix")
                for item in st.session_state["last_breakdown"]:
                    if item["Status"] == "💥 MISFIRED AREA":
                        st.error(f"❌ **{item['Item']} Misfired!** Correct Target: `{item['Correct Key']}`")
                        st.info(f"💡 **Correction Logic:** {item['Traceback Explanation']}")
                    else:
                        st.success(f"✅ **{item['Item']} Passed!** Solutions verified perfectly.")
                
                # Downloadable Done Exams Engine
                report_data = f"Shield Exam Summary Report\nScore: {st.session_state['last_score']}%\nGrade: {u_grade}"
                st.download_button("📥 DOWNLOAD COMPLETED SCRIPT SKELETON", data=report_data, file_name="Exam_Script_Report.txt")

        # 🤝 PARTNER SYNC EXAMINATION RECEIVER 
        elif selected_workspace == "🤝 Synchronized Partner Exam Center":
            st.markdown("<h2>🤝 Incoming Peer Failed Alignment Verification Check</h2>", unsafe_allow_html=True)
            my_shared = st.session_state["shared_exams"].get(CURRENT_USER_ID, [])
            if not my_shared:
                st.info("No failed metric logs routed from your synchronized sync partner.")
            else:
                for report in my_shared:
                    with st.expander(f"⚠️ Deficit Script from {report['from_name']} ── Score: {report['score']:.1f}%"):
                        st.dataframe(pd.DataFrame(report["data"]))

        # 📚 READ REVISION NOTES VAULT
        elif selected_workspace == "📚 Read Revision Notes":
            st.markdown("<h2>📂 Shared Document and Reference Cloud Center</h2>", unsafe_allow_html=True)
            for doc in st.session_state.get("revision_notes_db", []):
                st.info(f"**📌 {doc['Subject']} | {doc['Title']}**\n\n{doc['Content']}")

        # 💬 WHATSAPP GENERAL LOUNGE CHAT
        elif selected_workspace == "💬 General Lounge Chat":
            st.markdown("<h2>🌍 Global WhatsApp Lounge Communication Space</h2>", unsafe_allow_html=True)
            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            for msg in st.session_state.get("general_chat", []):
                is_me = (msg.get("sender") == USER_DATA.get("name"))
                cls = "chat-right" if is_me else "chat-left"
                st.markdown(f"<div class='chat-bubble {cls}'><b>{msg.get('sender')}</b><br>{msg.get('text')}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Lounge Form Chat Send", clear_on_submit=True):
                txt = st.text_input("Type Lounge Chat Message...")
                if st.form_submit_button("TRANSMIT MSG"):
                    if txt:
                        st.session_state["general_chat"].append({"sender": USER_DATA.get("name"), "text": txt, "timestamp": get_east_timestamp()})
                        save_cache_to_disk("db_genchat.json", st.session_state["general_chat"])
                        st.rerun()

        # 🔒 PRIVATE PEER CHATROOM MATRIX
        elif selected_workspace == "🔒 Private Peer Chatroom":
            st.markdown("<h2>🔒 Private Peer-to-Peer Link Channel</h2>", unsafe_allow_html=True)
            pid = USER_DATA.get("partner", "")
            if not pid: 
                st.warning("⚠️ No synchronized partner linked to your profile workspace node.")
            else:
                p_prof = st.session_state["users_registry"].get(pid, {})
                for msg in st.session_state.get("private_chats", []):
                    if msg.get("sender") in [USER_DATA.get("name"), p_prof.get("name")]:
                        st.write(f"**{msg.get('sender')}**: {msg.get('text')}")
                
                with st.form("Private Input Send Box", clear_on_submit=True):
                    ptxt = st.text_input("Send Private Message...")
                    if st.form_submit_button("SEND RECON ENCRYPTED"):
                        if ptxt:
                            st.session_state["private_chats"].append({"sender": USER_DATA.get("name"), "text": ptxt})
                            save_cache_to_disk("db_p2pchat.json", st.session_state["private_chats"])
                            st.rerun()

        # 📊 PROGRESS TRACKER SYLLABUS MATRIX
        elif selected_workspace == "📊 Progress Tracker Logs":
            st.markdown("<h2>📊 Personal Progress Tracker</h2>", unsafe_allow_html=True)
            user_progress = USER_DATA.get("progress", {})
            for sub in USER_DATA.get("subjects", ["Mathematics"]):
                st.subheader(f"Module Coverage: {sub}")
                st.write(user_progress.get(sub, "No metric entry mapped yet."))

        # 📂 FINISHED EXAM VAULT STORAGE NODE
        elif selected_workspace == "📂 Finished Exam Vault":
            st.markdown("<h2>📂 Historical Assessment Vault Records</h2>", unsafe_allow_html=True)
            if "last_score" in st.session_state:
                st.metric("Your Last High-Precision Score", f"{st.session_state['last_score']:.2f}%")
            else:
                st.info("No active session files recorded in microsecond local execution cache layers.")

        # 📚 SUBJECT GROUP SEPARATE STREAM CLUSTER
        elif selected_workspace == "📚 Subject Group Discussions":
            st.markdown("<h2>📚 Subject Group Discussion Streams</h2>", unsafe_allow_html=True)
            user_subs = USER_DATA.get("subjects", ["Mathematics"])
            selected_group = st.selectbox("Active Subject Frequency:", user_subs)
            
            assigned_leader = st.session_state["discussion_leaders"].get(selected_group, "None Appointed Yet")
            st.success(f"👑 Appointed Session Leader Coordinator: **{assigned_leader}**")
            
            # Interactive Text box slots for broadcasting inside a subject field
            if selected_group not in st.session_state["subject_chats"]:
                st.session_state["subject_chats"][selected_group] = []
                
            with st.form("Subject Stream Transmit Form", clear_on_submit=True):
                stream_txt = st.text_input(f"Send data packet to {selected_group} room...")
                if st.form_submit_button("BROADCAST"):
                    if stream_txt:
                        st.session_state["subject_chats"][selected_group].append({
                            "sender": USER_DATA.get("name"), "text": stream_txt, "timestamp": get_east_timestamp()
                        })
                        save_cache_to_disk("db_subchat.json", st.session_state["subject_chats"])
                        st.rerun()

        # 🤝 COLLABORATION PAIRING CONTROL INTERFACE
        elif selected_workspace == "🤝 Partner Connection Hub":
            st.markdown("<h2>🤝 Academic Collaboration Framework</h2>", unsafe_allow_html=True)
            pid = USER_DATA.get("partner", "")
            if pid:
                p_node = st.session_state["users_registry"].get(pid, {})
                st.success(f"🔗 Paired Node: {p_node.get('name')} | Mode: `{USER_DATA.get('partner_role')}`")
            else:
                st.info("No synchronized handshake verified. Connect profiles to activate partner verification center metrics.")

        # ⚙️ SUPER ADMINISTRATIVE SUBSYSTEM MODULATIONS
        elif selected_workspace == "⚙️ Super Admin Operations" and USER_DATA.get("role") in ["ADMIN", "SUPER_ADMIN"]:
            st.markdown("<h2>⚙️ Administrator Operations Dashboard Console</h2>", unsafe_allow_html=True)
            
            # Session Leader Appointer Logic Block
            st.markdown("### 💼 Appointment Matrix Section")
            all_subjects_list = ["Mathematics", "Physics", "Chemistry", "Biology"]
            target_sub_select = st.selectbox("Choose Field Group:", all_subjects_list)
            user_nodes_list = [node.get("name") for uid, node in st.session_state["users_registry"].items()]
            chosen_leader_node = st.selectbox("Appoint Session Leader Node Candidate:", user_nodes_list)
            
            if st.button("🔒 AUTHORIZE SESSION LEADER ASSIGNMENT"):
                st.session_state["discussion_leaders"][target_sub_select] = chosen_leader_node
                save_cache_to_disk("db_leaders.json", st.session_state["discussion_leaders"])
                st.success(f"Successfully locked {chosen_leader_node} as {target_sub_select} field coordinator.")
                st.rerun()

# Dynamic Platform Branding System Footer Component
st.markdown("""
<div style='text-align: center; margin-top: 50px;'>
    <p style='color: #444; font-size: 11px;'>🛡️ Academic Shield Network Infrastructure Engine v4.26 • Core Engineering Configured by Sudaisi Setra</p>
</div>
""", unsafe_allow_html=True)
