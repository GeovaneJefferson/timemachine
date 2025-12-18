#!/usr/bin/env python3
"""
BACKUP DAEMON — REBUILD STAGE 1 (CORE)
====================================

This is a COMPLETE, RUNNABLE daemon providing the core guarantees:

✓ Single-instance enforcement (OS-level UNIX socket lock)
✓ Watchdog real-time monitoring
✓ Atomic backups (temp file + os.replace)
✓ Per-file locking (no stale-lock hacks)
✓ Deduplication via SHA256 + hardlinks
✓ Metadata persistence (load/save)
✓ UI messaging via UNIX socket
✓ Polling safety net (full scan)

What is NOT included yet (next stages):
- Incremental backup trees
- Offline move detection
- Journal replay
- Flatpak backup
- Control commands

This file is safe to test on a second machine.
"""

import os
import sys
import time
import json
import uuid
import queue
import errno
import shutil
import socket
import signal
import hashlib
import logging
import threading
from typing import Dict, Optional
from concurrent.futures import ThreadPoolExecutor

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from server import *
from generate_backup_summary import generate_summary

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
POLLING_INTERVAL = 1800
MIN_REPROCESS_INTERVAL = 60
LARGE_FILE_THRESHOLD = 50 * 1024 * 1024
MAX_WORKERS = min(32, (os.cpu_count() or 4) * 2)

# ---------------------------------------------------------------------------
# PROCESS LOCK (SINGLE INSTANCE, STALE-SAFE)
# ---------------------------------------------------------------------------
class ProcessLock:
    def __init__(self, base_path: str):
        self.path = base_path + '.lock'
        self.sock = None

    def acquire(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self.sock.bind(self.path)
            return
        except OSError as e:
            if e.errno != errno.EADDRINUSE:
                raise

        # Socket exists — check if it's active
        try:
            test = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            test.settimeout(1)
            test.connect(self.path)
            test.close()
            # If connect succeeds, daemon is running
            raise RuntimeError('Daemon already running')
        except socket.error:
            # Stale socket — safe to remove
            try:
                os.remove(self.path)
            except OSError:
                raise RuntimeError('Cannot remove stale lock socket')

        # Retry bind
        self.sock.bind(self.path)

    def release(self):
        try:
            if self.sock:
                self.sock.close()
            if os.path.exists(self.path):
                os.remove(self.path)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# MESSAGE SENDER (UI)
# ---------------------------------------------------------------------------
class MessageSender:
    def __init__(self):
        self.socket_path = SERVER().SOCKET_PATH
        self.timeout = 2

    def send(self, message: dict) -> bool:
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect(self.socket_path)
                sock.sendall((json.dumps(message) + '\n').encode('utf-8'))
            return True
        except Exception:
            return False

# ---------------------------------------------------------------------------
# HASHING
# ---------------------------------------------------------------------------
def sha256(path: str, chunk: int = 65536) -> Optional[str]:
    try:
        st = os.stat(path)
        if st.st_size == 0:
            return hashlib.sha256(b'').hexdigest()
        if st.st_size > LARGE_FILE_THRESHOLD:
            return quick_hash(path, st)
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            while True:
                data = f.read(chunk)
                if not data:
                    break
                h.update(data)
        return h.hexdigest()
    except Exception:
        return None


def quick_hash(path: str, st) -> Optional[str]:
    try:
        h = hashlib.sha256()
        h.update(f"{st.st_size}-{st.st_mtime}".encode())
        with open(path, 'rb') as f:
            h.update(f.read(65536))
        return 'quick_' + h.hexdigest()
    except Exception:
        return None

# ---------------------------------------------------------------------------
# WATCHDOG HANDLER
# ---------------------------------------------------------------------------
class ChangeHandler(FileSystemEventHandler):
    def __init__(self, q, daemon):
        self.q = q
        self.daemon = daemon
        self.last = {}

    def on_any_event(self, event):
        if event.is_directory:
            return
        src = os.path.normpath(event.src_path)
        if self.daemon.should_exclude(src):
            return
        now = time.time()
        if now - self.last.get(src, 0) < 1:
            return
        self.last[src] = now
        dst = getattr(event, 'dest_path', None)
        try:
            self.q.put((event.event_type, src, dst), timeout=0.1)
        except queue.Full:
            pass

# ---------------------------------------------------------------------------
# DAEMON CORE
# ---------------------------------------------------------------------------
class BackupDaemon:
    def __init__(self):
        self.server = SERVER()
        self.home = os.path.expanduser('~')
        self.backup_root = self.server.app_main_backup_dir()

        self.event_q = queue.Queue(maxsize=5000)
        self.msg_q = queue.Queue(maxsize=500)
        self.shutdown = threading.Event()

        self.executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

        self.state_lock = threading.Lock()
        self.file_locks: Dict[str, threading.Lock] = {}

        self.metadata: Dict[str, dict] = {}
        self.hash_map: Dict[str, str] = {}
        self.last_processed: Dict[str, float] = {}

        self.watch_paths = self._load_watch_paths()
        self.exclude_hidden = str(
            self.server.get_database_value('EXCLUDE', 'exclude_hidden_itens')
        ).lower() == 'true'
        self.excludes = ['.git', 'node_modules', '__pycache__', '*.tmp']

        self.messenger = MessageSender()

    # ------------------------------------------------------------------
    def _load_watch_paths(self):
        raw = self.server.get_database_value('BACKUP_FOLDERS', 'folders') or ''
        paths = []
        for p in raw.split(','):
            p = os.path.abspath(os.path.expanduser(p.strip()))
            if os.path.isdir(p):
                paths.append(p)
        return paths

    # ------------------------------------------------------------------
    def should_exclude(self, path: str) -> bool:
        if self.exclude_hidden:
            rel = os.path.relpath(path, self.home)
            if any(part.startswith('.') for part in rel.split(os.sep)):
                return True
        name = os.path.basename(path)
        return any(name.endswith(p.replace('*', '')) for p in self.excludes)

    # ------------------------------------------------------------------
    def load_metadata(self):
        if not os.path.exists(self.server.METADATA_FILE):
            return
        try:
            with open(self.server.METADATA_FILE, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            for rel, meta in self.metadata.items():
                if 'hash' in meta and 'path' in meta:
                    self.hash_map[meta['hash']] = meta['path']
        except Exception:
            self.metadata = {}
            self.hash_map = {}

    # ------------------------------------------------------------------
    def save_metadata(self):
        try:
            self.server.save_metadata(self.metadata)
        except Exception:
            pass

    # ------------------------------------------------------------------
    def _file_lock(self, path: str) -> threading.Lock:
        with self.state_lock:
            self.file_locks.setdefault(path, threading.Lock())
            return self.file_locks[path]

    # ------------------------------------------------------------------
    def handle_event(self, ev):
        etype, src, dst = ev
        if etype == 'deleted':
            self.handle_delete(src)
        elif etype == 'moved' and dst:
            self.handle_move(src, dst)
        else:
            self.backup_file(src)

    # ------------------------------------------------------------------
    def backup_file(self, path: str):
        if not os.path.exists(path):
            return
        rel = os.path.relpath(path, self.home)
        now = time.time()
        if now - self.last_processed.get(rel, 0) < MIN_REPROCESS_INTERVAL:
            return

        h = sha256(path)
        if not h:
            return

        with self.state_lock:
            meta = self.metadata.get(rel)
            if meta and meta.get('hash') == h:
                self.last_processed[rel] = now
                return

        dest = os.path.join(self.backup_root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        tmp = dest + '.tmp_' + uuid.uuid4().hex

        try:
            if h in self.hash_map and os.path.exists(self.hash_map[h]):
                try:
                    os.link(self.hash_map[h], tmp)
                except OSError as e:
                    if e.errno != errno.EXDEV:
                        raise
                    shutil.copy2(path, tmp)
            else:
                shutil.copy2(path, tmp)

            with self._file_lock(dest):
                os.replace(tmp, dest)

            st = os.stat(path)
            with self.state_lock:
                self.metadata[rel] = {
                    'path': dest,
                    'hash': h,
                    'mtime': st.st_mtime,
                    'size': st.st_size
                }
                self.hash_map[h] = dest
                self.last_processed[rel] = now

            self._send_status(rel, 'Backed Up', 'success')

        except Exception:
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass

    # ------------------------------------------------------------------
    def handle_delete(self, path: str):
        rel = os.path.relpath(path, self.home)
        with self.state_lock:
            if rel in self.metadata:
                self.metadata[rel]['deleted'] = True
        self._send_status(rel, 'Deleted', 'error')

    # ------------------------------------------------------------------
    def handle_move(self, src: str, dst: str):
        if not os.path.exists(dst):
            self.handle_delete(src)
            return
        self.backup_file(dst)
        old = os.path.relpath(src, self.home)
        new = os.path.relpath(dst, self.home)
        with self.state_lock:
            if old in self.metadata:
                self.metadata[new] = self.metadata.pop(old)

    # ------------------------------------------------------------------
    def _send_status(self, rel: str, title: str, status: str):
        try:
            self.msg_q.put_nowait({
                'type': 'file_activity',
                'title': title,
                'description': rel,
                'status': status,
                'timestamp': int(time.time())
            })
        except queue.Full:
            pass

    # ------------------------------------------------------------------
    def worker_loop(self):
        while not self.shutdown.is_set():
            try:
                ev = self.event_q.get(timeout=0.5)
                self.executor.submit(self.handle_event, ev)
            except queue.Empty:
                pass

    # ------------------------------------------------------------------
    def message_loop(self):
        while not self.shutdown.is_set():
            try:
                msg = self.msg_q.get(timeout=0.5)
                self.messenger.send(msg)
            except queue.Empty:
                pass

    # ------------------------------------------------------------------
    def full_scan(self):
        for root in self.watch_paths:
            for base, _, files in os.walk(root):
                for name in files:
                    p = os.path.join(base, name)
                    if not self.should_exclude(p):
                        self.backup_file(p)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    server = SERVER()
    lock = ProcessLock(server.SOCKET_PATH)
    lock.acquire()

    daemon = BackupDaemon()
    daemon.load_metadata()

    def stop(*_):
        daemon.shutdown.set()

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    observer = Observer()
    handler = ChangeHandler(daemon.event_q, daemon)
    for p in daemon.watch_paths:
        observer.schedule(handler, p, recursive=True)
    observer.start()

    threading.Thread(target=daemon.worker_loop, daemon=True).start()
    threading.Thread(target=daemon.message_loop, daemon=True).start()

    last_scan = 0
    try:
        while not daemon.shutdown.is_set():
            if time.time() - last_scan > POLLING_INTERVAL:
                daemon.full_scan()
                generate_summary()
                last_scan = time.time()
            time.sleep(1)
    finally:
        daemon.shutdown.set()
        observer.stop()
        observer.join()
        daemon.executor.shutdown(wait=True)
        daemon.save_metadata()
        lock.release()


if __name__ == '__main__':
    main()
