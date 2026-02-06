from sqlmodel import SQLModel, create_engine, Field, Session, select
from typing import Optional
from datetime import datetime
from fastapi import FastAPI
from config import DATABASE_URL

sqlite_url = DATABASE_URL
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Table USER
class User (SQLModel) :
    id : Optional[int] = Field(default=None, primary_key=True)
    email : str
    password_hash : str

# Table Conversation
class Conversation (SQLModel) :
    user_id : int = Field(foreign_key="user.id")
    id : Optional[int] = Field(default=None, primary_key=True)
    titre : str

# Table Message
class Message (SQLModel) :
    conversation_id : int = Field(foreign_key="conversation.id")
    id : Optional[int] = Field(default=None, primary_key=True)
    role : str
    content : str
    date : datetime = Field(default_factory=datetime.utcnow)

engine = create_engine(sqlite_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
    
def get_user_by_email(email: str, session: Session):
    statement = select(User).where(User.email == email)
    result = session.exec(statement).first()
    return result

def get_user_by_id(user_id: int, session: Session):
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()

def create_user(email: str, password_hash : str, session: Session):
    new_user = User(email=email, password_hash=password_hash)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def create_conversation(user_id:int, titre:str, session:Session):
    new_conversation = Conversation(user_id=user_id, titre=titre)
    session.add(new_conversation)
    session.commit()
    session.refresh(new_conversation)
    return new_conversation

def get_user_conversation(user_id: int, session:Session):
    statement = select(Conversation).where(Conversation.user_id == user_id)
    results = session.exec(statement).all()
    return results

def add_message(conversation_id:int, role:str, content:str, session:Session):
    new_message = Message(conversation_id=conversation_id, role=role, content=content)
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    return new_message

def get_message_by_conversation(conversation_id:str, session:Session):
    statement = select(Message).where(Message.conversation_id == conversation_id)
    results = session.exec(statement).all()
    return results

def get_conversation_by_id(id:int, session:Session):
    statement = select(Conversation).where(Conversation.id == id)
    results = session.exec(statement).first()
    return results