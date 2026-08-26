from .file_reader import read_local_file
from .dir_scanner import list_directory
from .web_fetcher import fetch_url
from .iot_bridge import local_iot_request
from .rag_search import ingest_to_knowledge_base, search_knowledge_base
from .memory import save_core_memory

REGISTERED_TOOLS = [read_local_file, list_directory, fetch_url, save_core_memory, local_iot_request, ingest_to_knowledge_base, search_knowledge_base]
