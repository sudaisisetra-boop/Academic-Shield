# =========================================================================
# PART 1 OF 2: REVISED PERSISTENT MOCK DATABASE LAYER (database.py)
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
GLOBAL_BROADCASTS = load_storage_node("global_broadcasts.json", ["S5 Candidates: Ensure all Pure Math and Biology worksheet scans are clear before submission."])
SUGGESTIONS_BOX = load_storage_node("suggestions_box.json", [])
DISCUSSION_MESSAGES = load_storage_node("discussion_messages.json", [])
GENERAL_CHAT_LEDGER = load_storage_node("lounge_chat.json", [])
P2P_CHAT_LEDGER = load_storage_node("private_chat.json", [])
REVISION_NOTES_VAULT = load_storage_node("revision_notes_vault.json", [])

# Core Registry Base Node Map
DEFAULT_REGISTRY = {
    "admin_node": {
        "username": "admin_setra",
        "pwd": "AdminPassword2026",
        "name": "Setra Stones (Admin)",
        "role": "SUPER_ADMIN",
        "status": "Approved",
        "warning_msg": ""
    },
    "setra_student_node": {
        "username": "Setra stones",
        "pwd": "Amazima2026",
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

# Ensure the core default user identities are actively written back into memory arrays
if "admin_node" not in USERS_REGISTRY:
    USERS_REGISTRY["admin_node"] = DEFAULT_REGISTRY["admin_node"]
if "setra_student_node" not in USERS_REGISTRY:
    USERS_REGISTRY["setra_student_node"] = DEFAULT_REGISTRY["setra_student_node"]

save_storage_node("users_registry.json", USERS_REGISTRY)

def fetch_question_from_sheet(subject_domain):
    """
    Simulates random pulling mechanics matching custom layout rows.
    Returns clean mock content strings matching NCDC curriculum tracking standards.
    """
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
            {"Question": "Explain the behavioral structure of cell membranes and lipids under fluid mosaic parameters.", "Solution": "Applying structural alignment guidelines resolves the derivative limits factor smoothly."}
        ]
    }
    import random
    pool = mock_questions.get(subject_domain, [{"Question": "General Question Template", "Solution": "Standard Solution Matrix"}])
    return random.choice(pool)
