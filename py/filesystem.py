import os
import time
import uuid
import shutil
import hashlib
import logging
import stat
import fnmatch
from typing import Optional
from collections import OrderedDict
from config import (
    LARGE_FILE_THRESHOLD, DEBOUNCE_COOLDOWN, _LAST_EVENT_TIME, 
    DIR_PATTERNS, FILE_PATTERNS, server, EXPANDUSER
)

# Cache to prevent excessive database calls for settings
_DB_CACHE = {
    'exclude_hidden': False,
    'last_check': 0
}

# LRU debounce tracking to prevent memory leaks (max 50K entries)
_DEBOUNCE_LRU_MAX = 50000
_DEBOUNCE_CLEANUP_INTERVAL = 60  # Seconds between cleanup passes
_LAST_CLEANUP = time.time()

def _get_cached_setting():
    """
    Retrieves the 'exclude_hidden_itens' setting from the database.
    Updates the cache every 30 seconds to minimize overhead.
    """
    now = time.time()
    if now - _DB_CACHE['last_check'] > 30:
        val = server.get_database_value('EXCLUDE', 'exclude_hidden_itens')
        _DB_CACHE['exclude_hidden'] = str(val).lower() == 'true' if val else False
        _DB_CACHE['last_check'] = now
    return _DB_CACHE['exclude_hidden']

def calculate_sha256(file_path: str, chunk_size=65536, file_size=None, retries=3) -> Optional[str]:
    """Calculates a SHA256 hash, using a quick method for large files."""
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None

    if file_size is None:
        try:
            file_size = os.stat(file_path).st_size
        except OSError:
            pass

    if file_size == 0:
        return hashlib.sha256(b"").hexdigest()

    # Quick hash logic for large files
    if file_size and file_size > LARGE_FILE_THRESHOLD:
        try:
            st = os.stat(file_path)
            # Use size and mtime as a base fingerprint
            h = hashlib.sha256(f"{file_size}-{st.st_mtime}".encode())
            with open(file_path, "rb") as f:
                # Sample the start, middle, and end of the file
                h.update(f.read(chunk_size))
                f.seek(file_size // 2)
                h.update(f.read(chunk_size))
                f.seek(-chunk_size, 2)
                h.update(f.read(chunk_size))
            return "quick_" + h.hexdigest()
        except Exception:
            return None

    # Standard full hash for smaller files
    for attempt in range(retries):
        try:
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    h.update(chunk)
            return h.hexdigest()
        except OSError:
            time.sleep(0.5)

    return None

def atomic_copy(src: str, dst: str) -> bool:
    """Copies a file using a temporary file to ensure operation integrity."""
    tmp = f"{dst}.tmp_{uuid.uuid4().hex}"
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(src, "rb") as fr, open(tmp, "wb") as fw:
            shutil.copyfileobj(fr, fw)
        shutil.copystat(src, tmp, follow_symlinks=False)
        os.rename(tmp, dst)
        return True
    except Exception as e:
        logging.error(f"Atomic copy failed: {e}")
        if os.path.exists(tmp):
            os.remove(tmp)
        return False

def handle_special_file(src: str, dst: str) -> bool:
    """Handles non-regular files like symlinks or FIFOs."""
    try:
        mode = os.lstat(src).st_mode
        if stat.S_ISLNK(mode):
            os.symlink(os.readlink(src), dst)
            return True
        if stat.S_ISFIFO(mode):
            os.mkfifo(dst)
            return True
        return False
    except Exception:
        return False

def normalize_rel_path(path: str) -> str:
    """Normalizes paths relative to the user's home directory."""
    path = os.path.normpath(path)
    if not os.path.isabs(path):
        path = os.path.join(os.path.expanduser("~"), path)
    rel = os.path.relpath(path, os.path.expanduser("~"))
    return rel.replace(os.sep, "/")

def should_process(path: str) -> bool:
    """Determines if a file should be backed up based on exclusions and debouncing."""
    if not os.path.exists(path):
        return False

    def _should_exclude(path: str) -> bool:
        """Internal helper to check patterns and hidden status."""
        all_patterns = DIR_PATTERNS + FILE_PATTERNS
        
        # Performance Fix: Use cached value instead of direct DB call
        _exclude_hidden = _get_cached_setting()
        
        basename = os.path.basename(path)
        is_directory = os.path.isdir(path) if os.path.exists(path) else False
        
        # Check against defined exclusion patterns
        for pattern in all_patterns:
            if fnmatch.fnmatch(basename, pattern):
                if pattern in DIR_PATTERNS and not is_directory:
                    parent = os.path.dirname(path)
                    parent_name = os.path.basename(parent)
                    if fnmatch.fnmatch(parent_name, pattern):
                        return True
                return True
        
        # Handle hidden file/folder exclusions
        if _exclude_hidden:
            try:
                relative = os.path.relpath(path, EXPANDUSER)
                
                if basename.startswith('.'):
                    return True
                
                parts = relative.split(os.sep)
                for part in parts[:-1]:
                    if part.startswith('.'):
                        return True
            except ValueError:
                pass
        
        return False
    
    if _should_exclude(path):
        return False
    
    # Time-based debounce to prevent infinite backup loops
    norm_path = os.path.normpath(path)
    current_time = time.time()

    if current_time - _LAST_EVENT_TIME.get(norm_path, 0) < DEBOUNCE_COOLDOWN:
        return False

    _LAST_EVENT_TIME[norm_path] = current_time
    
    # OPTIMIZATION: Periodically cleanup old debounce entries to prevent memory leak
    global _LAST_CLEANUP
    if current_time - _LAST_CLEANUP > _DEBOUNCE_CLEANUP_INTERVAL:
        _LAST_CLEANUP = current_time
        dict_size = len(_LAST_EVENT_TIME)
        
        if dict_size > _DEBOUNCE_LRU_MAX:
            # Remove oldest 10% of entries
            cutoff_size = int(_DEBOUNCE_LRU_MAX * 0.9)
            cutoff_time = current_time - (DEBOUNCE_COOLDOWN * 2)
            
            # Remove entries older than 2x debounce cooldown
            old_keys = [k for k, v in _LAST_EVENT_TIME.items() if v < cutoff_time]
            for key in old_keys[:len(old_keys) - cutoff_size + len(old_keys)]:
                del _LAST_EVENT_TIME[key]
            
            if old_keys:
                logging.debug(f"Debounce cache cleanup: removed {len(old_keys)} entries, "
                            f"remaining: {len(_LAST_EVENT_TIME)}")
    
    return True