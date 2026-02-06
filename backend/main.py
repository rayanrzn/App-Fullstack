from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from auth import register_user, login_user, verify_token
import requests
from config import LLM_API_KEY, LLM_API_URL, LLM_MODEL
from Databases import *

app = FastAPI()
security = HTTPBearer()

# formulaire d'inscription
class UserRegister(BaseModel):
    email: str
    password: str

# formulaire de connexion
class UserLogin(BaseModel):
    email: str
    password: str

# reponse utilisateur (sans le mot de passe)
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: str

# un message dans une conversation
class Message(BaseModel):
    role: str  # "user" ou "assistant"
    content: str
    timestamp: str

# une conversation complete avec tous ses messages
class ConversationResponse(BaseModel):
    id: int
    user_id: int
    messages: List[Message]
    created_at: str

# requete vers l'ia
class AIRequest(BaseModel):
    message: str
    conversation_id : int

# reponse avec token jwt
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# permettre les requetes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# verifier le jwt token pour les routes protegees
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# inscrire un nouvel utilisateur
@app.post("/register", response_model=TokenResponse)
def register(user: UserRegister, session: Session = Depends(get_session)):
    result = register_user(user.email, user.password, session)
    if result is None:
        raise HTTPException(status_code=400, detail="Email already exists")
    return TokenResponse(access_token=result["token"], token_type="bearer")

# connecter un utilisateur
@app.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    result = login_user(user.email, user.password)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=result["token"], token_type="bearer")

# routes protegees (besoin du token jwt)

# recuperer les infos de l'utilisateur connecte
@app.get("/me")
def get_me(user_id: int = Depends(verify_token), session: Session = Depends(get_session)):
    user = get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# recuperer la conversation de l'utilisateur
@app.get("/conversations", response_model=ConversationResponse,)
def get_user_conversations(user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    conv = get_user_conversation(user_id, session)
    return conv

# envoyer un message à l'IA et sauvegarder la réponse
@app.post("/chat")
def chat(request: AIRequest, user_id: int = Depends(verify_token), session: Session = Depends(get_session)):
    if not LLM_API_KEY:
        raise HTTPException(status_code=500, detail="LLM API key not configured")
    
    conv = get_conversation_by_id(request.conversation_id, session)
    if not conv:
        raise HTTPException(status_code=404, detail="La conversation n'éxiste pas !")
    if conv.user_id != user_id:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé a rentrer !")
    
    
    # sauvegarder le message de l'utilisateur
    add_message(
        conversation_id=request.conversation_id,
        role="user",
        content=request.message,
        session=session
    )
    
    # appeler l'api ia
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Assistant",
        "Content-Type": "application/json"
    }
    
    historique_brut = get_message_by_conversation(request.conversation_id, session)
    message_pour_ia = []
    for m in historique_brut:
        message_pour_ia.append({"role": m.role, "content": m.content})

    payload = {
        "model": LLM_MODEL,
        "messages": message_pour_ia
    }
    
    try:
        response = requests.post(
            f"{LLM_API_URL}/chat/completions", 
            json=payload, 
            headers=headers, 
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        ai_response = data["choices"][0]["message"]["content"]
        ai_content = "Réponse de l'IA..."
        
        # sauvegarder la reponse de l'ia
        add_message(
            conversation_id=request.conversation_id,
            role="assistant",
            content=ai_response,
            session=session
        )
        
        return {"message": ai_response, "status": "success"}
    
    except Exception as e:
        print(f"Error details: {str(e)}")
        return {"message": str(e), "status": "error"}

# verifier que le serveur fonctionne
@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
