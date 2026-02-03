from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

# reponse avec token jwt
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
