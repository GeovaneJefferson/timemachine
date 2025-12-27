import socket
import json
import logging
import queue
import threading
import time
from config import server, truncate_path

class MessageSender:
    """Simplified message sender."""
    
    def __init__(self):
        self.socket_path = server.SOCKET_PATH
        self.timeout = 2
        self.message_queue = queue.Queue(maxsize=500)
        self.shutdown_event = threading.Event()
        self.sender_thread = None

    def start(self):
        """Start the message sender thread."""
        self.sender_thread = threading.Thread(
            target=self._sender_thread,
            daemon=True,
            name="MessageSender"
        )
        self.sender_thread.start()
        return self.sender_thread

    def _sender_thread(self):
        """Thread to send queued messages."""
        while not self.shutdown_event.is_set():
            try:
                msg = self.message_queue.get(timeout=0.5)
                self.send_message_sync(msg)
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Message sender error: {e}")

        # Drain remaining messages
        while not self.message_queue.empty():
            try:
                msg = self.message_queue.get_nowait()
                self.send_message_sync(msg)
            except:
                break

    def send_message_sync(self, message_data: dict) -> bool:
        """Send message via UNIX socket."""
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect(self.socket_path)
                sock.sendall((json.dumps(message_data) + "\n").encode("utf-8"))
            return True
        except Exception as e:
            logging.debug(f"Failed to send message: {e}")
            return False

    def send_file_status(self, rel_path: str, title: str, size: int, status: str):
        """Send file status message."""
        try:
            display_path = truncate_path(rel_path)
            self.message_queue.put({
                'type': 'file_activity',
                'title': title,
                'description': display_path,
                'size': size,
                'status': status,
                'timestamp': int(time.time())
            }, timeout=0.5)
        except Exception as e:
            logging.error(f"Send file status error: {e}")

    def send_progress_update(self, rel_path: str, file_size: int, 
                           files_backed_up_count: int, total_size_transferred: int,
                           total_files_to_scan: int = 0, total_transfer_size: int = 0,
                           backup_start_time: float = None):
        """Send progress update."""
        try:
            total_files = max(1, total_files_to_scan)
            total_bytes = max(1, total_transfer_size)

            if total_bytes > 0:
                progress = (total_size_transferred / total_bytes) * 100
            else:
                progress = (files_backed_up_count / total_files) * 100

            progress = min(100.0, max(0.0, progress))

            # Calculate ETA
            eta = "Calculating..."
            if backup_start_time and progress >= 0.5:
                elapsed = time.time() - backup_start_time
                if progress > 0:
                    total_estimate = elapsed / (progress / 100.0)
                    remaining = total_estimate - elapsed

                    if remaining > 1:
                        minutes = int(remaining / 60)
                        seconds = int(remaining % 60)
                        if minutes > 0:
                            eta = f"{minutes} min {seconds} sec"
                        else:
                            eta = f"{seconds} sec"
                    else:
                        eta = "Finishing soon"

            display_path = truncate_path(rel_path)

            self.message_queue.put({
                'type': 'backup_progress',
                'title': 'Backup Progress',
                'description': display_path,
                'progress': progress / 100.0,
                'status': 'running',
                'current_file': rel_path,
                'files_completed': files_backed_up_count,
                'total_files': total_files,
                'bytes_processed': total_size_transferred,
                'total_bytes': total_bytes,
                'eta': eta,
                'timestamp': int(time.time())
            }, timeout=0.5)
        except queue.Full:
            pass
        except Exception as e:
            logging.error(f"Error sending progress update: {e}")

    def shutdown(self):
        """Shutdown the message sender."""
        self.shutdown_event.set()
        if self.sender_thread and self.sender_thread.is_alive():
            self.sender_thread.join(timeout=2)