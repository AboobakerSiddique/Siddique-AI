from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    class Config: from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    class Config: from_attributes = True

class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageResponse] = []
