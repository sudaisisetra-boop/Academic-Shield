# =========================================================================
# FILE 1 OF 3: STABLE PERMANENT STORAGE ENGINE (database.py)
# =========================================================================
import json
import os
import time

# Create a secure localized directory cluster for data survival
DB_DIR = "shield_network_db"
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def load_storage_node(filename, default_structure):
    """Safely reads persistent data pools from the disk partition."""
    file_path = os.path.join(DB_DIR, filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as storage_file:
                return json.load(storage_file)
        except (json.JSONDecodeError, IOError):
            return default_structure
    return default_structure

def save_storage_node(filename, data_payload):
    """Writes system mutations permanently to prevent cache drop data leaks."""
    file_path = os.path.join(DB_DIR, filename)
    try:
        with open(file_path, "w", encoding="utf-8") as storage_file:
            json.dump(data_payload, storage_file, indent=4, ensure_ascii=False)
        return True
    except IOError:
        return False

# =========================================================================
# COMPREHENSIVE NCDC ADVANCED CURRICULUM VECTOR MAP (BIOLOGY INCLUDED)
# =========================================================================
NCDC_CURRICULUM_MAP = {
    "Mathematics": [
        "Pure Mathematics: Quadratics & Cubics", 
        "Vectors, Lines & Collinearity Matrix", 
        "Trigonometric Identities & Equations", 
        "Calculus: Differentiation Mechanics", 
        "Calculus: Integration Parameters"
    ],
    "Physics": [
        "Mechanics: Projectile Motion Linear Vectors", 
        "Modern Physics: Quantum & Atomic Structures", 
        "Waves, Optic Mechanics & Geometrical Refraction", 
        "Electricity, Magnetism & Alternating Currents"
    ],
    "Chemistry": [
        "Physical Chemistry: The Mole Concept & Gas Laws", 
        "Organic Chemistry: Alkanes, Alkenes & Alcohols", 
        "Inorganic Chemistry: Transition Elements & Periodicity"
    ],
    "Biology": [
        "Cell Biology: Ultra-structure & Cell Physiology",
        "Biochemistry: Enzymes, Lipids & Carbohydrates",
        "Anatomy & Physiology: Homeostasis & Osmo-regulation",
        "Syllabus Ecology: Population Dynamics & Ecosystems",
        "Genetics & Evolution: Monohybrid & Dihybrid Inheritance"
    ]
}

# =========================================================================
# SYSTEM CORE MASTER REPOSITORIES INITIALIZATION (CAPABLE OF 200+ USERS)
# =========================================================================

# Master User Record Coordinates Cache
DEFAULT_USERS = {
    "6601": {
        "username": "Setra stones", 
        "pwd": "Amazima2026", 
        "name": "Sudaisi Setra", 
        "class": "Senior Five", 
        "school": "The Amazima School", 
        "phone": "+256700000000", 
        "email": "setra@amazima.org", 
        "location": "Kampala", 
        "subjects": ["Mathematics", "Physics", "Biology"], 
        "status": "Approved", 
        "role": "SUPER_ADMIN", 
        "warning_msg": "", 
        "partner": "6602", 
        "partner_role": "Sync Partner"
    },
    "6602": {
        "username": "Gideon Cheps", 
        "pwd": "Gideon2026", 
        "name": "Gideon Cheps", 
        "class": "Senior Five", 
        "school": "The Amazima School", 
        "phone": "+256711111111", 
        "email": "gideon@amazima.org", 
        "location": "Jinja", 
        "subjects": ["Mathematics", "Chemistry", "Biology"], 
        "status": "Approved", 
        "role": "USER", 
        "warning_msg": "", 
        "partner": "6601", 
        "partner_role": "Sync Partner"
    }
}

# Synchronize instance states down to persistence layers
USERS_REGISTRY = load_storage_node("users_registry.json", DEFAULT_USERS)
REGISTRATION_CODES = load_storage_node("registration_codes.json", ["AMAZIMA-S5-2026", "SHIELD-TOKEN-2026"])
GLOBAL_BROADCASTS = load_storage_node("global_broadcasts.json", ["Welcome to the Academic Shield Network portal interface system."])
REVISION_NOTES_VAULT = load_storage_node("revision_notes_vault.json", [])
SUGGESTIONS_BOX = load_storage_node("suggestions_box.json", [])
LOUNGE_CHAT_HISTORY = load_storage_node("lounge_chat.json", [])
PRIVATE_CHAT_HISTORY = load_storage_node("private_chat.json", [])

def get_ugandan_timestamp():
    """Generates standard time reference strings for chat logging."""
    return time.strftime("%H:%M", time.localtime())
