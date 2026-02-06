from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import requests
from contextlib import asynccontextmanager

# Imports de tes fichiers locaux
from config import LLM_API_KEY, LLM_API_URL, LLM_MODEL
from database import (
    get_session, create_db_and_tables, Session, 
    get_user_by_id, get_user_conversation, 
    get_message_by_conversation, add_message
)
from auth import register_user, login_user, verify_token

# --- INITIALISATION ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crée les tables SQLite au démarrage
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
security = HTTPBearer()

# --- CONFIGURATION CORS (Pour React) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SCHÉMAS DE DONNÉES (PYDANTIC) ---

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

class MessageSchema(BaseModel): # Renommé pour éviter conflit avec database.py
    role: str
    content: str

class AIRequest(BaseModel):
    message: str
    conversation_id: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Nouveau schéma pour la création
class ConvCreate(BaseModel):
    titre: str

# --- DÉPENDANCE D'AUTHENTIFICATION ---

def get_current_user(res: HTTPAuthorizationCredentials = Depends(security)):
    token = res.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session invalide ou expirée"
        )
    return user_id

# --- ROUTES D'AUTHENTIFICATION ---

@app.post("/register", response_model=TokenResponse)
def register(user: UserRegister, session: Session = Depends(get_session)):
    result = register_user(user.email, user.password, session)
    if not result:
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà")
    return result

@app.post("/login", response_model=TokenResponse)
def login(user: UserLogin, session: Session = Depends(get_session)):
    result = login_user(user.email, user.password, session)
    if not result:
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")
    return result

@app.get("/me", response_model=UserResponse)
def get_me(user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    user = get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

# --- ROUTES CHAT / CONVERSATIONS ---

@app.post("/conversations")
def create_new_conv(data: ConvCreate, user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    from database import create_conversation # Assure-toi que c'est importé
    return create_conversation(user_id, data.titre, session)

@app.get("/conversations")
def get_conversations(user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_user_conversation(user_id, session)

@app.get("/conversations/{conversation_id}")
def get_messages(
    conversation_id: int, 
    user_id: int = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    messages = get_message_by_conversation(conversation_id, session)
    return messages

@app.post("/chat")
def chat(request: AIRequest, user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    # 1. Sauvegarder le message de l'utilisateur
    add_message(request.conversation_id, "user", request.message, session)
    
    # 2. Récupérer l'historique pour l'IA
    historique_brut = get_message_by_conversation(request.conversation_id, session)
    messages_pour_ia = [{"role": m.role, "content": m.content} for m in historique_brut]

    # 3. Appel à OpenRouter
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": LLM_MODEL,
        "messages": messages_pour_ia
    }
    
    try:
        response = requests.post(f"{LLM_API_URL}/chat/completions", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        ai_response = response.json()["choices"][0]["message"]["content"]
        
        # 4. Sauvegarder la réponse de l'IA
        add_message(request.conversation_id, "assistant", ai_response, session)
        
        return {"message": ai_response, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur IA: {str(e)}")

@app.get("/health")
def health():
    return {"status": "ok"}