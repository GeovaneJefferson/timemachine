#!/bin/bash

check_file() {
for f in $1:
do
    user_name=$(whoami)
    f="$(basename -- $f)"
    echo "$f" > /home/$user_name/.local/share/timemachine/src/scripts/restore_settings.txt
    cd /home/$user_name/.local/share/timemachine/src/ || exit
    python3 restore.py
done
}
check_file $PWD
