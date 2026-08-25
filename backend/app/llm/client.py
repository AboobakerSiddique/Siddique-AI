import json
from google import genai
from google.genai import types
from ..config import settings

try:
    client = genai.Client(api_key=settings.gemini_api_key)
except Exception:
    client = None

MODEL_ID = "gemini-3.6-flash"

def generate_response(prompt: str, system_instruction: str = None) -> str:
    if not client:
        return "ERROR: Gemini API Key is missing or invalid."
    
    config = types.GenerateContentConfig()
    if system_instruction:
        config.system_instruction = system_instruction
        
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=config
        )
        return response.text
    except Exception as e:
        return f"AI_SERVICE_ERROR: {str(e)}"

def stream_response(prompt: str, system_instruction: str = None):
    if not client:
        yield f"data: {json.dumps({'error': 'Gemini API Key is missing or invalid'})}\n\n"
        return
        
    config = types.GenerateContentConfig()
    if system_instruction:
        config.system_instruction = system_instruction
        
    try:
        response_stream = client.models.generate_content_stream(
            model=MODEL_ID,
            contents=prompt,
            config=config
        )
        for chunk in response_stream:
            if chunk.text:
                # Yield JSON strings so newlines in code blocks don't break the SSE format
                yield f"data: {json.dumps({'text': chunk.text})}\n\n"
        
        # Tell the frontend the stream is finished
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': f'AI_SERVICE_ERROR: {str(e)}'})}\n\n"
