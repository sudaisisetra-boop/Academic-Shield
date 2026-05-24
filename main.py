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
    initialize_global_states,
    create_blank_progress_card,
    push_system_notification
)

# Boot data directories and apply layout style engine
initialize_global_states()
inject_whatsapp_styles()

if "logged_in_uid" not in st.session_state:
    st.session_state["logged_in_uid"] = None

# =========================================================================
# GATEWAY TERMINAL (LOGIN & REGISTRATION SIGN-IN)
# =========================================================================
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
                        st.success(f"🔓 Access Granted. Welcome back, {user_node.get('name')}.")
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
                    new_profile = {
                        "username": reg_user, "pwd": reg_pwd, "name": reg_name, "class": reg_class,
                        "school": reg_school, "phone": reg_phone, "email": reg_email, "gender": reg_gender,
                        "location": reg_loc, "subjects": selected_subs, "status": "Pending Review",
                        "warning_msg": "", "avatar": random.choice(AVATAR_OPTIONS), "partner": "",
                        "partner_role": "Standalone", "role": "USER", "progress": create_blank_progress_card(selected_subs)
                    }
                    st.session_state["users_registry"][reg_uid] = new_profile
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success("🎯 Account submitted! Await Admin Activation.")

else:
    CURRENT_USER_ID = st.session_state["logged_in_uid"]
    USER_DATA = st.session_state["users_registry"].get(CURRENT_USER_ID, {})
    
    if not USER_DATA:
        st.session_state["logged_in_uid"] = None
        st.rerun()

    # =========================================================================
    # SIDEBAR TERMINAL CONTROL PANEL
    # =========================================================================
    with st.sidebar:
        st.markdown(f"<h3 style='color: #ff3333;'>🛡️ SHIELD TERMINAL</h3>", unsafe_allow_html=True)
        
        avatar_src = USER_DATA.get("avatar", AVATAR_OPTIONS[0])
        if avatar_src == "SUDAISI_BAKED":
            avatar_src = st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE)
            
        st.image(avatar_src, width=85)
        st.markdown(f"**User:** {USER_DATA.get('name')}")
        st.markdown(f"**Role:** `{USER_DATA.get('role')}`")
        
        # Google Meet Quick Hand Controller
        st.write("---")
        st.markdown("**🖐️ Google Meet Classroom Intercom**")
        my_hand_raised = st.session_state["raised_hands"].get(CURRENT_USER_ID, False)
        
        if my_hand_raised:
            if st.button("⬇️ LOWER HAND", type="primary"):
                st.session_state["raised_hands"][CURRENT_USER_ID] = False
                save_cache_to_disk("db_hands.json", st.session_state["raised_hands"])
                st.rerun()
        else:
            if st.button("✋ RAISE HAND"):
                st.session_state["raised_hands"][CURRENT_USER_ID] = True
                save_cache_to_disk("db_hands.json", st.session_state["raised_hands"])
                st.rerun()
                
        if USER_DATA.get("warning_msg"):
            st.markdown(f"<div class='system-warn-box'>⚠️ ADMIN ALERT:<br>{USER_DATA.get('warning_msg')}</div>", unsafe_allow_html=True)
            
        st.write("---")
        
        navigation_nodes = [
            "📋 Operational Dashboard", "📊 Personal Progress Tracker",
            "📝 Revision Center & Mock Vault", "💬 WhatsApp Lounge Chat", 
            "📚 Subject Group Discussions", "🤝 Partner Connection Hub"
        ]
        
        if USER_DATA.get("role") in ["ADMIN", "SUPER_ADMIN"]:
            navigation_nodes.append("⚙️ Super Admin Operations")
            
        selected_workspace = st.radio("Navigate Workspace Channels:", navigation_nodes)
        
        st.write("---")
        if st.button("🔴 SECURE LOGOUT"):
            st.session_state["logged_in_uid"] = None
            st.rerun()

    # =========================================================================
    # CORE INTERFACE WORKSPACE ROUTING
    # =========================================================================
    
    # 📋 DASHBOARD HUB PANEL
    if selected_workspace == "📋 Operational Dashboard":
        st.markdown("<h2>📋 Operational Candidate Dashboard</h2>", unsafe_allow_html=True)
        for alert in st.session_state.get("global_alerts", []):
            st.markdown(f"<div class='admin-broadcast-banner'>📢 ANNOUNCEMENT: {alert}</div>", unsafe_allow_html=True)
            
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-card'><h4>🏫 Institutional Hub</h4><p>{USER_DATA.get('school')}<br>Level: `{USER_DATA.get('class')}`</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><h4>🧬 Curriculum Scope</h4><p>{', '.join(USER_DATA.get('subjects', []))}</p></div>", unsafe_allow_html=True)
        with col3:
            partner_id = USER_DATA.get("partner", "")
            partner_name = st.session_state["users_registry"].get(partner_id, {}).get("name", "No Peer Linked") if partner_id else "No Peer Linked"
            st.markdown(f"<div class='metric-card'><h4>🤝 Collaboration Sync</h4><p>{partner_name}<br>Framework: `{USER_DATA.get('partner_role', 'Standalone')}`</p></div>", unsafe_allow_html=True)

        st.markdown("### 🔔 Active System Notifications Terminal (EAT)")
        user_notifications = st.session_state["last_read_tracker"].get(CURRENT_USER_ID, [])
        if not user_notifications:
            st.info("📩 Workspace activity log clear.")
        else:
            for note in reversed(user_notifications):
                seen_status = "⭐ New" if not note.get("seen") else "✓ Logged"
                st.markdown(f"> **[{note.get('time')}] ({seen_status})** {note.get('msg')}")
            if st.button("🧹 Clear Logs Monitor"):
                for note in st.session_state["last_read_tracker"][CURRENT_USER_ID]:
                    note["seen"] = True
                save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])
                st.rerun()

    # 📊 SYLLABUS SYNC MATRIX TRACKER
    elif selected_workspace == "📊 Personal Progress Tracker":
        st.markdown("<h2>📊 Personal Syllabus Coverage Matrix</h2>", unsafe_allow_html=True)
        if "progress" not in USER_DATA or not USER_DATA["progress"]:
            USER_DATA["progress"] = create_blank_progress_card(USER_DATA.get("subjects", []))
            st.session_state["users_registry"][CURRENT_USER_ID] = USER_DATA
        
        user_progress = USER_DATA["progress"]
        for sub in USER_DATA.get("subjects", []):
            if sub not in NCDC_CURRICULUM_MAP: continue
            with st.expander(f"📚 {sub} Module Milestone Mapping"):
                for topic in NCDC_CURRICULUM_MAP[sub]:
                    if sub not in user_progress: user_progress[sub] = {}
                    if topic not in user_progress[sub]: user_progress[sub][topic] = {"status": "Not Started", "score": 0}
                    
                    t_col1, t_col2, t_col3 = st.columns([2, 1, 1])
                    with t_col1: st.markdown(f"**{topic}**")
                    with t_col2:
                        opts = ["Not Started", "In Progress", "Fully Revised & Mastered"]
                        saved_idx = opts.index(user_progress[sub][topic].get("status", "Not Started")) if user_progress[sub][topic].get("status") in opts else 0
                        new_status = st.selectbox(f"Flag##{sub}##{topic}", opts, index=saved_idx, label_visibility="collapsed")
                    with t_col3:
                        new_score = st.number_input(f"Score##{sub}##{topic}", min_value=0, max_value=100, value=int(user_progress[sub][topic].get("score", 0)), step=5, label_visibility="collapsed")
                    
                    user_progress[sub][topic] = {"status": new_status, "score": new_score}
                
                if st.button(f"💾 Commit {sub} Records", key=f"sv_{sub}"):
                    st.session_state["users_registry"][CURRENT_USER_ID]["progress"] = user_progress
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    st.success("Matrix coverage records successfully locked down.")

    # 📝 REVISION CENTER & ASSESSMENT ENGINE (WITH EXAM FORWARDING LOGIC)
    elif selected_workspace == "📝 Revision Center & Mock Vault":
        st.markdown("<h2>📝 Academic Revision & Evaluation Vault</h2>", unsafe_allow_html=True)
        tab_notes, tab_exam, tab_shared = st.tabs(["📂 Shared Document Center", "⏱️ High-Precision Examination", "📩 Forwarded Peer Exams"])
        
        with tab_notes:
            for doc in st.session_state.get("revision_notes_db", []):
                st.markdown(f"<div class='notes-box'><h4>📌 {doc['Subject']} | {doc['Title']}</h4><p>{doc['Content']}</p></div>", unsafe_allow_html=True)
            with st.form("Reference Note Intake"):
                dt = st.text_input("Descriptive Title")
                ds = st.selectbox("Category Field", USER_DATA.get("subjects", ["Mathematics"]))
                dc = st.text_area("Content or Document Cloud Coordinates Link")
                if st.form_submit_button("PUBLISH TO RESOURCE BANK"):
                    if dt and dc:
                        st.session_state["revision_notes_db"].append({"Title": dt, "Subject": ds, "Content": dc})
                        st.rerun()

        with tab_exam:
            st.markdown("### ⏱️ Live Microsecond Metric Assessment Node")
            fallback_quiz = pd.DataFrame([
                {"Question": "Factorize completely the cubic expression: $x^3 - 6x^2 + 11x - 6 = 0$. Determine correct roots.", "OptionA": "1, 2, 3", "OptionB": "-1, -2, -3", "OptionC": "0, 1, 5", "OptionD": "2, 4, 6", "Answer": "A", "Solution": "By factor theorem, testing x=1 gives 0. Long division results in (x-1)(x-2)(x-3)=0."},
                {"Question": "A particle progresses along a linear vector with displacement $s = t^3 - 3t^2 + 2$. Evaluate acceleration at $t=3$ seconds.", "OptionA": "6 m/s^2", "OptionB": "12 m/s^2", "OptionC": "18 m/s^2", "OptionD": "24 m/s^2", "Answer": "B", "Solution": "v = ds/dt = 3t^2 - 6t. a = dv/dt = 6t - 6. At t=3, a = 6(3) - 6 = 12 m/s^2."}
            ])
            quiz_df = read_public_sheet("QuizBank")
            if quiz_df is None or quiz_df.empty: quiz_df = fallback_quiz
            
            if "exam_running" not in st.session_state: st.session_state["exam_running"] = False
            if "start_epoch" not in st.session_state: st.session_state["start_epoch"] = 0.0

            if not st.session_state["exam_running"]:
                if st.button("🚀 BOOT HIGH-PRECISION REVISION EXAM TERMINAL"):
                    st.session_state["exam_running"] = True
                    st.session_state["start_epoch"] = time.time()
                    st.rerun()
            else:
                elapsed = time.time() - st.session_state["start_epoch"]
                st.markdown(f"<div class='timer-container'><span style='color:#ff3333; font-size:20px; font-weight:bold;'>{elapsed:.4f} Seconds Logged</span></div>", unsafe_allow_html=True)
                
                with st.form("Exam Questionnaire Blueprint"):
                    user_selections = {}
                    for idx, row in quiz_df.iterrows():
                        st.markdown(f"#### Q{idx+1}: {row['Question']}")
                        opts = [f"A) {row['OptionA']}", f"B) {row['OptionB']}", f"C) {row['OptionC']}", f"D) {row['OptionD']}"]
                        user_selections[idx] = st.radio(f"Select Answer Choice for Q{idx+1}:", opts, key=f"qm_{idx}")
                    
                    if st.form_submit_button("🔒 LOCK ANSWERS AND SUBMIT FOR EVALUATION"):
                        total_time = time.time() - st.session_state["start_epoch"]
                        st.session_state["exam_running"] = False
                        
                        correct = 0
                        breakdown = []
                        for idx, row in quiz_df.iterrows():
                            chosen = user_selections[idx].split(")")[0].strip()
                            ans = str(row['Answer']).strip()
                            ok = (chosen == ans)
                            if ok: correct += 1
                            breakdown.append({"Item": f"Q {idx+1}", "Your Pick": chosen, "Correct Key": ans, "Status": "PASS" if ok else "FAIL", "Traceback Explanation": row['Solution']})
                        
                        score = (correct / len(quiz_df)) * 100
                        st.markdown("### 🏆 Performance Analytics Sheet")
                        st.metric("Performance Mark Percentage", f"{score:.2f}%")
                        
                        # Cache performance into state so user can choice to forward it if it's a failed block (< 50%)
                        st.session_state["last_score"] = score
                        st.session_state["last_breakdown"] = breakdown
                        st.rerun()

            if "last_score" in st.session_state:
                st.subheader("Last Exam Attempt Breakdown Summary")
                st.write(f"Final Score: **{st.session_state['last_score']:.2f}%**")
                st.dataframe(pd.DataFrame(st.session_state["last_breakdown"]))
                
                # Forward Failed Exam Routing Option
                if st.session_state["last_score"] < 50.0:
                    st.warning("⚠️ Critical Milestone Deficit detected (Score under 50%). Review with your peer sync.")
                    partner_id = USER_DATA.get("partner", "")
                    if partner_id:
                        if st.button("📤 FORWARD FAILED EXAM MATRIX TO ACADEMIC PARTNER"):
                            if partner_id not in st.session_state["shared_exams"]:
                                st.session_state["shared_exams"][partner_id] = []
                            st.session_state["shared_exams"][partner_id].append({
                                "from_name": USER_DATA.get("name"),
                                "score": st.session_state["last_score"],
                                "timestamp": get_east_timestamp(),
                                "data": st.session_state["last_breakdown"]
                            })
                            save_cache_to_disk("db_shared_exams.json", st.session_state["shared_exams"])
                            push_system_notification(partner_id, f"🚨 Peer Sync Warning: {USER_DATA.get('name')} forwarded a failed evaluation sheet for alignment check!")
                            st.success("Evaluation performance matrix cleanly routed to peer channel coordinates.")
                    else:
                        st.info("💡 Link an academic partner in the connection hub to sync failed records directly.")

        with tab_shared:
            st.subheader("Incoming Peer Error Analysis Records")
            my_shared = st.session_state["shared_exams"].get(CURRENT_USER_ID, [])
            if not my_shared:
                st.info("Inbox clear. No failed alignment metrics routed from your sync partner.")
            else:
                for idx, report in enumerate(my_shared):
                    with st.expander(f"⚠️ Report from {report['from_name']} ({report['timestamp']}) ── Score: {report['score']:.1f}%"):
                        st.dataframe(pd.DataFrame(report["data"]))

    # 💬 REALTIME WHATSAPP LOUNGE CHAT
    elif selected_workspace == "💬 WhatsApp Lounge Chat":
        st.markdown("<h2>💬 WhatsApp Lounge Communication Space</h2>", unsafe_allow_html=True)
        mode = st.radio("Channel Matrix Frequencies:", ["🌍 Global Network Mainframe", "🔒 Private Peer-to-Peer Link"], horizontal=True)
        
        def render_bubble(m, name):
            is_me = (m.get("sender") == name)
            cls = "chat-right" if is_me else "chat-left"
            tk = " <span class='whatsapp-ticks'>✓✓</span>" if is_me else ""
            aud = f"<div class='audio-note-box'>🎵 <b>Voice Note Simulation</b> ({m['audio_duration']}) ──🔊</div>" if m.get("audio_duration") else ""
            med = f"<div class='chat-media-box'>📁 Attached File Coordinates:<br><a href='{m['media_link']}' target='_blank' style='color:#53bdeb;'>{m['media_link']}</a></div>" if m.get("media_link") else ""
            st.markdown(f"<div class='chat-bubble {cls}'><span style='font-size:11px; font-weight:bold; color:#ff3333; display:block;'>{m.get('sender')}</span>{m.get('text')}{med}{aud}<span class='chat-timestamp'>{m.get('timestamp')}{tk}</span></div>", unsafe_allow_html=True)

        if mode == "🌍 Global Network Mainframe":
            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            for msg in st.session_state.get("general_chat", []):
                render_bubble(msg, USER_DATA.get("name"))
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("Global Tx", clear_on_submit=True):
                txt = st.text_input("Type Message...")
                c1, c2 = st.columns(2)
                l1 = c1.text_input("Attach File Link URL (Optional)")
                l2 = c2.text_input("Simulate Voice Note Duration (Optional)")
                if st.form_submit_button("TRANSMIT MSG"):
                    if txt or l1 or l2:
                        st.session_state["general_chat"].append({"sender": USER_DATA.get("name"), "text": txt, "timestamp": get_east_timestamp(), "media_link": l1, "audio_duration": l2})
                        save_cache_to_disk("db_genchat.json", st.session_state["general_chat"])
                        st.rerun()
                        
        elif mode == "🔒 Private Peer-to-Peer Link":
            pid = USER_DATA.get("partner", "")
            if not pid: st.warning("⚠️ No synchronized partner linked to your profile node.")
            else:
                p_prof = st.session_state["users_registry"].get(pid, {})
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
                for msg in st.session_state.get("private_chats", []):
                    if msg.get("sender") in [USER_DATA.get("name"), p_prof.get("name")]:
                        render_bubble(msg, USER_DATA.get("name"))
                st.markdown("</div>", unsafe_allow_html=True)
                
                with st.form("P2P Tx", clear_on_submit=True):
                    ptxt = p_text_input("Type Encrypted Message...")
                    if st.form_submit_button("TRANSMIT SECURE DATA"):
                        if ptxt:
                            st.session_state["private_chats"].append({"sender": USER_DATA.get("name"), "text": ptxt, "timestamp": get_east_timestamp()})
                            save_cache_to_disk("db_p2pchat.json", st.session_state["private_chats"])
                            push_system_notification(pid, f"📥 Encrypted message received from your partner {USER_DATA.get('name')}.")
                            st.rerun()

    # 📚 SUBJECT GROUP DISCUSSIONS (WITH LIVE HANDS AND VOICE NOTES)
    elif selected_workspace == "📚 Subject Group Discussions":
        st.markdown("<h2>📚 Subject Group Discussion Hub (EAT)</h2>", unsafe_allow_html=True)
        
        user_subs = USER_DATA.get("subjects", ["Mathematics"])
        selected_group = st.selectbox("Select Active Subject Channel Frequency:", user_subs)
        
        # Google Meet Panel: Raised Hands Indicator list
        active_hands = []
        for uid, is_raised in st.session_state["raised_hands"].items():
            if is_raised:
                peer_name = st.session_state["users_registry"].get(uid, {}).get("name", "Unknown Node")
                active_hands.append(f"✋ {peer_name}")
                
        if active_hands:
            st.markdown("### 🔊 Classroom Intercom: Raised Hands Status")
            st.warning(", ".join(active_hands) + " are requesting open floor execution speaker status.")
            
        st.write("---")
        st.info(f"🛰️ Connected to the **{selected_group}** Dedicated Revision Stream.")
        
        if selected_group not in st.session_state["subject_chats"]:
            st.session_state["subject_chats"][selected_group] = []
            
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for msg in st.session_state["subject_chats"][selected_group]:
            is_me = (msg.get("sender") == USER_DATA.get("name"))
            cls = "chat-right" if is_me else "chat-left"
            tk = " <span class='whatsapp-ticks'>✓✓</span>" if is_me else ""
            aud = f"<div class='audio-note-box'>🎵 <b>Voice Note Simulation</b> ({msg['audio_duration']}) ──🔊</div>" if msg.get("audio_duration") else ""
            med = f"<div class='chat-media-box'>📁 Attached File Coordinates:<br><a href='{msg['media_link']}' target='_blank' style='color:#53bdeb;'>{msg['media_link']}</a></div>" if msg.get("media_link") else ""
            st.markdown(f"<div class='chat-bubble {cls}'><span style='font-size:11px; font-weight:bold; color:#53bdeb; display:block;'>{msg.get('sender')} ({msg.get('school')})</span>{msg.get('text')}{med}{aud}<span class='chat-timestamp'>{msg.get('timestamp')}{tk}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        with st.form("SubTx", clear_on_submit=True):
            sub_txt = st.text_input(f"Broadcast text to {selected_group} Room...")
            c1, c2 = st.columns(2)
            s_l1 = c1.text_input("Attach Reference URL Link (Optional)")
            s_l2 = c2.text_input("Simulate Voice Note Duration (Optional)")
            
            if st.form_submit_button("TRANSMIT TO FIELD"):
                if sub_txt or s_l1 or s_l2:
                    st.session_state["subject_chats"][selected_group].append({
                        "sender": USER_DATA.get("name"),
                        "school": USER_DATA.get("school", "The Amazima School"),
                        "text": sub_txt,
                        "timestamp": get_east_timestamp(),
                        "media_link": s_l1,
                        "audio_duration": s_l2
                    })
                    save_cache_to_disk("db_subchat.json", st.session_state["subject_chats"])
                    st.rerun()

    # 🤝 COLLABORATIVE PAIRING FRAMEWORK MODULE
    elif selected_workspace == "🤝 Partner Connection Hub":
        st.markdown("<h2>🤝 Academic Collaboration & Partner Pairing Hub</h2>", unsafe_allow_html=True)
        pid = USER_DATA.get("partner", "")
        if pid:
            p_node = st.session_state["users_registry"].get(pid, {})
            st.success(f"🔗 Sync Channel Active! Linked Candidate: {p_node.get('name')} | Mode: {USER_DATA.get('partner_role')}")
            if st.button("💔 SEVER CHANNEL CONNECTION"):
                st.session_state["users_registry"][CURRENT_USER_ID]["partner"] = ""
                if pid in st.session_state["users_registry"]: st.session_state["users_registry"][pid]["partner"] = ""
                save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                st.rerun()
        else:
            candidates = {uid: node.get("name") for uid, node in st.session_state["users_registry"].items() if uid != CURRENT_USER_ID and not node.get("partner")}
            if not candidates: st.warning("No unlinked candidates currently broadcasting live on the tracking network.")
            else:
                tgt = st.selectbox("Select Candidate Target Node:", list(candidates.keys()), format_func=lambda x: candidates[x])
                role_md = st.selectbox("Assign Collaboration Matrix Model:", ["Mutual Study Partners", "Mentor-Mentee Framework", "Assessor-Candidate Pairing"])
                if st.button("🔗 LOCK SECURE SYNC HANDSHAKE"):
                    st.session_state["users_registry"][CURRENT_USER_ID]["partner"] = tgt
                    st.session_state["users_registry"][CURRENT_USER_ID]["partner_role"] = role_md
                    st.session_state["users_registry"][tgt]["partner"] = CURRENT_USER_ID
                    st.session_state["users_registry"][tgt]["partner_role"] = role_md
                    save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                    push_system_notification(tgt, f"✨ Handshake active! Paired with {USER_DATA.get('name')} as {role_md}.")
                    st.rerun()

    # ⚙️ SUPER ADMIN EXCLUSIVE PRIVILEGE WORKSPACES
    elif selected_workspace == "⚙️ Super Admin Operations" and USER_DATA.get("role") in ["ADMIN", "SUPER_ADMIN"]:
        st.markdown("<h2>⚙️ Command Center Operations</h2>", unsafe_allow_html=True)
        tab_users, tab_broad, tab_eng = st.tabs(["🔒 Identity Registry Matrix", "📢 Public Broadcast Operations", "🛠 Core Configs"])
        
        with tab_users:
            for uid, node in list(st.session_state["users_registry"].items()):
                st.markdown(f"<div class='directory-card'><b>ID:</b> <code>{uid}</code> | <b>Name:</b> {node.get('name')} | <b>Role:</b> <code>{node.get('role')}</code> | <b>Status:</b> <code>{node.get('status')}</code><br><b>Warning Text:</b> <span style='color:#ff9999;'>{node.get('warning_msg','None')}</span></div>", unsafe_allow_html=True)
                c_a1, c_a2, c_a3, c_a4 = st.columns(4)
                with c_a1:
                    if st.button("🟢 APPROVE", key=f"ap_{uid}"):
                        st.session_state["users_registry"][uid]["status"] = "Approved"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        push_system_notification(uid, "🟢 Profile status set to Approved by Admin.")
                        st.rerun()
                with c_a2:
                    if st.button("🟡 SUSPEND", key=f"sp_{uid}"):
                        st.session_state["users_registry"][uid]["status"] = "Suspended"
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        st.rerun()
                with c_a3:
                    w_txt = st.text_input("Enter Citation Text", key=f"tx_{uid}")
                    if st.button("⚠️ WARNING CITATION", key=f"wn_{uid}"):
                        st.session_state["users_registry"][uid]["warning_msg"] = w_txt
                        save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                        push_system_notification(uid, f"⚠️ Official Warning: {w_txt}")
                        st.rerun()
                with c_a4:
                    if st.button("🔴 PURGE UNIT", key=f"dl_{uid}"):
                        if uid not in ["0000", "6601"]:
                            del st.session_state["users_registry"][uid]
                            save_cache_to_disk("db_users.json", st.session_state["users_registry"])
                            st.rerun()

        with tab_broad:
            new_al = st.text_input("Draft Network Announcement Payload")
            if st.button("🚀 TRANSMIT DISPATCH"):
                if new_al:
                    st.session_state["global_alerts"].insert(0, new_al)
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.rerun()
            for idx, item in enumerate(st.session_state.get("global_alerts", [])):
                st.markdown(f"- {item}")
                if st.button(f"🗑️ Terminate Broadcast {idx}", key=f"t_al_{idx}"):
                    st.session_state["global_alerts"].pop(idx)
                    save_cache_to_disk("db_alerts.json", st.session_state["global_alerts"])
                    st.rerun()

        with tab_eng:
            admin_photo_url = st.text_input("Modify Admin Avatar Core URL Link Coordinate Asset:", value=st.session_state.get("custom_admin_photo", DEFAULT_SUDAISI_IMAGE))
            if st.button("💾 SAVE ADMIN AVATAR LOGS"):
                st.session_state["custom_admin_photo"] = admin_photo_url
                save_cache_to_disk("db_admin_photo.json", admin_photo_url)
                st.success("Admin photo asset configurations updated successfully.")
                st.rerun()
            st.write("---")
            st.write("Active Verification Access Keys Matrix:")
            st.write(st.session_state.get("generated_registration_codes", []))
            n_cd = st.text_input("Generate New Access Token")
            if st.button("➕ LOG REGISTRATION KEY"):
                if n_cd and n_cd not in st.session_state["generated_registration_codes"]:
                    st.session_state["generated_registration_codes"].append(n_cd)
                    save_cache_to_disk("db_regcodes.json", st.session_state["generated_registration_codes"])
                    st.rerun()

    # Dynamic Platform Branding System Footer Component
    st.markdown("""
    <div class='sudaisi-branding-footer'>
        <p style='color: #444; font-size: 11px; margin: 0;'>🛡️ Academic Shield Network Infrastructure Engine v4.26 • Core Engineering Configured by Sudaisi Setra</p>
    </div>
    """, unsafe_allow_html=True)
