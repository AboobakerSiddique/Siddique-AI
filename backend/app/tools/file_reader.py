import os

def read_local_file(file_path: str) -> str:
    """Reads the contents of a local file. Use this to inspect code, logs, or configurations.
    Args:
        file_path: The absolute or relative path to the file.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    if not os.path.isfile(file_path):
        return f"Error: '{file_path}' is not a file."
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Cap at ~15,000 characters to prevent blowing up the token context
            return content[:15000] + ("\n...[TRUNCATED]" if len(content) > 15000 else "")
    except Exception as e:
        return f"Error reading file: {str(e)}"
