from datetime import datetime, timedelta
from jose import JWTError, jwt
from bcrypt import hashpw, checkpw, gensalt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_user_by_email, create_user, Session

# --- SÉCURITÉ MOT DE PASSE ---

def hash_password(password: str) -> str:
    """Hache un mot de passe avec bcrypt."""
    return hashpw(password.encode(), gensalt()).decode()

def verify_password(password: str, hash: str) -> bool:
    """Vérifie un mot de passe par rapport à son hash."""
    return checkpw(password.encode(), hash.encode())

# --- GESTION DES TOKENS JWT ---

def create_access_token(user_id: int) -> str:
    """Crée un token JWT incluant l'ID utilisateur et une expiration."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """Décode et vérifie la validité d'un token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None

# --- LOGIQUE MÉTIER (AUTH) ---

def register_user(email: str, password: str, session: Session):
    """Inscrit un nouvel utilisateur et retourne un token."""
    # Vérification de l'existence
    if get_user_by_email(email, session):
        return None
    
    # Création de l'utilisateur
    password_hash = hash_password(password)
    user = create_user(email, password_hash, session)
    
    # Génération du token (accès via .id car c'est un objet SQLModel)
    token = create_access_token(user.id)
    
    # Retourne les clés attendues par TokenResponse dans main.py
    return {
        "access_token": token, 
        "token_type": "bearer"
    }

def login_user(email: str, password: str, session: Session):
    """Connecte un utilisateur existant et retourne un token."""
    user = get_user_by_email(email, session)
    
    if not user or not verify_password(password, user.password_hash):
        return None
    
    token = create_access_token(user.id)
    
    return {
        "access_token": token, 
        "token_type": "bearer"
    }