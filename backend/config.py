import os
from dotenv import load_dotenv

# charger les variables d'environnement depuis .env
load_dotenv()

# clé secrète pour les tokens jwt
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
# algorithme pour signer les tokens
ALGORITHM = "HS256"
# durée de validité du token en minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# chemin du fichier de base de données
DATABASE_PATH = os.getenv("DATABASE_PATH", "./db.json")

# configuration de l'api ia
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_URL = os.getenv("LLM_API_URL", "https://openrouter.ai/api/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/llama-2-7b-chat")
