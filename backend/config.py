import os
from dotenv import load_dotenv

# charger les variables d'environnement depuis .env
load_dotenv()

# clé secrète pour les tokens jwt
SECRET_KEY = os.getenv("SECRET_KEY", "azertyuiopqsdfghjklmwxcvbn1234567890")
# algorithme pour signer les tokens
ALGORITHM = "HS256"
# durée de validité du token en minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# dossier de la base de données
DATABASE_DIR = os.getenv("DATABASE_DIR", "./")

# clé API pour OpenRouter
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
# URL de l'API OpenRouter
LLM_API_URL = os.getenv("LLM_API_URL", "https://openrouter.ai/api/v1")
# modèle LLM à utiliser
LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/llama-3-8b-instruct")

# On récupère le chemin du dossier où se trouve le fichier config.py lui-même
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
