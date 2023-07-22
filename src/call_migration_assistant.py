from setup import *

if os.geteuid() != 0:
    print("Migration Assistant needs to run as root.")
    sub.run(['sudo', 'python3', *sys.argv])
    print("")
    print("Please wait...")
    print("")
    sub.run(f"python3 {SRC_MIGRATION_ASSISTANT_PY}", shell=True)