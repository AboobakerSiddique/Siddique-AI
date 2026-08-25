import os

MEMORY_FILE = "user_memory.txt"

def save_core_memory(fact: str) -> str:
    """Saves an important fact about the user to long-term memory. 
    Use this when the user asks you to remember something, or shares a persistent preference, name, or detail.
    
    Args:
        fact: A concise, standalone statement of the fact to remember.
    """
    try:
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"- {fact}\n")
        return f"Successfully saved to core memory: {fact}"
    except Exception as e:
        return f"Failed to save memory: {str(e)}"
