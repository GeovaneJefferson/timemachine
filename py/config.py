import os
from server import SERVER

server = SERVER()
EXPANDUSER = os.path.expanduser("~")

# Debounce
DEBOUNCE_COOLDOWN = 1.0
_LAST_EVENT_TIME = {}

# Exclusions - Enhanced patterns
DIR_PATTERNS = [
    ".git", 
    "node_modules", 
    ".temp", 
    "temp",
    "tmp",
    "__pycache__",
    ".idea",
    ".vscode",
    ".vs",
    "venv",
    "env",
    "virtualenv",
    ".venv",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".coverage",
    ".tox",
    "*.egg-info",
    "__pycache__*",
    "*__pycache__"
]

FILE_PATTERNS = [
    "*.tmp",
    "*.temp",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.so",
    "*.cache",
    "*.log",
    "*.bak",
    "*.swp",
    "*.swo",
    "*~",
    "*.class",
    "Thumbs.db",
    ".DS_Store",
    "desktop.ini"
]

# Performance / tuning
POLLING_INTERVAL = 1800
HIGH_CPU_THRESHOLD = 75.0
LARGE_FILE_THRESHOLD = 50 * 1024 * 1024

MIN_BATCH_SIZE = 10
BASE_BATCH_SIZE = 50
MAX_BATCH_SIZE = 200

MIN_REPROCESS_INTERVAL = 60
FLATPAK_BACKUP_INTERVAL = POLLING_INTERVAL


def truncate_path(path: str, max_len: int = 35) -> str:
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3):]