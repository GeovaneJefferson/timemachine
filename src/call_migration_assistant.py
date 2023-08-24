from setup import *

# Message
print('Migration Assistant needs to run as root.')
# Request users password
sub.run(['sudo', 'python3', *sys.argv])
# sub.run(['pkexec', 'python3', *sys.argv])
# Clear terminal
sub.run(['clear'])
# Open Migration Assistant
sub.run(["python3", SRC_MIGRATION_ASSISTANT_PY])