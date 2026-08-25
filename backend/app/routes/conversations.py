from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..routes.auth import get_current_user

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.get("", response_model=List[schemas.ConversationResponse])
def get_conversations(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Conversation).filter(models.Conversation.user_id == current_user.id).order_by(models.Conversation.created_at.desc()).all()

@router.post("", response_model=schemas.ConversationResponse)
def create_conversation(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = models.Conversation(user_id=current_user.id, title="New Session")
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

@router.get("/{conv_id}", response_model=schemas.ConversationDetailResponse)
def get_conversation(conv_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = db.query(models.Conversation).filter(models.Conversation.id == conv_id, models.Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv
