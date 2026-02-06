import os

# Clé secrète pour les tokens JWT
SECRET_KEY = "une_cle_tres_longue_et_securisee_12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- CONFIGURATION IA (OPENROUTER) ---

# REMPLACE CECI PAR TA VRAIE CLÉ OPENROUTER
LLM_API_KEY = "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" 

LLM_API_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"

# --- BASE DE DONNÉES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"






