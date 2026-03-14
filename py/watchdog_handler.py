import os
import logging
from watchdog.events import FileSystemEventHandler
from filesystem import should_process


class BackupChangeHandler(FileSystemEventHandler):
    """Event handler with basic debouncing."""
    def __init__(self, event_queue, daemon):
        self.queue = event_queue
        self.daemon = daemon

    def on_any_event(self, event):
        """Universal event handler."""
        src = os.path.normpath(event.src_path)

        # Handle directory creation for new watchers
        if event.is_directory and event.event_type == 'created':
            if not self.daemon.is_dir_excluded(src):
                try:
                    self.daemon.observer.schedule(self, src, recursive=False)
                    logging.debug(f"Scheduled new watcher on created directory: {src}")
                except Exception as e:
                    logging.error(f"Failed to schedule watcher on new directory {src}: {e}")
            return

        # Skip other directory events
        if event.is_directory:
            return

        if not should_process(event.src_path):
            return

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
