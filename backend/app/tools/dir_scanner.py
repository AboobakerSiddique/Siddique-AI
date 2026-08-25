import os

def list_directory(directory_path: str = ".") -> str:
    """Lists all files and folders in the specified local directory to understand project structure.
    Args:
        directory_path: The path to the folder. Defaults to current directory.
    """
    if not os.path.exists(directory_path):
        return f"Error: Directory '{directory_path}' does not exist."
    try:
        items = os.listdir(directory_path)
        return "\n".join(items) if items else "Directory is empty."
    except Exception as e:
        return f"Error listing directory: {str(e)}"
