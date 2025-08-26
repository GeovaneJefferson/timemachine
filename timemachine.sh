#!/bin/sh
# Start the Time Machine daemon
# exec python3 /app/share/timemachine/src/main.py

#!/bin/sh
# Start the Time Machine daemon
exec python3 /app/share/timemachine/src/main.py
export PYTHONPATH=/app/share/timemachine
exec python3 -m src.main