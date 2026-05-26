# =========================================================================
# SECURE DATA ENGINE LAYER (database.py)
# =========================================================================
import json
import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

def load_node(filename, default_value):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except:
            return default_value
    return default_value

def save_node(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def save_storage_node(filename, data):
    save_node(filename, data)

# --- NCDC OFFICIAL STIPULATED TOPICS TRACKER ---
NCDC_SYLLABUS = {
    "Mathematics": [
        "Pure Math: Quadratic Equations & Polynomials",
        "Pure Math: Logarithmic & Exponential Equations",
        "Pure Math: Trigonometric Identities & Equations",
        "Pure Math: Matrices & Determinants",
        "Pure Math: Vectors & Coordinate Geometry",
        "Pure Math: Calculus (Differentiation & Integration)",
        "Applied Math: Projectile Motion & Mechanics",
        "Applied Math: Probability & Statistics"
    ],
    "Physics": [
        "Mechanics: Linear Motion & Projectiles",
        "Modern Physics: Radioactivity & Nuclear Decay",
        "Waves & Optics: Light Refraction & Wave Properties",
        "Electricity & Magnetism: Fields and Capacitors",
        "Heat & Thermodynamics"
    ],
    "Chemistry": [
        "Physical Chemistry: Stoichiometry & Mole Concept",
        "Inorganic Chemistry: Periodicity & Transition Elements",
        "Organic Chemistry: Hydrocarbons & Functional Groups",
        "Chemical Kinetics & Equilibrium"
    ],
    "Biology": [
        "Cell Biology & Biochemistry",
        "Plant Anatomy & Physiology",
        "Human Anatomy: Circulatory & Reproductive Systems",
        "Genetics & Evolution",
        "Ecology & Environmental Biology"
    ]
}

# --- LOCAL EMERGENCY FALLBACK EXAM BANK ---
STATIC_EXAM_BANK = {
    "Mathematics": {
        "Pure Math: Quadratic Equations & Polynomials": [
            {"Question": "Given that the roots of $3x^2 - 5x + 2 = 0$ are $\\alpha$ and $\\beta$, find the quadratic equation whose roots are $\\alpha^2$ and $\\beta^2$.", "Solution": "alpha+beta=5/3, alpha*beta=2/3. New sum=13/9, product=4/9. Equation: 9x^2 - 13x + 4 = 0."},
            {"Question": "Express $f(x) = 4x^3 - 3x^2 + 2x - 1$ in terms of factors when divided by $(x-1)$. Find the remainder.", "Solution": "By remainder theorem, evaluate f(1) = 4 - 3 + 2 - 1 = 2. Remainder is 2."}
        ]
    },
    "Physics": {
        "Modern Physics: Radioactivity & Nuclear Decay": [
            {"Question": "A sample of Technetium-99 decays to 12.5% of its original activity in 18 hours. Calculate its half-life.", "Solution": "12.5% remaining implies 3 half-lives have elapsed. 18 / 3 = 6 hours."},
            {"Question": "A nucleus of Bismuth-210 undergoes beta minus decay. Write the balanced nuclear equation.", "Solution": "Bismuth-210 (Z=83) transitions to Polonium-210 (Z=84) with electron and antineutrino emission."}
        ]
    }
}

# --- CORE USER REGISTRY NODES ---
DEFAULT_USERS = {
    "node_7701": {
        "username": "Setrastones", "pwd": "Sheillahstones222", "name": "Sudaisi Setra", "class": "Senior Five",
        "school": "The Amazima School", "phone": "+256752047103", "email": "sudaisisetra@gmail.com", "location": "Jinja",
        "subjects": ["Mathematics", "Physics"], "status": "Approved", "role": "USER", "warning_msg": "", "grade_logs": []
    },
    "admin_setra": {
        "username": "admin_setra", "pwd": "AdminPassword2026", "name": "Sudaisi Setra (Admin)", "class": "Staff",
        "school": "The Amazima School", "phone": "+256752047103", "email": "admin@shield.ug", "location": "Jinja",
        "subjects": ["All"], "status": "Approved", "role": "SUPER_ADMIN", "warning_msg": "", "grade_logs": []
    }
}

USERS_REGISTRY = load_node("users_registry.json", DEFAULT_USERS)

# Enforce schema consistency to guarantee no KeyErrors happen in the directory layout
for uid, profile in USERS_REGISTRY.items():
    profile.setdefault("school", "The Amazima School")
    profile.setdefault("location", "Jinja")
    profile.setdefault("phone", "+256752047103")
    profile.setdefault("email", "sudaisisetra@gmail.com")
    profile.setdefault("class", "Senior Five")
    profile.setdefault("grade_logs", [])
    profile.setdefault("status", "Approved")

REGISTRATION_CODES = load_node("registration_codes.json", ["AMAZIMA-S5-2026", "SHIELD-JOIN"])
SUGGESTIONS_BOX = load_node("suggestions_box.json", [])
REVISION_NOTES_VAULT = load_node("revision_notes_vault.json", [
    {"Title": "Pure Mathematics P425/1 Notes", "Subject": "Mathematics", "Content": "S5 Polynomial and quadratic systems structural review worksheet."}
])

DISCUSSION_MESSAGES = load_node("discussion_messages.json", [])
GENERAL_CHAT_LEDGER = load_node("lounge_chat.json", [])
P2P_CHAT_LEDGER = load_node("private_chat.json", [])
MUTUAL_EXAMS_DB = load_node("mutual_exams_db.json", {})

# --- LIVE GOOGLE SHEETS SYNCHRONIZATION ENGINE ---
def fetch_questions_from_google_sheet(subject, topic):
    """
    Safely connects to your Google Sheet connection using Streamlit Cloud Secrets.
    Falls back gracefully to the offline NCDC question arrays if secrets are unconfigured.
    """
    try:
        if "gcs_connections" in st.secrets:
            secret_dict = dict(st.secrets["gcs_connections"])
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_info(secret_dict, scopes=scopes)
            client = gspread.authorize(creds)
            
            # Access workbook assuming title matches subject track domain names
            sheet = client.open(f"Academic_Shield_{subject}").sheet1
            records = sheet.get_all_records()
            
            # Filter rows by selected topic parameter column
            filtered = [r for r in records if str(r.get("Topic", "")).strip().lower() == topic.strip().lower()]
            if len(filtered) >= 2:
                import random
                chosen = random.sample(filtered, 2)
                return [{"Question": c["Question"], "Solution": c["Solution"]} for c in chosen]
            elif filtered:
                return [{"Question": c["Question"], "Solution": c["Solution"]} for c in filtered]
    except Exception as e:
        pass # Fall back directly to hardcoded infrastructure arrays below

    # Backup local lookup mapping system
    sub_dict = STATIC_EXAM_BANK.get(subject, {})
    if topic in sub_dict:
        return sub_dict[topic]
        
    # Generalized disaster recovery matrix packet
    return [
        {"Question": f"Evaluate foundational parameters regarding NCDC Syllabus for {subject}: Topic ({topic}). Question Item #1.", "Solution": "Refer to official standard student manuals."},
        {"Question": f"Analyze structured calculation equations mapping out computational attributes for {topic}. Question Item #2.", "Solution": "Verify final equations against school text proofs."}
]
