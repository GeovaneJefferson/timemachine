import os
import time
import uuid
import shutil
import hashlib
import logging
import stat
import fnmatch
from typing import Optional
from config import LARGE_FILE_THRESHOLD, DEBOUNCE_COOLDOWN, _LAST_EVENT_TIME, DIR_PATTERNS, FILE_PATTERNS, server, EXPANDUSER
    

def calculate_sha256(file_path: str, chunk_size=65536, file_size=None, retries=3) -> Optional[str]:
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None

    if file_size is None:
        try:
            file_size = os.stat(file_path).st_size
        except OSError:
            pass

    if file_size == 0:
        return hashlib.sha256(b"").hexdigest()

    if file_size and file_size > LARGE_FILE_THRESHOLD:
        try:
            st = os.stat(file_path)
            h = hashlib.sha256(f"{file_size}-{st.st_mtime}".encode())
            with open(file_path, "rb") as f:
                h.update(f.read(chunk_size))
                f.seek(file_size // 2)
                h.update(f.read(chunk_size))
                f.seek(-chunk_size, 2)
                h.update(f.read(chunk_size))
            return "quick_" + h.hexdigest()
        except Exception:
            return None

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
    path = os.path.normpath(path)
    if not os.path.isabs(path):
        path = os.path.join(os.path.expanduser("~"), path)
    rel = os.path.relpath(path, os.path.expanduser("~"))
    return rel.replace(os.sep, "/")


def should_process(path: str) -> bool:
    """Check if file should be processed."""
    if not os.path.exists(path):
        return False

    def _should_exclude(path: str) -> bool:
        """Check if path should be excluded."""
        all_patterns = DIR_PATTERNS + FILE_PATTERNS
        
        _exclude_hidden_val = server.get_database_value('EXCLUDE', 'exclude_hidden_itens')
        _exclude_hidden = str(_exclude_hidden_val).lower() == 'true' if _exclude_hidden_val else False
        
        basename = os.path.basename(path)
        is_directory = os.path.isdir(path) if os.path.exists(path) else False
        
        # Check patterns
        for pattern in all_patterns:
            if fnmatch.fnmatch(basename, pattern):
                if pattern in DIR_PATTERNS and not is_directory:
                    parent = os.path.dirname(path)
                    parent_name = os.path.basename(parent)
                    if fnmatch.fnmatch(parent_name, pattern):
                        return True
                return True
        
        # Hidden files/folders exclusion
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
    
    # Time-based debounce
    norm_path = os.path.normpath(path)
    current_time = time.time()

    if current_time - _LAST_EVENT_TIME.get(norm_path, 0) < DEBOUNCE_COOLDOWN:
        return False

    _LAST_EVENT_TIME[norm_path] = current_time
    return True