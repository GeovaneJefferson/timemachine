import json
import logging
import os
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


class MetadataStore:
    def __init__(self):
        self.metadata = {}
        self.hash_to_path_map = {}

    def load(self):
        """Load metadata from disk."""
        if not os.path.exists(server.METADATA_FILE):
            logging.info("No metadata file found, starting fresh")
            self.metadata = {}
            self.hash_to_path_map = {}
            return

        try:
            with open(server.METADATA_FILE, 'r', encoding='utf-8') as f:
                loaded_metadata = json.load(f)

            self.metadata = {}
            for key, val in loaded_metadata.items():
                normalized_key = normalize_rel_path(key, EXPANDUSER)
                self.metadata[normalized_key] = val

            logging.info(f"Loaded {len(self.metadata)} metadata entries")

            # Rebuild hash map
            self.hash_to_path_map = {}
            for key, val in self.metadata.items():
                file_hash = val.get('hash')
                backup_path = val.get('path')

                if file_hash and backup_path:
                    if backup_path.startswith(server.app_main_backup_dir()):
                        self.hash_to_path_map[file_hash] = backup_path
                    elif file_hash not in self.hash_to_path_map:
                        self.hash_to_path_map[file_hash] = backup_path

            logging.info(f"Loaded and normalized {len(self.metadata)} metadata entries")
        except Exception as e:
            logging.error(f"Failed to load metadata: {e}")
            self.metadata = {}
            self.hash_to_path_map = {}

    def save(self):
        """Save metadata to disk."""
        server.save_metadata(self.metadata)
        
    def get(self, key, default=None):
        """Get metadata entry with optional default value."""
        normalized_key = normalize_rel_path(key, EXPANDUSER)
        return self.metadata.get(normalized_key, default)
        
    def __getitem__(self, key):
        """Get metadata entry using dictionary syntax."""
        normalized_key = normalize_rel_path(key, EXPANDUSER)
        return self.metadata[normalized_key]
        
    def __setitem__(self, key, value):
        """Set metadata entry using dictionary syntax."""
        normalized_key = normalize_rel_path(key, EXPANDUSER)
        self.metadata[normalized_key] = value
        
    def __contains__(self, key):
        """Check if key exists in metadata."""
        normalized_key = normalize_rel_path(key, EXPANDUSER)
        return normalized_key in self.metadata
        
    def keys(self):
        """Get all keys in metadata."""
        return self.metadata.keys()
        
    def items(self):
        """Get all items in metadata."""
        return self.metadata.items()