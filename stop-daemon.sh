#!/bin/sh
PID_FILE="$HOME/.var/app/com.gnome.timemachine/config/daemon.pid"
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    echo "Stopping Time Machine daemon (PID: $PID)..."
    kill "$PID"
else
    echo "Time Machine daemon not running (no PID file found)."
fi