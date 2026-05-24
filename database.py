import streamlit as st
import pandas as pd
import datetime
import json
import os

# Complete curriculum alignment structures mapping
NCDC_CURRICULUM_MAP = {
    "Mathematics": ["Numerical Concepts", "Equations and Inequalities", "Coordinate Geometry 1", "Partial Fractions", "Trigonometry", "Descriptive Statistics", "Vectors", "Differentiation 1", "Integration 1", "Complex Numbers", "Differential Equations"],
    "Physics": ["Measurement and Dimensions", "Statics", "Linear Motion", "Fluid Mechanics", "Mechanical Properties of Matter", "Thermometry", "Heat Quantities", "Electrostatics", "Capacitors"],
    "Chemistry": ["Moles and Equations", "Atomic and Electronic Structure", "Bonding and Structure", "Periodicity I", "Thermochemistry", "Organic Chemistry I", "Equilibria I", "Electrochemistry"],
    "Biology": ["Cell Biology", "Nutrition", "Transport", "Respiration", "Homeostasis", "Coordination", "Ecology"]
}

DEFAULT_SUDAISI_IMAGE = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=200"
AVATAR_OPTIONS = [
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    "https://cdn-icons-png.flaticon.com/512/4140/4140037.png",
    "https://cdn-icons-png.flaticon.com/512/4140/4140048.png"
]

SHEET_ID = st.secrets.get("SHEET_ID", "1xU80PotVALVM3sWt7PS3kLGbsivqzMvznXq0c8Cu44M")

def get_east_timestamp():
    """Generates precise East Africa Time (EAT / UTC+3) timestamps."""
    utc_now = datetime.datetime.utcnow()
    east_now = utc_now + datetime.timedelta(hours=3)
    return east_now.strftime("%I:%M %p")

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
    except Exception: 
        pass

def load_cache_from_disk(filename, default_val):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f: 
                return json.load(f)
        except Exception: 
            pass
    return default_val

def push_system_notification(user_id, alert_text):
    if "last_read_tracker" not in st.session_state:
        st.session_state["last_read_tracker"] = {}
    if user_id not in st.session_state["last_read_tracker"]:
        st.session_state["last_read_tracker"][user_id] = []
    st.session_state["last_read_tracker"][user_id].append({
        "msg": alert_text, "time": get_east_timestamp(), "seen": False
    })
    save_cache_to_disk("db_readtrack.json", st.session_state["last_read_tracker"])

def create_blank_progress_card(subjects_list):
    card = {}
    for sub in subjects_list:
        if sub in NCDC_CURRICULUM_MAP:
            card[sub] = {topic: {"status": "Not Started", "score": 0} for topic in NCDC_CURRICULUM_MAP[sub]}
    return card

def initialize_global_states():
    # Primary profiles system configuration
    if "users_registry" not in st.session_state:
        st.session_state["users_registry"] = {
            "0000": {"username": "Admin", "pwd": "SudaisiAdmin2026", "name": "Sudaisi Setra", "class": "Senior Five", "school": "The Amazima School", "phone": "0752047103", "email": "admin@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry", "Biology"], "status": "Approved", "warning_msg": "", "avatar": "SUDAISI_BAKED", "partner": "", "partner_role": "Standalone", "role": "SUPER_ADMIN"},
            "6601": {"username": "Setra stones", "pwd": "Amazima2026", "name": "Setra Stones", "class": "Senior Five", "school": "The Amazima School", "phone": "0752047103", "email": "setra@shield.com", "gender": "Male", "location": "Kampala", "subjects": ["Mathematics", "Physics", "Chemistry"], "status": "Approved", "warning_msg": "", "avatar": AVATAR_OPTIONS[0], "partner": "", "partner_role": "Standalone", "role": "USER"}
        }
        disk_users = load_cache_from_disk("db_users.json", {})
        if disk_users: st.session_state["users_registry"].update(disk_users)

    # Communications channels memory allocations
    if "general_chat" not in st.session_state: 
        st.session_state["general_chat"] = load_cache_from_disk("db_genchat.json", [])
    if "private_chats" not in st.session_state: 
        st.session_state["private_chats"] = load_cache_from_disk("db_p2pchat.json", [])
    if "subject_chats" not in st.session_state:
        st.session_state["subject_chats"] = load_cache_from_disk("db_subchat.json", {})
        
    # Virtual Intercom Classroom & Evaluation parameters allocations
    if "raised_hands" not in st.session_state:
        st.session_state["raised_hands"] = load_cache_from_disk("db_hands.json", {})
    if "shared_exams" not in st.session_state:
        st.session_state["shared_exams"] = load_cache_from_disk("db_shared_exams.json", {})
        
    # Administrative control platform constants
    if "global_alerts" not in st.session_state: 
        st.session_state["global_alerts"] = load_cache_from_disk("db_alerts.json", ["🚀 Platform Online. Secure Mirror Systems Functional."])
    if "last_read_tracker" not in st.session_state: 
        st.session_state["last_read_tracker"] = load_cache_from_disk("db_readtrack.json", {})
    if "generated_registration_codes" not in st.session_state: 
        st.session_state["generated_registration_codes"] = load_cache_from_disk("db_regcodes.json", ["SHIELD2026", "ASP2026"])
    if "custom_admin_photo" not in st.session_state: 
        st.session_state["custom_admin_photo"] = load_cache_from_disk("db_admin_photo.json", DEFAULT_SUDAISI_IMAGE)
    if "revision_notes_db" not in st.session_state:
        st.session_state["revision_notes_db"] = [
            {"Title": "Pure Mathematics Vectors Blueprint", "Subject": "Mathematics", "Content": "Vectors core revision summary notes summary for P425/1 standards."}
]
