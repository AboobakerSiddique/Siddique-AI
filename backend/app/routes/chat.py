import json
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..routes.auth import get_current_user
from ..llm.client import stream_response

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: int = None

BASE_SYSTEM_INSTRUCTION = '''
You are Siddique AI. 
The owner/user is Siddique.
Communication style: Direct, situational, action-oriented. Low tolerance for repetition and unnecessary explanations.
Humor: Sarcasm, puns, playful bullying when obvious mistakes are made.
Problem Solving: Challenge bad ideas, suggest better alternatives, prioritize performance and visual quality.
If I reply "ha", interpret it as "okay / understood / acknowledged".
'''

def get_or_create_conversation(db: Session, user_id: int, conv_id: int = None) -> models.Conversation:
    if conv_id:
        conv = db.query(models.Conversation).filter(models.Conversation.id == conv_id, models.Conversation.user_id == user_id).first()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conv
    
    conv = models.Conversation(user_id=user_id, title="New Session")
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_dynamic_instruction():
    instruction = BASE_SYSTEM_INSTRUCTION
    if os.path.exists("user_memory.txt"):
        with open("user_memory.txt", "r", encoding="utf-8") as f:
            memories = f.read().strip()
            if memories:
                instruction += f"\n\nCORE MEMORIES (Always refer to these if relevant):\n{memories}"
    return instruction

@router.post("/stream")
def chat_stream(request: ChatRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    conv = get_or_create_conversation(db, current_user.id, request.conversation_id)
    
    db_messages = db.query(models.Message).filter(models.Message.conversation_id == conv.id).order_by(models.Message.created_at.asc()).all()
    recent_messages = db_messages[-10:]
    history_payload = [{"role": m.role, "content": m.content} for m in recent_messages]

    user_msg = models.Message(conversation_id=conv.id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    if conv.title == "New Session":
        conv.title = request.message[:30] + ("..." if len(request.message) > 30 else "")
        db.commit()

    def stream_and_save():
        full_response = ""
        yield f"data: {json.dumps({'conversation_id': conv.id})}\n\n"
        
        dynamic_instruction = get_dynamic_instruction()
        
        for chunk in stream_response(
            prompt=request.message, 
            system_instruction=dynamic_instruction,
            history=history_payload
        ):
            yield chunk
            if chunk.startswith("data: ") and "[DONE]" not in chunk:
                try:
                    data = json.loads(chunk[6:])
                    if "text" in data:
                        full_response += data["text"]
                except: pass
                
        ai_msg = models.Message(conversation_id=conv.id, role="assistant", content=full_response)
        db.add(ai_msg)
        db.commit()

    return StreamingResponse(stream_and_save(), media_type="text/event-stream")
