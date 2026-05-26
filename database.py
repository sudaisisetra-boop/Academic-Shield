# =========================================================================
# FINAL COMPREHENSIVE ENGINE LAYER: DATABASE MANAGER (database.py)
# =========================================================================
import json
import os
import random
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials
import gspread

DB_FILE = "users_registry.json"

def load_storage_node(filename, default_factory):
    """Loads state arrays safely from persistent local storage."""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except Exception:
            return default_factory
    return default_factory

def save_storage_node(filename, data_packet):
    """Writes runtime payload changes instantly down to permanent disk memory."""
    try:
        with open(filename, "w") as f:
            json.dump(data_packet, f, indent=4)
    except Exception:
        pass

def save_node(filename, data_packet):
    """Fallback link alias keeping system call signatures aligned."""
    save_storage_node(filename, data_packet)

# -------------------------------------------------------------------------
# PERMANENT ACCOUNT DATA REGISTRY INFRASTRUCTURE
# -------------------------------------------------------------------------
DEFAULT_REGISTRY = {
    "admin_node": {
        "username": "Admin",
        "pwd": "AdminSudaisi222",
        "name": "Setra Stones (Admin)",
        "role": "SUPER_ADMIN",
        "status": "Approved",
        "warning_msg": ""
    },
    "setra_student_node": {
        "username": "Setrastones",
        "pwd": "Sheillahstones222",
        "name": "Setra Stones",
        "class": "Senior Five",
        "school": "The Amazima School",
        "phone": "+256752047103",
        "email": "sudaisisetra@gmail.com",
        "location": "Jinja",
        "subjects": ["Mathematics", "Physics", "Chemistry"],
        "status": "Approved",
        "role": "USER",
        "warning_msg": "",
        "grade_logs": []
    }
}

# Persistent variables loaded from disk storage permanently
USERS_REGISTRY = load_storage_node(DB_FILE, DEFAULT_REGISTRY)
REGISTRATION_CODES = load_storage_node("registration_codes.json", ["AMAZIMA-S5-2026"])
GLOBAL_BROADCASTS = load_storage_node("global_broadcasts.json", ["S5 Candidates: Ensure all Pure Math worksheet scans are clear before submission."])
SUGGESTIONS_BOX = load_storage_node("suggestions_box.json", [])

# Permanent Chatrooms (Messages are appended and written directly to local disk storage)
DISCUSSION_MESSAGES = load_storage_node("discussion_messages.json", [])
GENERAL_CHAT_LEDGER = load_storage_node("lounge_chat.json", [])
P2P_CHAT_LEDGER = load_storage_node("private_chat.json", [])
REVISION_NOTES_VAULT = load_storage_node("revision_notes_vault.json", [])

# Enforce clean credential synchronization to wipe out old cached values
if "admin_node" in USERS_REGISTRY:
    USERS_REGISTRY["admin_node"]["username"] = "Admin"
    USERS_REGISTRY["admin_node"]["pwd"] = "AdminSudaisi222"
else:
    USERS_REGISTRY["admin_node"] = DEFAULT_REGISTRY["admin_node"]

if "setra_student_node" in USERS_REGISTRY:
    USERS_REGISTRY["setra_student_node"]["username"] = "Setrastones"
    USERS_REGISTRY["setra_student_node"]["pwd"] = "Sheillahstones222"
else:
    USERS_REGISTRY["setra_student_node"] = DEFAULT_REGISTRY["setra_student_node"]

save_storage_node(DB_FILE, USERS_REGISTRY)

# -------------------------------------------------------------------------
# SECURE LIVE GOOGLE SHEETS API REVISION DATA PIPELINE
# -------------------------------------------------------------------------
def fetch_questions_from_google_sheet(subject_domain):
    """
    Connects to the Google Sheet securely in microseconds using cloud secrets.
    Pulls the spreadsheet tab matching the subject name, reads Column A (question) 
    and Column B (metadata), and returns 2 random questions.
    """
    try:
        # Load the configuration from Streamlit Cloud dashboard secure secrets portal
        secrets_dict = dict(st.secrets["gcs_connections"])
        sheet_id = secrets_dict.get("google_sheet_id")
        
        # Authenticate Google Service Bot Email Accounts
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(secrets_dict, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Open Workbook and access the targeted subject worksheet tab
        spreadsheet = client.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(subject_domain)
        
        # Extract all cells cleanly into a list of row dictionaries
        records = worksheet.get_all_records()
        
        if len(records) >= 2:
            sampled_rows = random.sample(records, 2)
            formatted_questions = []
            for row in sampled_rows:
                # Target exact user column formats: "question" and "metadata"
                q_text = row.get("question", row.get("Question", "Scenario question entry field empty."))
                m_text = row.get("metadata", row.get("Metadata", "Official NCDC standard solution matrix field empty."))
                formatted_questions.append({"Question": str(q_text), "Solution": str(m_text)})
            return formatted_questions
    except Exception as e:
        # Graceful fallback architecture if Google Cloud is offline or secrets are missing during setup
        pass

    # High-fidelity system local safety backup data framework
    mock_pool = {
        "Mathematics": [
            {"Question": "Solve the cubic equation 2x^3 - 3x^2 - 11x + 6 = 0 completely.", "Solution": "SOLUTION: Factorizing gives (x-3)(2x-1)(x+2) = 0. Roots: x = 3, x = 0.5, x = -2. TOPIC: Polynomials"},
            {"Question": "Given vectors OA = 2i + 3j and OB = 5i - 2j, calculate the tracking coordinate position properties for vector OT.", "Solution": "SOLUTION: Vector scalar addition rules confirm matching components perfectly. TOPIC: Vectors"}
        ],
        "Physics": [
            {"Question": "A projectile is fired at an angle of 45 degrees. Calculate its maximum horizontal displacement parameters.", "Solution": "SOLUTION: Range formula R = (u^2 * sin(2*theta)) / g handles trajectory calculations flawlessly. TOPIC: Mechanics"},
            {"Question": "Explain the decay structural layout parameters of a radioactive isotope element like Technetium-99.", "Solution": "SOLUTION: Inherent exponential radioactive decay calculation curves dictate particle drop. TOPIC: Radioactivity"}
        ],
        "Chemistry": [
            {"Question": "Calculate the total number of moles present in 25 grams of pure Calcium Carbonate (CaCO3).", "Solution": "SOLUTION: Molar mass equals 100g/mol. Total Moles = 25 / 100 = 0.25 moles calculated cleanly. TOPIC: Stoichiometry"},
            {"Question": "Explain standard dynamic volumetric elements of acid-base buffer solutions.", "Solution": "SOLUTION: Weak conjugate pairs handle proton transitions cleanly. TOPIC: Volumetric Analysis"}
        ],
        "Biology": [
            {"Question": "Explain the fluid mosaic framework structure of living cells and lipid membranes.", "Solution": "SOLUTION: Lipid bilayer fluid structures maximize cellular protection metrics. TOPIC: Cell Membranes"},
            {"Question": "Track the respiratory enzyme chain breakdown matrices within animal cell structures.", "Solution": "SOLUTION: Mitochondria layers optimize energy storage extraction loops. TOPIC: Respiration"}
        ]
    }
    pool = mock_pool.get(subject_domain, [{"Question": "Syllabus Scenario Assignment", "Solution": "Official NCDC Solution Standard"}])
    if len(pool) >= 2:
        return random.sample(pool, 2)
    return [pool[0], pool[0]]
