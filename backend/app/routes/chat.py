from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..routes.auth import get_current_user
from ..models import User
from ..llm.client import generate_response, stream_response

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str = None
    message_id: str = None

SIDDQUE_SYSTEM_INSTRUCTION = '''
You are Siddque AI. 
The owner/user is Siddique.
Communication style: Direct, situational, action-oriented. Low tolerance for repetition and unnecessary explanations.
Humor: Sarcasm, puns, playful bullying when obvious mistakes are made.
Problem Solving: Challenge bad ideas, suggest better alternatives, prioritize performance and visual quality.
If I reply "ha", interpret it as "okay / understood / acknowledged".
'''

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    response_text = generate_response(
        prompt=request.message,
        system_instruction=SIDDQUE_SYSTEM_INSTRUCTION
    )
    
    if response_text.startswith("AI_SERVICE_ERROR") or response_text.startswith("ERROR"):
        raise HTTPException(status_code=503, detail=response_text)
        
    return ChatResponse(response=response_text)

@router.post("/stream")
def chat_stream(request: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    return StreamingResponse(
        stream_response(
            prompt=request.message,
            system_instruction=SIDDQUE_SYSTEM_INSTRUCTION
        ),
        media_type="text/event-stream"
    )
