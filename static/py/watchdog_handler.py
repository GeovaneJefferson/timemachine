import os
import logging
from watchdog.events import FileSystemEventHandler
from filesystem import should_process


class BackupChangeHandler(FileSystemEventHandler):
    """Event handler with basic debouncing."""
    def __init__(self, event_queue):
        self.queue = event_queue

    def on_any_event(self, event):
        """Universal event handler."""
        if not should_process(event.src_path):
            return

        src = os.path.normpath(event.src_path)
        dst = os.path.normpath(getattr(event, "dest_path", "")) if hasattr(event, "dest_path") else ""

        try:
            if hasattr(event, 'dest_path'):
                self.queue.put(('moved', src, dst), timeout=1)
            else:
                self.queue.put((event.event_type, src, dst), timeout=1)
            logging.debug(f"Queued: {event.event_type} - {src}")
        except Exception:
            logging.warning("Event queue full")

    on_created = on_modified = on_deleted = on_moved = on_any_event