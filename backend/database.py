from tinydb import TinyDB, Query
from config import DATABASE_PATH
from datetime import datetime
import os

# chemins des deux fichiers json separes
users_db_path = os.path.join(os.path.dirname(DATABASE_PATH) or "./", "users.json")
conversations_db_path = os.path.join(os.path.dirname(DATABASE_PATH) or "./", "conversations.json")

# creer les deux bases de donnees
users_db = TinyDB(users_db_path)
conversations_db = TinyDB(conversations_db_path)

# utiliser les tables par defaut de tinydb
users_table = users_db.table('_default')
conversations_table = conversations_db.table('_default')

# trouver un utilisateur par email
def get_user_by_email(email: str):
    User = Query()
    return users_table.get(User.email == email)

# trouver un utilisateur par id
def get_user_by_id(user_id: int):
    User = Query()
    return users_table.get(User.id == user_id)

# creer un nouvel utilisateur
def create_user(email: str, password_hash: str):
    user_id = len(users_table) + 1
    user = {
        "id": user_id,
        "email": email,
        "password_hash": password_hash,
        "created_at": datetime.now().isoformat()
    }
    users_table.insert(user)
    return user

# recuperer ou creer une conversation pour un utilisateur
def get_or_create_conversation(user_id: int):
    Conversation = Query()
    conv = conversations_table.get(Conversation.user_id == user_id)
    
    if not conv:
        conv_id = len(conversations_table) + 1
        conv = {
            "id": conv_id,
            "user_id": user_id,
            "messages": [],
            "created_at": datetime.now().isoformat()
        }
        conversations_table.insert(conv)
    
    return conv

# ajouter un message a la conversation d'un utilisateur
def add_message_to_conversation(user_id: int, role: str, content: str):
    Conversation = Query()
    conv = conversations_table.get(Conversation.user_id == user_id)
    
    if conv:
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        conv["messages"].append(message)
        conversations_table.update({"messages": conv["messages"]}, Conversation.user_id == user_id)
        return conv
    
    return None
