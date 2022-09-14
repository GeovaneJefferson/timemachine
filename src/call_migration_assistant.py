from setup import *

if os.geteuid() == 0:
    print("All set!")
else:
    print("Migration Assistant needs to run as root.")
    sub.call(['sudo', 'python3', *sys.argv])
    print("")
    print("Please wait...")
    print("")
    sub.call(f"python3 {src_migration_assistant}", shell=True)