from datetime import datetime, timedelta
from jose import JWTError, jwt
from bcrypt import hashpw, checkpw, gensalt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from Databases import get_user_by_email, create_user

# hasher un mot de passe avec bcrypt
def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()

# verifier un mot de passe contre son hash
def verify_password(password: str, hash: str) -> bool:
    return checkpw(password.encode(), hash.encode())

# creer un jwt token avec user_id et expiration
def create_access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token 

# verifier et decoder un jwt token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None

# enregistrer un nouvel utilisateur
def register_user(email: str, password: str, session):
    # verifier si l'utilisateur existe
    if get_user_by_email(email):
        return None
    
    # hasher et creer
    password_hash = hash_password(password)
    user = create_user(email, password_hash, session)
    
    # creer le token
    token = create_access_token(user["id"])
    
    return {"token": token}

# connecter un utilisateur
def login_user(email: str, password: str, session):
    user = get_user_by_email(email,session)
    
    # verifier email et password
    if not user or not verify_password(password, user["password_hash"]):
        return None
    
    # creer le token
    token = create_access_token(user["id"])
    
    return {"token": token}
