import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..routes.auth import get_current_user
from ..llm.client import generate_response, stream_response

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: int = None

SIDDQUE_SYSTEM_INSTRUCTION = '''
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

@router.post("/stream")
def chat_stream(request: ChatRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    conv = get_or_create_conversation(db, current_user.id, request.conversation_id)
    
    # Save user message
    user_msg = models.Message(conversation_id=conv.id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    # Generate title if it's the first message
    if conv.title == "New Session":
        conv.title = request.message[:30] + ("..." if len(request.message) > 30 else "")
        db.commit()

    # Generator wrapper to intercept and save the full AI response
    def stream_and_save():
        full_response = ""
        # Tell the frontend the conversation ID immediately
        yield f"data: {json.dumps({'conversation_id': conv.id})}\n\n"
        
        for chunk in stream_response(prompt=request.message, system_instruction=SIDDQUE_SYSTEM_INSTRUCTION):
            yield chunk
            # Extract text to save to DB
            if chunk.startswith("data: ") and "[DONE]" not in chunk:
                try:
                    data = json.loads(chunk[6:])
                    if "text" in data:
                        full_response += data["text"]
                except: pass
                
        # Save assistant message once stream finishes
        ai_msg = models.Message(conversation_id=conv.id, role="assistant", content=full_response)
        db.add(ai_msg)
        db.commit()

    return StreamingResponse(stream_and_save(), media_type="text/event-stream")
