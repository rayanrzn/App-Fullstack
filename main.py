from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import UserRegister, UserLogin, TokenResponse, AIRequest, ConversationResponse
from auth import register_user, login_user, verify_token
from database import get_or_create_conversation, add_message_to_conversation, get_user_by_id
import requests
from config import LLM_API_KEY, LLM_API_URL, LLM_MODEL

app = FastAPI()
security = HTTPBearer()

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

# routes publiques

# inscrire un nouvel utilisateur
@app.post("/register", response_model=TokenResponse)
def register(user: UserRegister):
    result = register_user(user.email, user.password)
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
def get_me(user_id: int = Depends(get_current_user)):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# recuperer la conversation de l'utilisateur
@app.get("/conversations", response_model=ConversationResponse)
def get_user_conversations(user_id: int = Depends(get_current_user)):
    conv = get_or_create_conversation(user_id)
    return conv

# envoyer un message a l'ia
@app.post("/chat")
def chat(request: AIRequest, user_id: int = Depends(get_current_user)):
    if not LLM_API_KEY:
        raise HTTPException(status_code=500, detail="LLM API key not configured")
    
    # sauvegarder le message de l'utilisateur
    add_message_to_conversation(user_id, "user", request.message)
    
    # appeler l'api ia
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Assistant",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": request.message}
        ]
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
        
        # sauvegarder la reponse de l'ia
        add_message_to_conversation(user_id, "assistant", ai_response)
        
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
