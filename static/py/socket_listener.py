import socket
import json
import logging
import threading
import os


class SocketListener:
    def __init__(self, daemon):
        self.daemon = daemon
        self.control_socket_path = daemon.server.SOCKET_PATH + '.ctrl'

    def start_listener(self):
        """Start UNIX socket listener for daemon communication."""
        thread = threading.Thread(
            target=self._socket_listener_thread,
            daemon=True,
            name="SocketListener"
        )
        thread.start()
        return thread

    def _socket_listener_thread(self):
        """UNIX Socket listener thread."""
        self._remove_socket_file()

        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
                listener.bind(self.control_socket_path)
                listener.listen(1)
                logging.info(f"Listening for control commands on UNIX socket: {self.control_socket_path}")

                while not self.daemon.shutdown_event.is_set():
                    listener.settimeout(0.5)
                    try:
                        conn, _ = listener.accept()
                    except socket.timeout:
                        continue

                    with conn:
                        data = b''
                        while True:
                            chunk = conn.recv(4096)
                            if not chunk:
                                break
                            data += chunk

                        if data:
                            self._process_control_command(data.decode('utf-8'))
        except Exception as e:
            logging.error(f"CRITICAL: Control socket listener failed: {e}")
            self.daemon.shutdown_event.set()
        finally:
            self._remove_socket_file()

    def _process_control_command(self, data: str):
        """Processes commands received over the control socket."""
        try:
            command_obj = json.loads(data)
            command = command_obj.get('command')
            
            if command == 'cancel':
                logging.warning("Received 'cancel' command. Initiating shutdown.")
                self.daemon.shutdown_event.set()
                
            # Add logic for other commands here
        except Exception as e:
            logging.error(f"Error processing control command data: {e}")

    def _remove_socket_file(self):
        """Remove socket file."""
        try:
            if os.path.exists(self.control_socket_path):
                os.remove(self.control_socket_path)
        except:
            pass