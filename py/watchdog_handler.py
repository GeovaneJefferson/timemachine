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
        # Skip directory events - we only care about files
        if event.is_directory:
            return

        if not should_process(event.src_path):
            return

        src = os.path.normpath(event.src_path)

        try:
            # FIX: Handle moved events properly with destination
            if hasattr(event, 'dest_path') and event.dest_path:
                dst = os.path.normpath(event.dest_path)

                # Check if destination should also be processed
                if should_process(dst):
                    self.queue.put(('moved', src, dst), timeout=5)  # IMPROVED: Increased from 1s to 5s
                    logging.debug(f"Queued: moved - {src} -> {dst}")
                else:
                    # Destination is excluded, treat as deletion
                    self.queue.put(('deleted', src, ''), timeout=5)  # IMPROVED: Increased timeout
                    logging.debug(f"Queued: deleted (moved to excluded) - {src}")
            else:
                # For non-move events, dst is not needed
                self.queue.put((event.event_type, src, None), timeout=5)  # IMPROVED: Increased timeout
                logging.debug(f"Queued: {event.event_type} - {src}")

        except Exception as e:
            # FIX: Better error handling - log which event failed
            logging.error(f"Event queue error (type={event.event_type}, src={src}): {e}")

    # Bind all event types to the unified handler
    on_created = on_modified = on_deleted = on_moved = on_any_event
