import socket
import json
import time
import logging
import random
import sys

# --- MOCK DEPENDENCIES ---
# We define a mock Server class to provide the required SOCKET_PATH,
# mimicking the structure used in your daemon.py (e.g., from server import *)
class MockServer:
    """Mock class to provide the expected socket path."""
    SOCKET_PATH = "/tmp/time_machine_ui.sock"
    # Placeholder for APP_NAME as it might be used in logging/proctitle
    APP_NAME = "TimeMachine" 
    
# Use the mock server
server = MockServer()

# Configure basic logging for the test script
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s [%(levelname)s] %(message)s')

# --- send_to_ui FUNCTION (Copied from daemon.py for test context) ---

def send_to_ui(message: str):
    """
    Sends a JSON message to the UI via a Unix Domain Socket.
    (Error handling copied from user's daemon.py snippet.)
    """
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # Attempt to connect to the socket where the UI is listening
        sock.connect(server.SOCKET_PATH) 
        sock.sendall(message.encode("utf-8"))
        sock.close()
        logging.info(f"Successfully sent message to UI on {server.SOCKET_PATH}")
    except socket.timeout:
        logging.warning(f"send_to_ui: Socket operation timed out for {server.SOCKET_PATH}.")
    except FileNotFoundError:
        logging.debug(f"send_to_ui: Socket file not found at {server.SOCKET_PATH}. UI likely not running or socket not created yet.")
    except ConnectionRefusedError:
        # Common if UI is not running, but a key state to log for testing
        logging.info(f"send_to_ui: Connection refused at {server.SOCKET_PATH}. UI likely not running or not listening.")
    except Exception as e:
        logging.warning(f"send_to_ui: Error communicating with UI via {server.SOCKET_PATH}: {e}")

# --- HELPER FOR TEST DATA ---

def format_bytes(bytes_val, unit='MB'):
    """Simple helper to create human-readable speed/size strings for mock data."""
    if unit.upper() == 'MB':
        return f"{bytes_val / (1024 * 1024):.2f} MB"
    if unit.upper() == 'GB':
        return f"{bytes_val / (1024 * 1024 * 1024):.2f} GB"
    return f"{bytes_val} Bytes"

# --- SIMULATION LOGIC ---

def simulate_transfers():
    """Simulates sending various states of transfer messages."""
    
    logging.info("--- Starting UI message simulation ---")
    logging.info(f"Attempting to connect to socket: {server.SOCKET_PATH}")
    
    # --- 1. SIMULATE ACTIVE TRANSFER (Multiple updates for progress bar) ---
    file_id = "TRANS_001"
    file_size_bytes = 5_000_000_000 # 5 GB
    logging.info(f"Simulating active transfer for ID: {file_id}")
    
    for i in range(1, 6):
        progress = i * 20.0
        
        # Mock real-time data
        message = {
            "id": file_id, 
            "filename": "large_database_backup.sql",
            "size": format_bytes(file_size_bytes, 'GB'),
            "eta": f"{6 - i}m 30s",
            "speed": format_bytes(random.randint(15000000, 25000000)), # 15-25 MB/s
            "progress": progress,
            "status": "Transferring",
            "error": None
        }
        send_to_ui(json.dumps(message))
        time.sleep(0.5) # Wait half a second between updates

    # --- 2. SIMULATE SUCCESSFUL COMPLETION (100%) ---
    logging.info(f"Simulating completion for ID: {file_id}")
    message_complete = {
        "id": file_id, 
        "filename": "large_database_backup.sql",
        "size": format_bytes(file_size_bytes, 'GB'),
        "eta": "0s",
        "speed": "0 KB/s",
        "progress": 100.0,
        "status": "Completed",
        "error": None
    }
    send_to_ui(json.dumps(message_complete))
    time.sleep(1)

    # --- 3. SIMULATE ERROR STATE (The user's example error) ---
    file_id_error = "TRANS_ERR_002"
    file_size_bytes_error = 120_000_000 # 120 MB
    logging.info(f"Simulating error state for ID: {file_id_error}")

    message_error = {
        "id": file_id_error,
        "filename": "holiday_photos_2023.tar.gz",
        "size": format_bytes(file_size_bytes_error, 'MB'),
        "eta": "no space",
        "speed": "0 KB/s",
        "progress": 0.0,
        "error": "Not enough disk space",
        "status": "Failed"
    }
    send_to_ui(json.dumps(message_error))
    time.sleep(1)
    
    # --- 4. SIMULATE WAITING/QUEUED STATE ---
    file_id_queue = "TRANS_Q_003"
    file_size_bytes_queue = 800_000_000 # 800 MB
    logging.info(f"Simulating queued state for ID: {file_id_queue}")

    message_queue = {
        "id": file_id_queue,
        "filename": "new_os_patch.deb",
        "size": format_bytes(file_size_bytes_queue, 'MB'),
        "eta": "Waiting...",
        "speed": "0 KB/s",
        "progress": 0.0,
        "error": None,
        "status": "Queued" # Custom status for the UI to display
    }
    send_to_ui(json.dumps(message_queue))
    time.sleep(1)

    # --- 5. SIMULATE QUICK ACTIVITY LOG ENTRY (Recent Activity) ---
    file_id_activity = "ACTIVITY_004"
    file_size_bytes_activity = 1024 # 1 KB
    logging.info(f"Simulating quick activity log entry: Database Cleanup for ID: {file_id_activity}")

    # Start message (0%) - e.g., "Starting database optimization"
    message_start_activity = {
        "id": file_id_activity,
        "filename": "Database Optimization Script",
        "size": format_bytes(file_size_bytes_activity, 'Bytes'),
        "eta": "Running...",
        "speed": "N/A",
        "progress": 0.0,
        "error": None,
        "status": "Processing"
    }
    send_to_ui(json.dumps(message_start_activity))
    time.sleep(0.5)

    # Completion message (100%) - e.g., "Optimization successful"
    message_complete_activity = {
        "id": file_id_activity,
        "filename": "Database Optimization Script",
        "size": format_bytes(file_size_bytes_activity, 'Bytes'),
        "eta": "Completed",
        "speed": "N/A",
        "progress": 100.0,
        "error": None,
        "status": "Completed"
    }
    send_to_ui(json.dumps(message_complete_activity))
    time.sleep(1)


if __name__ == "__main__":
    simulate_transfers()
    logging.info("--- Simulation finished. Check UI for status updates. ---")
