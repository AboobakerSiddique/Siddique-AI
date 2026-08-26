import json
from google import genai
from google.genai import types
from ..config import settings
from ..tools.registry import REGISTERED_TOOLS

try:
    client = genai.Client(api_key=settings.gemini_api_key)
except Exception:
    client = None

MODEL_ID = "gemini-3.6-flash"

def stream_response(prompt: str, system_instruction: str = None, history: list = None, image_bytes: bytes = None, image_mime_type: str = None):
    if not client:
        yield f"data: {json.dumps({'error': 'Gemini API Key is missing or invalid'})}\n\n"
        return
        
    config = types.GenerateContentConfig(tools=REGISTERED_TOOLS)
    if system_instruction:
        config.system_instruction = system_instruction
        
    safe_history = []
    if history:
        last_role = None
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            if not msg["content"].strip() or role == last_role:
                continue
            safe_history.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )
            last_role = role
            
        if safe_history and safe_history[-1].role == "user":
            safe_history.append(types.Content(role="model", parts=[types.Part.from_text(text="Acknowledged.")]))

    try:
        chat = client.chats.create(model=MODEL_ID, config=config, history=safe_history)
        
        # Build the multimodal payload
        message_parts = []
        if image_bytes and image_mime_type:
            message_parts.append(types.Part.from_bytes(data=image_bytes, mime_type=image_mime_type))
        message_parts.append(types.Part.from_text(text=prompt))
        
        response_stream = chat.send_message_stream(message_parts)
        
        for chunk in response_stream:
            if chunk.text:
                yield f"data: {json.dumps({'text': chunk.text})}\n\n"
        
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': f'AI_SERVICE_ERROR: {str(e)}'})}\n\n"
