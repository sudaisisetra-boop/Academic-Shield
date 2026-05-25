# =========================================================================
# REVISED MASTER DATABASE ENGINE LAYER (database.py)
# =========================================================================
import json
import os

def load_storage_node(filename, default_factory):
    """Loads a state tracking array file safely from local persistent cluster storage."""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except Exception:
            return default_factory
    return default_factory

def save_storage_node(filename, data_packet):
    """Writes runtime payload properties down to persistent cluster state memory storage."""
    try:
        with open(filename, "w") as f:
            json.dump(data_packet, f, indent=4)
    except Exception:
        pass

def save_node(filename, data_packet):
    """Fallback link alias keeping system call structures identical across files."""
    save_storage_node(filename, data_packet)

# Initialize standard operational environment arrays
REGISTRATION_CODES = load_storage_node("registration_codes.json", ["AMAZIMA-S5-2026"])
GLOBAL_BROADCASTS = load_storage_node("global_broadcasts.json", ["S5 Candidates: Ensure all Pure Math worksheet scans are clear before submission."])
SUGGESTIONS_BOX = load_storage_node("suggestions_box.json", [])
DISCUSSION_MESSAGES = load_storage_node("discussion_messages.json", [])
GENERAL_CHAT_LEDGER = load_storage_node("lounge_chat.json", [])
P2P_CHAT_LEDGER = load_storage_node("private_chat.json", [])
REVISION_NOTES_VAULT = load_storage_node("revision_notes_vault.json", [])

# Core Registry Base Node Map - Explicit User Custom Request Configuration
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

USERS_REGISTRY = load_storage_node("users_registry.json", DEFAULT_REGISTRY)

# Enforce clean sync override to protect against corrupted or cached JSON states
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

save_storage_node("users_registry.json", USERS_REGISTRY)

def fetch_question_from_sheet(subject_domain):
    """Simulates random pulling mechanics matching custom NCDC syllabus parameters."""
    mock_questions = {
        "Mathematics": [
            {"Question": "Solve the cubic equation 2x^3 - 3x^2 - 11x + 6 = 0 completely.", "Solution": "Factorizing gives (x-3)(2x-1)(x+2) = 0. Roots: x = 3, x = 0.5, x = -2."},
            {"Question": "Given vectors OA = 2i + 3j and OB = 5i - 2j, find the vector tracking coordinates for OT.", "Solution": "Vector computation verifies tracking alignment parameters cleanly."}
        ],
        "Physics": [
            {"Question": "A projectile is fired at an angle of 45 degrees. Calculate its maximum horizontal displacement.", "Solution": "R = (u^2 * sin(2*theta)) / g. Max range occurs at 45 degrees where sin(90)=1."},
        ],
        "Chemistry": [
            {"Question": "Calculate the total number of moles present in 25 grams of pure Calcium Carbonate (CaCO3).", "Solution": "Molar mass = 100g/mol. Moles = 25 / 100 = 0.25 moles calculated accurately."}
        ],
        "Biology": [
            {"Question": "Explain the behavioral structure of cell membranes and lipids under fluid mosaic parameters.", "Solution": "Fluid mosaic framework demonstrates structural phospholipid mobility."}
        ]
    }
    import random
    pool = mock_questions.get(subject_domain, [{"Question": "General Question Template", "Solution": "Standard Solution Matrix"}])
    return random.choice(pool)
