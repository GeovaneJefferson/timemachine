import json
import logging
import os
import sqlite3
import threading
from collections.abc import MutableMapping

from config import server, EXPANDUSER


def normalize_rel_path(path: str, base: str = None) -> str:
    """Normalize a relative path consistently for use as metadata keys."""
    if base is None:
        base = EXPANDUSER

    if not os.path.isabs(path):
        path = os.path.join(base, path)

    path = os.path.normpath(path)

    try:
        rel_path = os.path.relpath(path, base)
    except ValueError:
        rel_path = path

    rel_path = rel_path.replace(os.sep, '/')

    return rel_path


class _MetadataEntry(dict):
    """Dictionary wrapper that auto-commits changes back to the store."""

    def __init__(self, store, key, data):
        super().__init__(data or {})
        self._store = store
        self._key = key

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        self._store._write_entry(self._key, self)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._store._write_entry(self._key, self)


class MetadataStore(MutableMapping):
    """SQLite-backed metadata store.

    This keeps metadata on disk without loading the whole manifest into RAM.
    It is intentionally compatible with the previous dict-based API.
    """

    def __init__(self):
        # Maintain backward compatibility: code expects `daemon.metadata.metadata`.
        self.metadata = self

        self._db_path = server.METADATA_FILE
        logging.info(f"MetadataStore using database path: {self._db_path}")
        self._conn = None
        self._lock = threading.RLock()

        # Optional fast lookup cache for hashes.
        self.hash_to_path_map = {}

    def _connect(self):
        """Establish SQLite connection and ensure schema exists."""
        if self._conn is not None:
            return

        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA synchronous=NORMAL;")
        self._conn.execute("PRAGMA foreign_keys=ON;")
        self._ensure_schema()

    def _ensure_schema(self):
        """Create the metadata table if it does not exist."""
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS metadata (
                    path TEXT PRIMARY KEY,
                    hash TEXT,
                    mtime REAL,
                    size INTEGER,
                    deleted INTEGER DEFAULT 0,
                    deleted_time REAL,
                    backup_path TEXT,
                    data TEXT
                )
                """
            )
            self._conn.execute("CREATE INDEX IF NOT EXISTS idx_metadata_hash ON metadata(hash);")
            self._conn.execute("CREATE INDEX IF NOT EXISTS idx_metadata_deleted ON metadata(deleted);")

    def _write_entry(self, key: str, data: dict, commit: bool = True):
        """Write a single metadata entry to SQLite."""
        normalized_key = normalize_rel_path(key, EXPANDUSER)
        # Only store additional fields in the JSON blob to keep storage small.
        extra = {k: v for k, v in (data or {}).items() if k not in ('path', 'hash', 'mtime', 'size', 'deleted', 'deleted_time')}
        json_blob = json.dumps(extra, ensure_ascii=False) if extra else None

        with self._lock, self._conn:
            self._conn.execute(
                """
                INSERT INTO metadata (path, hash, mtime, size, deleted, deleted_time, backup_path, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    hash=excluded.hash,
                    mtime=excluded.mtime,
                    size=excluded.size,
                    deleted=excluded.deleted,
                    deleted_time=excluded.deleted_time,
                    backup_path=excluded.backup_path,
                    data=excluded.data
                """,
                (
                    normalized_key,
                    data.get('hash'),
                    data.get('mtime'),
                    data.get('size'),
                    1 if data.get('deleted') else 0,
                    data.get('deleted_time'),
                    data.get('path'),
                    json_blob,
                ),
            )

    def _row_to_dict(self, row):
        if row is None:
            return None

        # row = (path, hash, mtime, size, deleted, deleted_time, backup_path, data)
        base = {
            'path': row[6],
            'hash': row[1],
            'mtime': row[2],
            'size': row[3],
            'deleted': bool(row[4]),
            'deleted_time': row[5],
        }

        # Merge any additional fields from the JSON blob
        try:
            extra = json.loads(row[7]) if row[7] else {}
            if isinstance(extra, dict):
                base.update(extra)
        except Exception:
            pass

        return base

    def _get_row(self, key: str):
        normalized_key = normalize_rel_path(key, EXPANDUSER)
        with self._lock:
            cur = self._conn.execute(
                "SELECT path, hash, mtime, size, deleted, deleted_time, backup_path, data"
                " FROM metadata WHERE path = ?",
                (normalized_key,),
            )
            return cur.fetchone()

    def load(self):
        """Load or initialize metadata storage."""
        self._connect()

    def save(self):
        """Persist any pending changes."""
        if self._conn:
            with self._lock:
                self._conn.commit()

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __getitem__(self, key):
        row = self._get_row(key)
        if row is None:
            raise KeyError(key)
        return _MetadataEntry(self, normalize_rel_path(key, EXPANDUSER), self._row_to_dict(row))

    def __setitem__(self, key, value):
        self._write_entry(key, value)

    def __delitem__(self, key):
        normalized_key = normalize_rel_path(key, EXPANDUSER)
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM metadata WHERE path = ?", (normalized_key,))

    def __contains__(self, key):
        return self._get_row(key) is not None

    def __len__(self):
        with self._lock:
            cur = self._conn.execute("SELECT COUNT(*) FROM metadata")
            return cur.fetchone()[0]

    def __iter__(self):
        with self._lock:
            cur = self._conn.execute("SELECT path FROM metadata")
            for (path,) in cur:
                yield path

    def keys(self):
        return list(self.__iter__())

    def items(self):
        with self._lock:
            cur = self._conn.execute(
                "SELECT path, hash, mtime, size, deleted, deleted_time, backup_path, data FROM metadata"
            )
            for row in cur:
                yield (row[0], self._row_to_dict(row))

    # Convenience helpers ------------------------------------------------------
    def get_backup_path_for_hash(self, file_hash: str):
        """Return a backup path for a given hash (non-deleted)."""
        if not file_hash:
            return None
        with self._lock:
            cur = self._conn.execute(
                "SELECT backup_path FROM metadata WHERE hash = ? AND deleted = 0 LIMIT 1",
                (file_hash,),
            )
            row = cur.fetchone()
            return row[0] if row else None

    def count_hash_references(self, file_hash: str, include_deleted: bool = False) -> int:
        """Count how many entries exist for a given hash."""
        if not file_hash:
            return 0
        query = "SELECT COUNT(*) FROM metadata WHERE hash = ?"
        params = [file_hash]
        if not include_deleted:
            query += " AND deleted = 0"
        with self._lock:
            cur = self._conn.execute(query, params)
            return cur.fetchone()[0]

    def close(self):
        """Close the SQLite connection."""
        if self._conn:
            try:
                self._conn.commit()
                self._conn.close()
            except Exception:
                pass
            self._conn = None
