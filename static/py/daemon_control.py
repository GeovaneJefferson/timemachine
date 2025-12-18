#!/usr/bin/env python3
"""Simple helper to send control commands to the daemon via the control UNIX socket.

Usage:
  python3 daemon_control.py --command cancel --mode graceful
  python3 daemon_control.py --command cancel --mode immediate

This can be invoked by the web backend when a user clicks "Stop Backup".
"""
import argparse
import json
import socket
import os
import sys
from static.py.server import SERVER


def send_control_command(command: str, mode: str = 'graceful', timeout: float = 2.0) -> bool:
    server = SERVER()
    ctrl_path = server.SOCKET_PATH + '.ctrl'
    payload = {'command': command, 'mode': mode}

    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect(ctrl_path)
            sock.sendall((json.dumps(payload) + "\n").encode('utf-8'))
            # try to read response
            try:
                resp = sock.recv(4096)
                if resp:
                    try:
                        obj = json.loads(resp.decode('utf-8'))
                        return obj.get('result') == 'ok'
                    except Exception:
                        return True
            except socket.timeout:
                return True
    except FileNotFoundError:
        print(f"Control socket not found: {ctrl_path}", file=sys.stderr)
        return False
    except ConnectionRefusedError:
        print(f"Connection refused to control socket: {ctrl_path}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Failed to send control command: {e}", file=sys.stderr)
        return False

    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--command', '-c', required=True, help='Command to send (cancel)')
    p.add_argument('--mode', '-m', choices=['graceful', 'immediate'], default='graceful')
    args = p.parse_args()

    ok = send_control_command(args.command, args.mode)
    if not ok:
        sys.exit(2)
    print('OK')


if __name__ == '__main__':
    main()

